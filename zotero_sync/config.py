
import os

from configparser import RawConfigParser

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
