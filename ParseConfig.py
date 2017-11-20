"""Parse config file"""

import json

DATA = json.load(open('config.json'))

def get_token():
    """Return token"""

    return DATA['token']

def get_db_config():
    """Return database connection config"""
    
    return DATA['db']
