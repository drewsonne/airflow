# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
from collections import namedtuple

from expiringdict import ExpiringDict

from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.plugins.base import AirflowConfigurationProviderPlugin

VersionedParam = namedtuple('VersionedParam', ['section', 'key', 'value', 'version'])


class AwsSsmConfigurationProvider(AirflowConfigurationProviderPlugin):
    """
    Provide access to configurations stored in AWS SSM Parameter store
    """

    defaults = {
        'ssm_param_max_age': 720,
        'ssm_aws_conn_id': 'aws_default',
        'ssm_path_prefix': '/airflow'
    }

    @property
    def source_name(self):
        return 'aws ssm'

    def __init__(self, conf):
        super(AwsSsmConfigurationProvider, self).__init__(conf)

        self._cache = ExpiringDict(
            max_len=1000,
            max_age_seconds=self._conf['ssm_param_max_age'])
        self._ssm = AwsHook(
            aws_conn_id=self._conf['ssm_aws_conn_id']
        ).get_client_type('ssm')

    def has_section(self, section):
        self.get_section(section)
        return section in self._cache

    def get_section(self, section):
        if section not in self._cache:
            response = self._ssm.get_parameters_by_path(
                Path=self._ssm_section(section),
                Recursive=True,
                WithDecryption=True
            )
            configuration = self._parse_ssm_response(response)
            self._cache[section] = configuration[section]

        return self._cache[section]

    def get_var_option(self, section, key):
        section = self.get_section(section)
        if key in section:
            return section[key]
        return None

    def _ssm_section(self, section):
        return "{prefix}/{section}".format(
            prefix=self._conf['ssm_path_prefix'].rstrip('/'),
            section=section
        )

    def _ssm_key(self, section, key):
        return "{prefix}/{key}".format(
            prefix=self._ssm_section(section),
            key=key
        )

    def _parse_ssm_response(self, parameters):
        versioned_params = []
        for parameter in parameters:
            normalised_name = parameter['Name'].lstrip(
                self._conf['ssm_path_prefix']
            )
            section, key = normalised_name.split('/')
            versioned_params.append(VersionedParam(
                section=section,
                key=key,
                value=parameter['Value'],
                version=int(parameter['Version'])
            ))

        sections = {}
        for param in versioned_params:
            if param.section not in sections:
                sections[param.section] = {}
            if param.key not in sections[param.section]:
                sections[param.section][param.key] = []

            sections[param.section][param.key].append(param)

        for section_name, section in sections.items():
            for key, values in section.items():
                sorted_values = sorted(values, key=lambda p: p.version)
                sections[section_name][key] = sorted_values[0].value

        return sections
