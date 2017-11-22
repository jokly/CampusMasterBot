"""Parse config file"""

from os import environ

def get_env():
    """Return enviroment ['dev' or 'prod']"""

    return environ.get('ENV')

def get_token():
    """Return token"""

    return environ.get("TOKEN")

def get_db_config():
    """Return database connection config"""

    return {'dbname': environ.get('DB_NAME'), 'host': environ.get('DB_HOST'),
            'port': environ.get('DB_PORT'), 'user': environ.get('DB_USER'),
            'passwd': environ.get('DB_PASSWD')}
