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
import os

from airflow.configuration import env_var

AIRFLOW_HOME = env_var.get('AIRFLOW_HOME', '~/airflow', expand=True)

DEFAULT_CONFIG = os.path.join('config_templates', 'default_airflow.cfg')
TEST_CONFIG = os.path.join('config_templates', 'default_test.cfg')

WEBSERVER_CONFIG = AIRFLOW_HOME + '/webserver_config.py'

if 'AIRFLOW_CONFIG' in os.environ:
    AIRFLOW_CONFIG = env_var.expand('AIRFLOW_CONFIG')
else:
    AIRFLOW_CONFIG = os.path.join(AIRFLOW_HOME, 'airflow.cfg')

