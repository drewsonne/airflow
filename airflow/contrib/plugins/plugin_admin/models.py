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

from flask_appbuilder.models.generic import GenericColumn, GenericModel, GenericSession
from flask_appbuilder.models.generic.interface import GenericInterface

from airflow.plugins_manager import AirflowPlugin, plugins
from airflow.www.views import AirflowModelView


class AirflowPluginModel(GenericModel):
    Name = GenericColumn(str, primary_key=True)
    Module = GenericColumn(str)
    Source = GenericColumn(str)


class AirflowPluginSession(GenericSession):
    def _add_plugin(self, plugin):
        model = AirflowPluginModel()
        model.Name = plugin.name
        model.Module = plugin.get_module()
        model.Source = 'Package' if plugin.load_type == AirflowPlugin.LOAD_TYPE_PKG else 'File'

        self.add(model)

    def _import_plugin_models(self):
        for p in plugins:
            self._add_plugin(p)

    def get(self, pk):
        self.delete_all(AirflowPluginModel())
        self._import_plugin_models()
        return super(AirflowPluginSession, self).get(pk)

    def all(self):
        self.delete_all(AirflowPluginModel())
        self._import_plugin_models()
        return super(AirflowPluginSession, self).all()


sess = AirflowPluginSession()


class PluginAdminAppBuilderBaseView(AirflowModelView):
    list_title = 'Loaded Plugins'

    route_base = '/admin/plugins'

    datamodel = GenericInterface(AirflowPluginModel, sess)

    base_permissions = ['can_list', 'can_show']

    list_columns = ['Name', 'Module', 'Source']
    search_columns = ['Name', 'Source']
