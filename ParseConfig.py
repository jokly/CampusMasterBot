"""Parse config file"""

from os import environ
import json

CONFIG = json.load(open('config.json'))

def get_env():
    """Return enviroment ['dev' or 'prod']"""

    return environ.get('ENV')

def get_token():
    """Return token"""

    return environ.get("TOKEN")

def get_url():
    """Return application url"""

    return environ.get("URL")

def get_db_config():
    """Return database connection config"""

    return {'dbname': environ.get('DB_NAME'), 'host': environ.get('DB_HOST'),
            'port': environ.get('DB_PORT'), 'user': environ.get('DB_USER'),
            'passwd': environ.get('DB_PASSWD')}

def get_reg_btns():
    """Return dict with buttons text for registration"""

    return CONFIG['menus']['reg_menu']

def get_main_menu_btns():
    """Return dict with buttons text for main menu"""

    return CONFIG['menus']['main_menu']
