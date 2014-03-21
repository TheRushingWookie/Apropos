import sqlite3
import uuid
import os
import logging
import json
import hmac
import base64
from main import *
from DBClasses import *
from Analytics import user, api_analytics
from time import gmtime, strftime
from random import randrange
from fuzzywuzzy import process, fuzz
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from hashlib import sha1
from collections import OrderedDict


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


conn = sqlite3.connect(os.getcwd() + '/API' + '.db', check_same_thread=False)


def set_logger(logger_instance):
    ''' Sets up a logging instance in the global var logger'''
    global logger
    logger = logger_instance
    logger.warn('new logger')


def fetchall_to_list(query_rows, col):
    '''Returns a single column in a list of a query'''
    filtered_rows = []
    for row in query_rows:
        filtered_rows.append(row[col])
    return filtered_rows


def fetch_single_val(query_rows, col):
    for row in query_rows:
        return row[col]

id_one_selector = '''select id from (?) where (?) = (?)'''
id_two_selector = '''select id from (?) where (?) = (?) and (?) = (?)'''


def find_id(table_name, query_dict):
    '''Finds the id of the row with matching query_dict for the table. Returns id'''
    global id_one_selector, id_two_selector
    c = conn.cursor()

    selector_string = id_one_selector
    selector_vals = ()
    if len(query_dict.keys()) > 1:

        for i in query_dict.keys():
            selector_string += ' and (?) = (?)'
            selector_vals += (i, query_dict[i])
    else:
        key = query_dict.keys()[0]
        selector_vals = (key, query_dict[key])
    selector_string = '''select id from (?) where (?) = (?)'''
    return fetch_single_val(c.execute(selector_string, selector_vals), 0)


def create_apropos_tables():
    '''Sets up database tables.'''
    # Create table
    c = conn.cursor()
    c.execute('''CREATE TABLE tags
            (
                id integer PRIMARY KEY,
                tag_name text )''')

    c.execute('''CREATE TABLE tagmap
            (
            id integer PRIMARY KEY,
            tag_id integer,
             api_id integer)''')

    c.execute('''CREATE TABLE api_providers
        (
            id integer PRIMARY KEY,
        date text,
        api_provider_name text,
        email text,
        owner_key text)''')

    c.execute('''CREATE TABLE api_endpoints
        (
        id integer PRIMARY KEY,
        date text,
        api_name text,
        api_url text,
        owner_key text,
        category text,
        api_provider_id integer, FOREIGN KEY(owner_key) REFERENCES api_providers(owner_key))
        ''')

    c.execute('''CREATE TABLE api_authent_info (
            id integer PRIMARY KEY,
            date text,
            info_json text ,
            api_endpoint_id integer, FOREIGN KEY(api_endpoint_id) REFERENCES api_endpoints(id))''')
    c.execute('''CREATE TABLE api_authent_terms (
                                                id integer PRIMARY KEY,
                                                date text,
                                                owner_key text,
                                                authent_json text,
                                                api_endpoint_id integer, FOREIGN KEY(api_endpoint_id) REFERENCES api_endpoints(id))''')
    # Insert a row of data

    # Save (commit) the changes
    conn.commit()
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.


def generate_uuid():
    '''Used to generate a provider key. The key serves as a password for each api_provider_name.'''
    return str(uuid.uuid4())


def get_key_hmac(base_string, provider_key):
    assert (provider_key)
    return base64.urlsafe_b64encode(hmac.new(provider_key.encode('ascii'), base_string.encode('ascii'), sha1).digest())


def hmac_json_string(json_input_unordered, key):
    json_input = OrderedDict(
        sorted(json_input_unordered.items(), key=lambda t: t[0]))
    hmac = get_key_hmac(json.dumps(json_input), key)
    json_input['hmac'] = hmac
    return json.dumps(json_input)


