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
from abc import ABCMeta, abstractmethod, abstractproperty


class AirflowConfigurationProviderPlugin(object):
    """
    Providers an interface for retrieving configurations
    from an arbitrary source
    """
    __metaclass__ = ABCMeta

    defaults = {}

    priority = 0

    def __init__(self, conf):
        """
        :param conf: Configuration key/values from conf_provider section
        """
        self._conf = conf
        for key, value in self.defaults.items():
            if key not in self._conf:
                self._conf[key] = value

    @abstractproperty
    def source_name(self):
        """
        Name to return in the config source property. This should be lower case
        short, and use only spaces or periods.
        """
        raise NotImplementedError

    @abstractmethod
    def as_dict(self, display_source=False, display_sensitive=False):
        """
        Fetch all configuration sections

        :param display_source: If False, the option value is returned. If True,
            a tuple of (option_value, source) is returned. Source is either
            'airflow.cfg', 'default', 'env var', or 'cmd'.
        :type display_source: bool
        :param display_sensitive: If True, the values of options set by env
            vars and bash commands will be displayed. If False, those options
            are shown as '< hidden >'
        :type display_sensitive: bool
        """
        raise NotImplementedError

    @abstractmethod
    def get_var_option(self, section, key):
        """
        For a given section and key, return  a configuration result
        if this provider has this section and key available.

        :param section: Section of the airflow config to search for the key in
        :type section: basestring
        :param key: Unique identifier within the section to search for a configuration value in
        :type key: basestring
        """
        raise NotImplementedError

    @abstractmethod
    def has_section(self, section):
        """
        Return true if the provider has the section in question

        :param section: section from the config
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def get_section(self, section):
        """
        Returns the section as a dict. Values are converted to int, float, bool
        as required.
        :param section: section from the config
        :return: dict
        """
        raise NotImplementedError
