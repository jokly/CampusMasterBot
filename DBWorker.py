"""Module for working with database"""

from enum import Enum
from pg import DB, DatabaseError
import ParseConfig

DB_CONFIG = ParseConfig.get_db_config()
PDB = DB(dbname=DB_CONFIG['dbname'], host=DB_CONFIG['host'], port=int(DB_CONFIG['port']),\
         user=DB_CONFIG['user'], passwd=DB_CONFIG['passwd'])

class RegStatus(Enum):
    """Registration status"""

    NO_PHONE = 1
    NO_ROOM = 2
    COMPLETE = 3

def get_reg_status(user_chat_id):
    """Registration user status"""

    user = dict(chat_id=user_chat_id)

    try:
        PDB.get('users', user)

        if user['room'] is None:
            return RegStatus.NO_ROOM

        return RegStatus.COMPLETE

    except DatabaseError:
        return RegStatus.NO_PHONE

def reg_user(user_chat_id, telephone_number):
    """Add user chat_id with phone"""

    PDB.insert('users', chat_id=user_chat_id, telephone_number=telephone_number)

def update_room(user_chat_id, room):
    """Update user room"""
    PDB.update('users', PDB.get('users', dict(chat_id=user_chat_id)), room=room)