def verify_owner(api_provider_name, input_json):
    '''Verify that the api_provider_name corresponds to the owner_key
        Returns true if it matches'''
    c = conn.cursor()
    logger.debug('''api_provider_name %s''', api_provider_name)
    owner_key = api_providers.query.filter_by(
        api_provider_name=api_provider_name).one().owner_key
    logger.debug('json before hmac %s', json.dumps(input_json))
    hmac = input_json['hmac']
    del input_json['hmac']
    logger.debug('json after hmac %s ', json.dumps(input_json))
    db_generated_hmac_json = hmac_json_string(input_json, owner_key)
    dbhmac = json.loads(db_generated_hmac_json)['hmac']
    owner_verified = (dbhmac == hmac)
    if owner_verified:
        return True
    logger.debug(
        '''owner_key: %s . provided_hmac %s .wanted hmac %s . api_provider_name %s . owner_verified %s .''',
        owner_key, hmac, dbhmac, api_provider_name, owner_verified)
    return False


def if_provider_exists(provider_name, c):
    '''Verifies if a provider already exists'''
    provider_results = fetch_single_val(
        c.execute ('''Select api_provider_name from api_providers where api_provider_name = ?''', (provider_name,)).fetchall(), 0)
    if provider_results:
        return True
    else:
        return False


def register_api_provider(api_provider_name, email):
    '''Creates an account for an API provider.
        Returns the provider key if the provider does not exist.'''
    c = conn.cursor()
    time = strftime("%a, %d %b %Y %X +0000", gmtime())
    if not if_provider_exists(api_provider_name, c):
        provider_key = generate_uuid()
        c.execute("insert into api_providers values (NULL,?, ?, ?, ?)",
                  (time, api_provider_name, email, provider_key))
        conn.commit()
        return provider_key
    else:
        return None


def add_authent_info(api_provider_name, api_endpoint_name, authent_info_json):
    '''Adds an API key to the DB. Submitter does not need to be verified as anyone can submit an API key. A captcha should prevent spamming. Returns true or false based on success.'''
    c = conn.cursor()
    time = strftime("%a, %d %b %Y %X +0000", gmtime())
    provider_id = fetch_single_val(
        c.execute (''' select id from api_providers where api_provider_name = ?''', (api_provider_name,)).fetchall(), 0)
    if provider_id:
        # authenticate that a provider exists with the gvien name
        api_endpoint_id = fetch_single_val(
            c.execute('''select id from api_endpoints where api_name = (?) and api_provider_id = (?)''', (api_endpoint_name, provider_id)).fetchall(), 0)

        if api_endpoint_id:
            # If an api_endpoint with the given name and provider proceed
            authent_terms_json = fetch_single_val(
                c.execute('''select authent_json from api_authent_terms where api_endpoint_id = ?''', (api_endpoint_id,)), 0)
            if authent_terms_json:
                logger.debug(
                    'add_authent_info:authent_terms_json for %s is %s', api_provider_name, authent_terms_json)
                authent_terms = json.loads(authent_terms_json)
                authent_info = json.loads(authent_info_json)
                for i in authent_terms.keys():
                    if i not in authent_info:
                        logger.warning(
                            '''add_authent_info:Missing json key %s in json %s for api %s''', i, authent_info_json, api_endpoint_name)
                        return False
                c.execute('''insert into api_authent_info values (NULL,?,?,?)''', (
                    time, authent_info_json, api_endpoint_id))
                conn.commit()
                return True
            else:
                logger.warning('add_authent_info: authent terms for %s not found for info %s' (
                    api_endpoint_name, authent_info_json))
        else:
            logger.warning(
                'add_authent_info: no endpoint found for %s', (api_endpoint_name,))
    else:
        logger.warning(
            'add_authent_info: No provider id found for name %s', (api_provider_name))
    return False


def add_api_authent_terms(api_provider_name, api_endpoint_name, owner_key, terms, endpoint_id, time):
    '''Updates the terms that need to exist in any api_key json. Can only be used by the owner of the api provider account. Returns true/false depending on success.'''
    c = conn.cursor()
    c.execute('''insert into api_authent_terms values (NULL,?,?,?,?)''',
              (time, owner_key, terms, endpoint_id))



