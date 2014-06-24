import json
import nose
import paste.fixture
import pylons.test
import pylons.config as config
import sqlalchemy.orm as orm
import ckan.config.middleware as middleware
import ckan.lib.create_test_data as ctd
import ckan.model as model
import ckan.tests as tests
import ckan.plugins as plugins
import ckanext.datastore.db as db
from ckanext.datastore.tests.helpers import rebuild_all_dbs, set_url_type

from bin import datastore_pycsw

class TestDatastoreCswPlugin(tests.WsgiAppCase):
    sysadmin_user = None
    normal_user = None

    @classmethod
    def setup_class(cls):
        wsgiapp = middleware.make_app(config['global_conf'], **config)
        cls.app = paste.fixture.TestApp(wsgiapp)

        if not tests.is_datastore_supported():
            raise nose.SkipTest("Datastore not supported")

        plugins.load('datastore')
        plugins.load('datastorecsw')

        ctd.CreateTestData.create()
        cls.sysadmin_user = model.User.get('testsysadmin')
        cls.normal_user = model.User.get('annafan')

        engine = db._get_engine(
            {'connection_url': pylons.config['ckan.datastore.write_url']})
        cls.Session = orm.scoped_session(orm.sessionmaker(bind=engine))
        set_url_type(model.Package.get('annakarenina').resources, cls.sysadmin_user)

    @classmethod
    def teardown_class(cls):
        rebuild_all_dbs(cls.Session)
        plugins.unload('datastore')
        plugins.unload('datastorecsw')

    def test_create_datastore_resource_in_package(self):
        package = model.Package.get('annakarenina')
        data = {'resource': {'package_id': package.id}}
        postparams = '%s=1' % json.dumps(data)
        auth = {'Authorization': str(self.sysadmin_user.apikey)}
        res = self.app.post('/api/action/datastore_create', params=postparams,
                            extra_environ=auth, status=200)
        res_dict = json.loads(res.body)
        assert 'resource_id' in res_dict['result']
        assert len(model.Package.get('annakarenina').resources) == 3

        res = tests.call_action_api(self.app, 'resource_show',
                                    id=res_dict['result']['resource_id'])
        assert res['url'] == '/datastore/dump/' + res['id'], res