import ckan.plugins as p
import ckanext.csw.logic.action as action


class DatastoreCSW(p.SingletonPlugin):
    p.implements(p.IConfigurable)
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IActions)
    p.implements(p.IAuthFunctions)
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.IResourceUrlChange)
    p.implements(p.IResourceController, inherit=True)

    def configure(self, config):
        return

    def update_config(self, config):
        templates = 'templates'
        p.toolkit.add_template_directory(config, templates)

    def before_map(self, map):
        controller = 'ckanext.csw.controllers.view:ViewController'
        map.connect('datastore_package_show', '/datastore_package/object/:id',
                    controller=controller, action='show_object')
        return map

    def get_actions(self):
        return {
            'iso_metadata': action.iso_metadata,
        }

    def get_auth_functions(self):
        return {}