def get_authent_info(api_endpoint_name):
    '''Get a random authent info'''
    c = conn.cursor()
    endpoint_id = fetch_single_val(
        c.execute('''select id from api_endpoints where api_name = (?)''', (api_endpoint_name,)).fetchall(), 0)
    if endpoint_id:

        possible_keys = fetchall_to_list(
            c.execute('''select info_json from api_authent_info where api_endpoint_id = (?)''', (endpoint_id,)).fetchall(), 0)

        if possible_keys:
            random_index = randrange(len(possible_keys))
            return possible_keys[random_index]
        else:
            logger.warning(
                'get_authent_info: No possible keys found for apiendpoint %s', api_endpoint_name)
    else:
        logger.warning(
            '''get_authent_info: Failed to find endpoint_id for endpoint %s''', api_endpoint_name)

    return False


def add_tags_to_endpoint(tags, c, api_id):
    for tag in tags:
        # loop through tags inserting each into the tags table and make a link via the tagmap table. If the tag already exists, link the pre-existing tag.
        prev_tag = fetch_single_val(
            c.execute('''select id from tags where tag_name = (?)''', (tag,)).fetchall(), 0)
        if prev_tag:
            tag_id = prev_tag
        else:
            c.execute('''insert into tags values (NULL,?)''', (tag,))
            tag_id = fetch_single_val(
                c.execute('''select id from tags where tag_name = (?)''', (tag,)).fetchall(), 0)

        c.execute(
            '''insert into tagmap values (NULL, ?,?)''', (tag_id, api_id))


def print_table(table_name):
    c = conn.cursor()
    results = c.execute('''select * from ''' + table_name ).fetchall()
    return results


def get_tags(api_endpoint_name):
    api_id = api_endpoints.query.filter_by(
        api_name=api_endpoint_name).first().id
    tag_links = tagmap.query.filter_by(api_id=api_id).all()
    tags_list = []
    for tag_link in tag_links:
        tags_list += [tags.query.filter_by(id=tag_link.tag_id).one().tag_name]
    print tags_list
print get_tags('openweathermap')

def update_tags(api_provider_name, api_endpoint_name, new_tags, json_input):
    '''Lets a proxy reconfigure its tags'''
    owner_verified = verify_owner(api_provider_name, json_input)
    if owner_verified:
        try:
            owner_key = api_providers.query.filter_by(
                api_provider_name=api_provider_name).one().owner_key
            api_id = api_endpoints.query.filter_by(
                api_name=api_endpoint_name, owner_key=owner_key).first().id
            try:
                old_tags = tagmap.query.filter_by(api_id=api_id).all()

                for tag in old_tags:
                    # print tag
                    db.session.delete(tag)
                db.session.commit()
                c = conn.cursor()
                add_tags_to_endpoint(new_tags, c, api_id)
                conn.commit()
            except SQLAlchemyError:
                logger.warning(
                    'No old_tags found for api %s with id %s', api_endpoint_name, api_id)
        except SQLAlchemyError:
            logger.warning('No api_id found for api %s', api_endpoint_name)
    else:
        logger.warning(
            'Unverified update_tags %s %s.', api_provider_name, api_endpoint_name)


def test_update_tags():
    '''Test function for update_tags'''
    prev_tag_ids = tagmap.query.filter_by(api_id=1).all()
    api_endpoint = api_endpoints.query.filter_by(id=1).one()
    tags_to_be_updated = ['test_tag1', 'test_tag2', 'test_tag31']
    prev_tags = []
    for prev_tag in prev_tag_ids:
        prev_tags += [tags.query.filter_by(
            id=prev_tag.tag_id).one().tag_name, ]
    logger.debug('Prev tags are %s', prev_tags)
    update_tags(api_endpoint.api_provider.api_provider_name,
                api_endpoint.api_name, api_endpoint.owner_key, tags_to_be_updated)
    new_tag_ids = tagmap.query.filter_by(api_id=1).all()
    new_tags = []
    for new_tag in new_tag_ids:
        new_tags += [tags.query.filter_by(id=new_tag.tag_id).one().tag_name, ]
    logger.debug('New tags are %s', new_tags)
    assert new_tags == tags_to_be_updated
    # db.session.delete()
#test_update_tags()

