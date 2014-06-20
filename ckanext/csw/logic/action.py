from ckan import logic
from ckan.logic import side_effect_free

@side_effect_free
def datastore_package_show(context, data_dict):
    id = data_dict['id']
    dataset_id = data_dict[dataset_id]

    print data_dict
    return