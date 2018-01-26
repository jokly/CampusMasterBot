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
            'passwd': environ.get('DB_PASSWD'), 'tables':
                {'users': CONFIG['tables']['users'], 'complaints': CONFIG['tables']['complaints'],
                 'status': CONFIG['tables']['status']}
           }

def get_reg_btns(lang):
    """Return dict with buttons text for registration"""

    lang = format_lang(lang)
    return CONFIG['lang'][lang]['menus']['reg_menu']

def get_main_menu_btns(lang):
    """Return dict with buttons text for main menu"""

    lang = format_lang(lang)
    return CONFIG['lang'][lang]['menus']['main_menu']

def get_conversations(lang, *args):
    """ Return dict with conversations messages according to language """

    lang = format_lang(lang)
    r = CONFIG['lang'][lang]['conversations']

    for e in args:
        r = r[e]

    return r

def format_lang(lang):
    """ """

    return lang.split('-')[0]
