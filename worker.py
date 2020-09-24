#!/usr/bin/env python3
import os

from configparser import RawConfigParser
from pyzotero.zotero import Zotero

import abstrackr.generate_predictions
import zotero_sync.fetch as fetch

config = RawConfigParser()
config.read(os.path.normpath(os.path.join(os.path.dirname(__file__), r'./config.txt')))

api_key = config.get('zotero', 'api_key')

fetch.from_all_by_key(api_key)

#print("postgresql")
#abstrackr.generate_predictions.main('conn_string')
