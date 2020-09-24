# https://www.python.org/dev/peps/pep-0263/ encoding: utf-8

import datetime, json, math, os
import json

from configparser import RawConfigParser
# for regular SQL execution
from sqlalchemy import create_engine, pool, text, MetaData
# for setting up db schema
from sqlalchemy import func, Column, DateTime, Integer, String, Table
from pyzotero.zotero import Zotero

config = RawConfigParser()
config.read(os.path.normpath(os.path.join(os.path.dirname(__file__), r'../config.txt')))

def response_headers(Z):
    """ Get the response headers of the last made request
    """
    return Z.request.headers

def _fetch_key_info(api_key):
    z = Zotero('AnyLibrary', 'AnyType', api_key)
    key_info = z.key_info()
    return key_info

def _inspect_api_key(api_key, key_info = None):
    if not key_info :
        key_info = _fetch_key_info(api_key)
    z = Zotero(key_info['userID'], 'user', api_key)
    groups = z.groups()
    return (groups, key_info)

def _duration(start_time) :
    return (datetime.datetime.now(datetime.timezone.utc)-start_time).total_seconds()

def _start_duration() :
    return datetime.datetime.now(datetime.timezone.utc)

def _ensure_schema_exists(engine, metadata, library_type_id):
    with engine.connect() as db:
        query = "CREATE SCHEMA IF NOT EXISTS %s" % library_type_id ;
        db.execute(text(query))
        query = "CREATE SCHEMA IF NOT EXISTS zotero ;"
        db.execute(text(query))

    t_references = Table("references", metadata,
        Column('id', Integer, primary_key=True),
        Column('key', String(8), unique=True, comment='Zotero API item identifier'),
        Column('version', Integer, comment='Version used for syncing with Zotero API'),
        Column('pmid', Integer, comment='Pubmed identifier'),
        Column('eid', Integer, comment='Scopus electronic identifier: the prefix `2-s2.0-` is omitted'),
        Column('doi', String(50), comment='digital object identifier'),
        Column('title', String(1000), comment='title of journal article, book, conference, etc.'),
        Column('abstract', String(20000), comment=''),
        Column('authors', String(1000), comment=''),
        Column('journal', String(1000), comment='Name of the journal that the reference was published in'),
        Column('publication_date', String(50), comment='Zotero stores publication dates as plain text'),
        Column('keywords', String(1000), comment='keywords suggested by the author(s)'),
        Column('CAS', String(1000), comment='Chemical Abstracts Service identifier for chemical substances, as indexed by Scopus'),
        Column('MeSH', String(1000), comment='Medical Subject Headings indexed by MEDLINE'),
        Column('EMTREE', String(1000), comment='EMTREE indexed by EMBASE'),
        schema=library_type_id
    )

    t_syncs = Table("syncs", metadata,
        Column('id', Integer, primary_key=True),
        Column('timestamp', DateTime(True), server_default=func.now(), comment='Timestamp of this sync'),
        Column('version', Integer, comment='Last_modified_version of library used for syncing with Zotero API'),
        Column('library', String(15), comment='ID of library composed of prefix user or group and library number'),
        Column('name', String(127), comment='Name of library that was synced'),
        Column('duration', Integer, comment='How many seconds it took to sync with Zotero API'),
        schema='zotero'
    )

    metadata.create_all(engine)

def from_zotero_user(user_id = None, api_key = None, key_info = None, db_key = 'conn_string') :
    if not user_id and not api_key :
        return "no idea how I should know which user library to sync, neither api_key, nor userID was provided."
    elif api_key :
        if not key_info :
            key_info = _get_key_info(api_key)
        # this overrides user if given as argument:
        user_id = key_info['userID']
        name = "%s's user library" % key_info['username']
        if not 'user' in key_info['access'] :
            return "no read access to user library: ", key_info['access']
    else :
        print("Warning: fetching user library without API key. How to check?")
        # todo: check access and abort if 403 access denied
        name = "user library %s" % user_id
    return from_zotero_library(user_id, 'user', name, api_key, db_key)

def from_zotero_group(group, api_key = None, key_info = None, db_key = 'conn_string'):
    return from_zotero_library(group['id'], 'group', group['data']['name'], api_key, db_key)

