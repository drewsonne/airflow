from flask import Blueprint
from flask_appbuilder import BaseView, expose

from airflow.plugins_manager import AirflowPlugin


class PluginAdminAppBuilderBaseView(BaseView):
    default_view = 'index'

    @expose("/")
    def index(self):
        return self.render("test_plugin/test.html", content="Hello galaxy!")


class PluginAdmin(AirflowPlugin):
    name = 'plugin_admin'
    appbuilder_views = []
    flask_blueprints = []

    @classmethod
    def on_load(cls, *args, **kwargs):
        cls.appbuilder_views.append({
            "name": "Plugins",
            "category": "Admin",
            "view": PluginAdminAppBuilderBaseView(),
            "href": "/admin/plugins"
        })

        cls.flask_blueprints.append(Blueprint(
            "plugin_admin",
            __name__,
            template_folder='templates',
            static_folder='static',
            static_url_path='/static/plugin_admin'
        ))