def add_api_endpoint(api_provider_name, api_name, api_url, category, tags, api_authent_terms, json_input):
    '''Adds an api endpoint to the db and adds the tags and api_authent_terms to their respective tables. Returns true or false depending on success.'''
    c = conn.cursor()

    owner_verified = verify_owner(api_provider_name, json_input)
    # Check that owner key matches the provided api_provider_name
    if owner_verified:
        owner_key = api_providers.query.filter_by(
            api_provider_name=api_provider_name).one().owner_key
        time = strftime("%a, %d %b %Y %X +0000", gmtime())
        provider_results = fetch_single_val(
            c.execute ('''Select api_name from api_endpoints where api_name = (?)''', (api_name,)).fetchall(), 0)
        # Check if a api_endpoint with the same name already exists
        if provider_results:
            logger.info('''add_api_endpoint:Previous provider found.''')
            return False
        else:  # add a new api_endpoint
            provider_id = fetch_single_val(
                c.execute (''' select id from api_providers where api_provider_name = ?''', (api_provider_name,)).fetchall(), 0)
            if provider_id:  # find the provider row
                c.execute('''insert into api_endpoints values (NULL,?,?,?,?,?,?)''', (
                    time, api_name, api_url, owner_key, category, provider_id))  # add the endpoint
                id = fetch_single_val(
                    c.execute (''' select id from api_endpoints where api_name = (?) and owner_key = (?)''', (api_name, owner_key,)).fetchall(), 0)
                # add the authent terms to the authent terms table
                conn.commit()
                add_api_authent_terms(
                    api_provider_name, api_name, owner_key, api_authent_terms, id, time)
                conn.commit()
                add_tags_to_endpoint(tags, c, id)
                conn.commit()
                return True

            else:
                logger.warning('''add_api_endpoint:Missing provider id.''')
    else:
        logger.warning('''add_api_endpoint:Owner not verified''')
        return False


test_api_id = ""


def create_test_db():
    global test_api_id
    # create_apropos_tables()
    db.create_all()
    db.session.commit()
    test_api_id = register_api_provider(
        "Example_provider", "example@example.com")
    logger.debug(print_table("api_providers"))
    #test_api_id = u'4150c9e7-c1a6-4511-bca1-7cb5bb3a724e'

    # add_api_key("Example_provider","test_api3",test_api_id,"wdwd")
    conn.commit()
    cnn = db.engine.connect()
    print cnn.execute('select * from api_endpoints').fetchall()

    # print_table('api_endpoints')


def find_closest_tags(tags):
    c = conn.cursor()
    fuzzed_tags = {}
    choices = fetchall_to_list(c.execute('SELECT tag_name FROM TAGS'), 0)
    for i in tags:
        #Find the closest matching tag
        fuzz_possibilities = process.extractOne(i, choices)
        fuzzed = fuzz_possibilities[0]
        logger.debug("Initial Tag %s. fuzzed tag %s", i, fuzzed)
        fuzzed_tags[i] = fuzzed
    logger.debug("tags %s", tags)
    logger.debug("choices %s", choices)
    logger.debug("fuzzed is " + str(fuzzed_tags))
    return fuzzed_tags


def query_api(category, tags):
    '''Main public access point for the DB. Queries the database for all APIs that match the category and all of the tags. Returns a list of API urls.'''
    c = conn.cursor()
    placeholder = '?'  # For SQLite. See DBAPI paramstyle.
    placeholders = ', '.join(placeholder for unused in tags)

    # print "table"
    # print_table('api_providers')
    intersect_string = '''SELECT api_endpoints.api_url
                    FROM tagmap, api_endpoints, tags
                    WHERE tags.id = tagmap.tag_id
                    AND api_endpoints.category = (?)
                    AND (tags.tag_name IN (''' + placeholders + '''))
                    AND api_endpoints.id = tagmap.api_id
                    GROUP BY api_endpoints.id
                    HAVING COUNT( api_endpoints.id )=(?)'''  # This fun line of SQL translates into finding the APIs that match all the tags and the category
    logger.debug("query_strings is %s ", intersect_string)
    query_rows = c.execute(intersect_string, (category,) + tags + (len(tags),))
    filtered_rows = []

    for row in query_rows:
        filtered_rows.append([row[0]])
    logger.debug('''filtered_rows %s''', filtered_rows)
    return filtered_rows


# print query_api('weather', ('bullshit', 'temperature'))
