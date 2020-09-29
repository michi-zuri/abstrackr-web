#!/usr/bin/env python3

import abstrackr.generate_predictions
from zotero_sync import fetch, schema, config

api_key, conn_string = config.read()

# Flush schema cache :
#schema.from_zotero(flush = True, verbose = True)
#engine = schema.entry(config.get('database', 'conn_string'), verbose = False)
#fetch.from_all_by_key(engine, api_key)

print("Starting Abstrackr sorting algorithm")
#abstrackr.generate_predictions.main(conn_string, 'zot_g_2543222')
