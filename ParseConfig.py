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

def get_reg_btn(lang, btn_name):
    """Return button text for registration"""

    return _get_text(lang, 'menus', 'reg_menu', btn_name)

def get_main_menu_btn(lang, btn_name):
    """Return button text for main menu"""

    return _get_text(lang, 'menus', 'main_menu', btn_name)

def get_conversations(lang, *args):
    """ Return dict with conversations messages according to language """

    return _get_text(lang, 'conversations', *args)

def _get_text(lang, *args):
    """Return text from config.json """

    lang = _format_lang(lang)
    if not lang in CONFIG['lang']:
        lang = 'en'

    text = CONFIG['lang'][lang]

    for arg in args:
        text = text[arg]

    return text

def _format_lang(lang):
    """Return formated lang """

    return lang.split('-')[0]