def from_zotero_library(library_id, library_type, library_name, api_key = None, db_key = 'conn_string'):
    library_type_id = "zot_"+library_type[:1]+"_"+str(library_id)
    print(library_type_id)

    # Database connection setup with sqlalchemy
    engine = create_engine(config.get('database', db_key))
    metadata = MetaData(engine, schema=library_type_id)

    # Every library gets a separate schema within the database
    _ensure_schema_exists(engine, metadata, library_type_id)

    # Setup the Zotero connection through pyzotero
    z = Zotero(str(library_id), library_type, api_key)

    # Start the engine and fetch items from the cloud!
    with engine.connect() as db:
        # Start sync timer and log attempt to sync.
        # Duration and latest version will be updated when finished.
        query = """
        INSERT INTO zotero.syncs (timestamp, library, name)
        VALUES ( DEFAULT, :lib, :name) RETURNING id,timestamp;
        """
        sync = db.execute(text(query), lib=library_type_id, name=library_name).fetchone() # ( Int, datetime )
        print("Sync #%i was started at %s" % (sync[0], sync[1].strftime('%c')) )

        # Get current local library version
        query = """
        SELECT version FROM zotero.syncs WHERE library='%s' AND duration IS NOT NULL ORDER BY version DESC LIMIT 1;
        """ % library_type_id
        res_last_sync_version = db.execute(text(query)).fetchone() # ( Int, ) or None
        if res_last_sync_version :
            last_sync_version = res_last_sync_version[0]
            query = """
            SELECT COUNT(*) FROM %s.references ;
            """ % library_type_id
            local_count = db.execute(text(query)).fetchone() # ( Int, ) or None
            print("local mirror is at version %i and contains %i items" % (last_sync_version, local_count[0] ))
        else :
            last_sync_version = 0
            print("Starting initial sync of library %s" % library_type_id)

        # Get current remote library count and version
        z.top(limit=1, format='keys')
        remote_count    = int(z.request.headers.get('total-results', 0))
        library_version = int(z.request.headers.get('last-modified-version', 0))
        print("remote cloud is at version %i and contains %i items" % (library_version , remote_count))

        if last_sync_version < library_version :
            # Get list of local item keys and their versions
            query = """
            SELECT key,version FROM %s.references ;
            """ % library_type_id
            local_versions = dict(db.execute(text(query)).fetchall()) # { String: Int, }

            def _fetch_updates_and_inserts( start = 0) :
                start_round = _start_duration()
                inserts = 0
                update_list = z.top(limit=100, start=start, format='json', since=last_sync_version)
                # Maybe there are only deletions to handle, so checking number of updates to handle
                if len(update_list) > 0 :
                    for item in update_list :
                        if item['key'] in local_versions :
                            query = """
                            UPDATE %s.references
                            SET version=:version, title=:title
                            WHERE key=:key ;
                            """ % library_type_id
                            db.execute(text(query), version=item["version"], title=item["data"]["title"], key=item["key"] )
                        else :
                            query = """
                            INSERT INTO %s.references (key, version, title)
                            VALUES ( :key, :version, :title) ;
                            """ % library_type_id
                            db.execute(text(query),  key=item["key"], version=item["version"], title=item["data"]["title"] )
                            inserts += 1
                    round_duration = _duration(start_round)
                    print( "Finished processing %i updates in %s seconds." % (len(update_list), str(round_duration)) )
                    if len(update_list) == 100 :
                        # fetch more updates. There is a 1% chance that this will be in vain.
                        print( "Fetching more updates now." )
                        _fetch_updates_and_inserts(start=start+100)
                    else :
                        print( "All updates processed." )
                else :
                    round_duration = _duration(start_round)
                    print( "Zero updates to process (it took %s seconds to figure that out)" % str(round_duration) )

            # fetch all updates in batches of 100 (includes updates to existing items and new items)
            _fetch_updates_and_inserts()

            # if this is not the initial sync, there's nothing to delete...
            if last_sync_version > 0:
                start_round = _start_duration()
                print( "Fetching list of deletions since last successful sync." )
                # Get list of deleted items from cloud
                delete_list = z.deleted(limit=None, format='versions', since=last_sync_version)
                if len(delete_list['items']) > 0:
                    for item in delete_list['items'] :
                        if item in local_versions:
                            query = """
                            DELETE FROM %s.references WHERE key=:key ;
                            """ % library_type_id
                            db.execute(text(query), key=item)
                        else:
                            print("Tried to DELETE item with key %s, but this item is not in local library..." % item )
                round_duration = _duration(start_round)
                print("Finished processing %i deletions in %s seconds" % ( len(delete_list['items']), str(round_duration) ) )
            else :
                print("Initial sync has been successful. Next time atomic updates will be performed!")
        else :
            print("Nothing to sync, everything is up to date.")

        duration = _duration(sync[1])
        query = """
        UPDATE zotero.syncs
        SET duration=:duration, version=:version
        WHERE id=:id ;
        """
        db.execute(text(query), duration=math.ceil(duration), version=library_version, id=sync[0])
        # Closing connection to database ༺ with engine.connect() as db : ༻
    return "Syncing library %s took %s seconds\n" % (library_type_id, str(duration))

def from_all_by_key(api_key, only_groups = False):
    groups, key_info = _inspect_api_key(api_key)
    if not only_groups and 'user' in key_info['access']:
        print(from_zotero_user(key_info['userID'], api_key, key_info))
    for group in groups:
        if not 'groups' in key_info['access'] :
            return "no groups to sync in this API key starting with %s" % api_key[:4]
        if str(group['id']) in key_info['access']['groups']:
            print(from_zotero_group(group, api_key))
