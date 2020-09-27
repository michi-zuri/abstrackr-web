# https://www.python.org/dev/peps/pep-0263/ encoding: utf-8

import datetime, json, math, os

from configparser import RawConfigParser
from sqlalchemy import func, text, Column, DateTime, Integer, String, Table

config = RawConfigParser()
config.read(os.path.normpath(os.path.join(os.path.dirname(__file__), r'../config.txt')))




def exists(engine, metadata, library_type_id):
    """ Prepare database to accomodate all possible fields for storage.
        Create, schema, tables and columns as needed
    """
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
