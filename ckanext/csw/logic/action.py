from ckan import logic
import ckan.plugins as p
from ckan.logic import side_effect_free

@side_effect_free
def datastore_package_show(context, data_dict):

    id = data_dict['id']

    if id:
        pkg = logic.action.get.package_show(context, data_dict)
        if not pkg:
            raise p.toolkit.ObjectNotFound('Dataset not found')
    else:
        raise p.toolkit.ValidationError('Please provide a package ID')

    return pkg