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
from flask import Blueprint

from airflow.plugins_manager import AirflowPlugin


class PluginAdmin(AirflowPlugin):
    name = 'plugin_admin'

    @classmethod
    def on_load(cls, *args, **kwargs):
        cls.register_flask_blueprints(Blueprint(
            "plugin_admin",
            __name__,
            template_folder='templates',  # registers airflow/plugins/templates as a Jinja template folder
            static_folder='static',
            static_url_path='/static/test_plugin'
        ))

    @classmethod
    def on_app_load(cls, appbuilder, *args, **kwargs):
        from airflow.contrib.plugins.plugin_admin.models import PluginAdminAppBuilderBaseView

        v = PluginAdminAppBuilderBaseView()
        appbuilder.add_view(
            view=v,
            name='Plugins',
            category='Admin',
            icon='fa-puzzle-piece'
        )
