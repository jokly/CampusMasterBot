"""Parse config file"""

import json

DATA = json.load(open('config.json'))

def get_token():
    """Return token"""

    return DATA["token"]
