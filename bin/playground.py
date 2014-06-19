import os, sys
import argparse
from ConfigParser import SafeConfigParser
import requests
import logging
import datetime
import pycsw.config
import pycsw.repository

ckan_url = 'http://127.0.0.1:5000/'

logging.basicConfig(format='%(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

def setup_db(pycsw_config):

    from sqlalchemy import Column, Text

    database = pycsw_config.get('repository', 'database')
    table_name = pycsw_config.get('repository', 'table', 'records')

    ckan_columns = [
        Column('ckan_id', Text, index=True),
        Column('ckan_modified', Text),
    ]

    pycsw.admin.setup_db(database,
        table_name, '',
        create_plpythonu_functions=False,
        extra_columns=ckan_columns)

def load(pycsw_config, ckan_url):
    database = pycsw_config.get('repository', 'database')
    table_name = pycsw_config.get('repository', 'table', 'records')

    context = pycsw.config.StaticContext()
    repo = pycsw.repository.Repository(database, context, table=table_name)

    log.info('Started gathering CKAN datasets identifiers: {0}'.format(str(datetime.datetime.now())))

    query = 'api/search/dataset?qjson={"fl":"id,metadata_modified,extras_metadata_source", "q":"id:' \
            '[\\"\\" TO *]", "limit":1000, "start":%s}'
    start = 0
    gathered_records = {}

    while True:
        url = ckan_url + query % start

        response = requests.get(url)
        listing = response.json()
        if not isinstance(listing, dict):
            raise RuntimeError, 'Wrong API response: %s' % listing
        results = listing.get('results')
        if not results:
            break
        for result in results:
            gathered_records[result['id']] = {
                'metadata_modified': result['metadata_modified'],
                'id': result['id'],
            }

        start = start + 1000
        log.debug('Gathered %s' % start)

    log.info('Gather finished ({0} datasets): {1}'.format(
        len(gathered_records.keys()),
        str(datetime.datetime.now())
    ))

    existing_records = {}

def _load_config(file_path):
    abs_path = os.path.abspath(file_path)
    if not os.path.exists(abs_path):
        raise AssertionError('pycsw config file {0} does not exist.'.format(abs_path))
    config = SafeConfigParser()
    config.read(abs_path)
    return config

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--pycsw_config',
                        action = 'store', default = 'default.cfg',
                        help = 'pycsw config file to use.')

    parser.add_argument('-u', '--ckan_url',
                        action = 'store',
                        help = 'CKAN instance to import the datasets from.')

    if len(sys.argv) <= 1:
        parser.print_usage()
        sys.exit(1)

    arg = parser.parse_args()
    pycsw_config = _load_config(arg.pycsw_config)

    if arg.command == 'setup':
        setup_db(pycsw_config)
    elif arg.command == 'load':
        load(pycsw_config, ckan_url)
    elif arg.command == 'clear':
        clear(pycsw_config)
    else:
        print 'Unknown command {0}'.format(arg.command)
        sys.exit(1)
