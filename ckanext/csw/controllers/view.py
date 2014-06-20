import ckan.plugins as p
from ckan import model
from ckan.lib.base import BaseController, c, abort
from pylons.i18n import _

class ViewController(BaseController):
    def show_object(self, id, ref_type='object'):
        try:
            context = {'model': model, 'user': c.user}
            if ref_type == 'object':
                obj = p.toolkit.get_action('datastore_package_show')(context, {'id': id})
            elif ref_type == 'dataset':
                obj = p.toolkit.get_action('datastore_package_show')(context, {'dataset_id': id})
        except p.toolkit.ObjectNotFound, e:
            abort(404,_(str(e)))
        except p.toolkit.NotAuthorized:
            abort(401, self.not_auth_message)
        except Exception, e:
            msg = 'An error ocurred: [%s]' % str(e)
            abort(500g)