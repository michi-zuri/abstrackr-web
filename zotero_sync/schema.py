# https://www.python.org/dev/peps/pep-0263/ encoding: utf-8

import datetime, json, math, os

from configparser import RawConfigParser
from sqlalchemy import create_engine, func, text, Column, DateTime, Integer, MetaData, String, Table
import requests

config = RawConfigParser()
config.read(os.path.normpath(os.path.join(os.path.dirname(__file__), r'../config.txt')))

def check_schema() :
    schema_file = os.path.dirname(__file__)+'/schema.json'
    try :
        with open(schema_file, 'r') as file :
            schema = json.load(file)
    except :
        schema = {}
    headers = schema.get("headers",{})
    #disable caching for dev:
    headers = {}
    updated_schema = None
    response = requests.get("https://api.zotero.org/schema", headers=headers)
    print(response.status_code)
    if response.status_code == 200 :
        updated_schema = response.json()
        updated_schema['headers'] = {}
        updated_schema['headers']['Accept-Encoding'] = 'gzip'
        updated_schema['headers']['If-None-Match'] = response.headers['ETag']
        updated_schema['headers']['If-Modified-Since'] = response.headers['Last-Modified']
        unsorted_fields = {}
        for type in updated_schema['itemTypes'] :
            for field in type['fields'] :
                key = field.get('baseField',field['field'])
                if key=='accessDate' or key=='filingDate' or key=='date' :
                    unsorted_fields[key] = 'timestamp'
                else :
                    unsorted_fields[key] = 'varchar(32767)'
        sorted_fields = sorted(unsorted_fields.items())
        updated_schema['fields'] = dict(sorted_fields)
        with open(schema_file, 'w') as file:
            json.dump(updated_schema, file)
    if updated_schema :
        return updated_schema
    else :
        return schema

schema = check_schema()
print( "The Zotero schema was last modified %s""" % schema['headers']['If-Modified-Since'] )

def exists(engine, metadata, library_type_id):
    """ Prepare database to accomodate all possible fields for storage.
        Create, schema, tables and columns as needed
    """
    with engine.connect() as db:
        query = """
CREATE SCHEMA IF NOT EXISTS %s""" % library_type_id ;
        db.execute(text(query))
        query = """
CREATE TABLE IF NOT EXISTS %s.items ();""" % library_type_id
        db.execute(text(query))
        query = """
ALTER TABLE %s.items ADD COLUMN IF NOT EXISTS "%s" %s PRIMARY KEY;
        """ % (library_type_id, 'key', 'varchar(8)')
        db.execute(text(query))
        query = """
ALTER TABLE %s.items ADD COLUMN IF NOT EXISTS "%s" %s;
        """ % (library_type_id, 'version', 'integer')
        db.execute(text(query))
        query = """
ALTER TABLE %s.items ADD COLUMN IF NOT EXISTS "%s" %s;
        """ % (library_type_id, 'itemType', 'varchar(20)')
        db.execute(text(query))
        query = """
ALTER TABLE %s.items ADD COLUMN IF NOT EXISTS "%s" %s;
        """ % (library_type_id, 'dateAdded', 'timestamp with time zone')
        db.execute(text(query))
        query = """
ALTER TABLE %s.items ADD COLUMN IF NOT EXISTS "%s" %s;
        """ % (library_type_id, 'dateModified', 'timestamp with time zone')
        db.execute(text(query))
        foreign_columns = [ 'creators', 'tags', 'collections', 'relations' ]
        for field in foreign_columns :
            query = """
ALTER TABLE %s.items ADD COLUMN IF NOT EXISTS "%s" %s;
            """ % (library_type_id, field, 'varchar(32767)')
            db.execute(text(query))
        for field,type in schema['fields'].items() :
            query = """
ALTER TABLE %s.items ADD COLUMN IF NOT EXISTS "%s" %s;
            """ % (library_type_id, field, type)
            db.execute(text(query))


        query = """
CREATE SCHEMA IF NOT EXISTS zotero ;"""
        db.execute(text(query))
        query = """
CREATE TABLE IF NOT EXISTS zotero.sync_logs ();"""
        db.execute(text(query))
        query = """
ALTER TABLE zotero.sync_logs ADD COLUMN IF NOT EXISTS "%s" %s PRIMARY KEY;
        """ % ('id', 'integer DEFAULT nextval(\'zotero.sync_logs_id_seq\'::regclass)')
        db.execute(text(query))
        query = """
ALTER TABLE zotero.sync_logs ADD COLUMN IF NOT EXISTS "%s" %s ;
        """ % ('timestamp', 'timestamp with time zone DEFAULT now()')
        db.execute(text(query))
        query = """
ALTER TABLE zotero.sync_logs ADD COLUMN IF NOT EXISTS "%s" %s ;
        """ % ('version', 'integer')
        db.execute(text(query))
        query = """
ALTER TABLE zotero.sync_logs ADD COLUMN IF NOT EXISTS "%s" %s ;
        """ % ('library', 'varchar(15)')
        db.execute(text(query))
        query = """
ALTER TABLE zotero.sync_logs ADD COLUMN IF NOT EXISTS "%s" %s ;
        """ % ('name', 'varchar(255)')
        db.execute(text(query))
        query = """
ALTER TABLE zotero.sync_logs ADD COLUMN IF NOT EXISTS "%s" %s ;
        """ % ('duration', 'integer')
        db.execute(text(query))
'''
    t_syncs = Table("syncs", metadata,
        Column('id', Integer, primary_key=True),
        Column('timestamp', DateTime(True), server_default=func.now(), comment='Timestamp of this sync'),
        Column('version', Integer, comment='Last_modified_version of library used for syncing with Zotero API'),
        Column('library', String(15), comment='ID of library composed of prefix user or group and library number'),
        Column('name', String(255), comment='Name of library that was synced'),
        Column('duration', Integer, comment='How many seconds it took to sync with Zotero API'),
        schema='zotero'
    )

    metadata.create_all(engine)
'''

library_type_id="zot_t_testing"
# Database connection setup with sqlalchemy
engine = create_engine(config.get('database', 'conn_string'))
metadata = MetaData(engine, schema='library_type_id')
exists(engine, metadata, library_type_id)


'''
Column('pmid', Integer, comment='Pubmed identifier'),
Column('eid', Integer, comment='Scopus electronic identifier: the prefix `2-s2.0-` is omitted'),
Column('keywords', String(1000), comment='keywords suggested by the author(s)'),
Column('CAS', String(1000), comment='Chemical Abstracts Service identifier for chemical substances, as indexed by Scopus'),
Column('MeSH', String(1000), comment='Medical Subject Headings indexed by MEDLINE'),
Column('EMTREE', String(1000), comment='EMTREE indexed by EMBASE'),
'''
