#!/usr/bin/env python3

import os

from configparser import RawConfigParser

import abstrackr.generate_predictions
from zotero_sync import fetch, schema

def read():
    config = RawConfigParser()
    config.read('./config.txt')

    try:
        api_key = config.get('zotero', 'api_key')
    except Exception as e :
        api_key = None
        print("Could not set optional api_key from ./config.txt")
    try:
        conn_string = config.get('database', 'conn_string')
    except Exception as e :
        print("""Could not find this in ./config.txt :

        [database]
        conn_string=postgresql://etc """)
        exit(1)

    return conn_string, api_key

conn_string, api_key = read()

# Uncomment the following line to flush the schema cache :
#schema.from_zotero(flush = True, verbose = True)
engine = schema.entry(conn_string, verbose = False)
#fetch.from_all_by_key(engine, api_key)
fetch.from_zotero_group(engine, 2582275)

#print("Starting Abstrackr sorting algorithm")
#abstrackr.generate_predictions.main(conn_string, 'zot_g_2543222')
