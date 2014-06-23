import paste.fixture
import pylons.test
import pylons.config as config
import webtest

import ckan.model as model
import ckan.tests as tests
import ckan.plugins as plugins
import requests

from bin import datastore_pycsw
from nose.tools import assert_equal

class TestDatastoreCswPlugin(object):

    """
    @classmethod
    def setup_class(cls):
        plugins.load('datastorecsw')
        return config

    @classmethod
    def teardown_class(cls):
        plugins.unload('datastorecsw')
    """

    def test_iso_metadata(self):
        result = tests.call_action_api(config, 'iso_metadata',
                                       apiKey=None, name='blue')