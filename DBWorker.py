from pg import DB, DatabaseError
from enum import Enum
from pprint import pprint

import ParseConfig

DB_CONFIG = ParseConfig.get_db_config()
PDB = DB(dbname=DB_CONFIG['dbname'], host=DB_CONFIG['host'], port=DB_CONFIG['port'],\
         user=DB_CONFIG['user'], passwd=DB_CONFIG['passwd'])

class RegStatus(Enum):
    NO_PHONE = 1
    NO_ROOM = 2
    COMPLETE = 3

def get_reg_status(user_chat_id):
    user = dict(chat_id=user_chat_id)

    try:
        PDB.get('users', user)

        if user['room'] is None:
            return RegStatus.NO_ROOM

        return RegStatus.COMPLETE

    except DatabaseError:
        return RegStatus.NO_PHONE

def reg_user(user_chat_id, telephone_number):
    PDB.insert('users', chat_id=user_chat_id, telephone_number=telephone_number)

def update_room(user_chat_id, room):
    pass
