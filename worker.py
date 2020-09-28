#!/usr/bin/env python3
import os

from configparser import RawConfigParser
from pyzotero.zotero import Zotero

import abstrackr.generate_predictions
from zotero_sync import fetch, schema

config = RawConfigParser()
config.read(os.path.normpath(os.path.join(os.path.dirname(__file__), './config.txt')))

api_key = config.get('zotero', 'api_key')

# Flush schema cache :
#schema.from_zotero(flush = True, verbose = True)

engine = schema.entry(config.get('database', 'conn_string'), verbose = False)
fetch.from_zotero_group(engine, 88617)
fetch.from_all_by_key(engine, api_key)

#print("postgresql")
#abstrackr.generate_predictions.main('conn_string')
