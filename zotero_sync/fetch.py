# https://www.python.org/dev/peps/pep-0263/ encoding: utf-8

import datetime, json, math, os, json

from configparser import RawConfigParser
from sqlalchemy import create_engine, text, MetaData
from pyzotero.zotero import Zotero

from . import schema as ensure_schema

config = RawConfigParser()
config.read(os.path.normpath(os.path.join(os.path.dirname(__file__), r'../config.txt')))

def _fetch_key_info(api_key):
    z = Zotero('AnyLibrary', 'AnyType', api_key)
    key_info = z.key_info(limit=0)
    return key_info

def _duration(start_time) :
    return (datetime.datetime.now(datetime.timezone.utc)-start_time).total_seconds()

def _start_duration() :
    return datetime.datetime.now(datetime.timezone.utc)

def from_zotero_user(user_id, api_key = None, key_info = None, db_key = 'conn_string') :
    from_zotero_library(user_id, 'user', api_key, key_info, db_key)

def from_zotero_group(group_id, api_key = None, key_info = None, db_key = 'conn_string'):
    from_zotero_library(group_id, 'group', api_key, key_info, db_key)

def from_zotero_library(library_id, library_type, api_key = None, key_info = None, db_key = 'conn_string'):
    skip = False
    if not library_type[:1] == 'u' and not library_type[:1] == 'g' :
        print("invalid library_type %s" % library_type)
        skip = True
    if library_id > 999999999 :
        print("invalid group id %i" % library_id)
        skip = True
    if skip :
        print("Skipping library of type %s with id %i ¶\n" % (library_type, library_id))
        return
    try:
        _from_zotero_library(library_id, library_type, api_key, db_key)
    except Exception as e:
        library_type_id = "%s_%s_%i" % (str(e)[7:10], library_type[:1], library_id)
        print("\n%s ¶" % library_type_id)
        engine = create_engine(config.get('database', db_key))
        metadata = MetaData(engine)
        with engine.connect() as db:
            query = """
            INSERT INTO zotero.syncs (timestamp, library)
            VALUES ( DEFAULT, :lib) RETURNING id,timestamp;
            """
            sync = db.execute(text(query), lib=library_type_id).fetchone() # ( Int, datetime )
            print("Sync #%i was aborted at %s" % (sync[0], sync[1].strftime('%c')) )

def _from_zotero_library(library_id, library_type, api_key = None, db_key = 'conn_string'):
    library_type_id = "zot_%s_%i" % (library_type[:1], library_id)

    # Database connection setup with sqlalchemy
    engine = create_engine(config.get('database', db_key))
    metadata = MetaData(engine, schema=library_type_id)

    # Every library gets a separate schema within the database
    ensure_schema.exists(engine, metadata, library_type_id)

    # Setup the Zotero connection through pyzotero
    z = Zotero(library_id, library_type, api_key)
    check_access = z.items(limit=1, format="json")
    library_name = check_access[0]['library']['name']

    print("\n%s %s ¶" % (library_type_id, library_name))

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
    try:
        _from_all_by_key(api_key, only_groups)
    except Exception as e:
        print("\ninvalid API key starting with %s ¶" % api_key[:3])

def _from_all_by_key(api_key, only_groups = False):
    key_info = _fetch_key_info(api_key)
    if 'user' in key_info['access'] and not only_groups :
        from_zotero_user(key_info['userID'], api_key, key_info)
    else :
        return "not syncing user library for API key starting with %s" % api_key[:4]

    if 'groups' in key_info['access']:
        for group in key_info['access']['groups'] :
            from_zotero_group(int(group), api_key, key_info)
    else :
        return "no groups to sync in this API key starting with %s" % api_key[:4]
