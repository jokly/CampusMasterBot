"""Module for working with database"""

import logging
from enum import Enum
from datetime import datetime
import pg
import ParseConfig

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

DB_CONFIG = ParseConfig.get_db_config()
USERS_TABLE = DB_CONFIG['tables']['users']
COMPLAINTS_TABLE = DB_CONFIG['tables']['complaints']
STATUS_TABLE = DB_CONFIG['tables']['status']

PDB = pg.DB(dbname=DB_CONFIG['dbname'], host=DB_CONFIG['host'], port=int(DB_CONFIG['port']),\
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
        PDB.get(USERS_TABLE, user)

        if user['room'] is None:
            return RegStatus.NO_ROOM

        return RegStatus.COMPLETE

    except pg.DatabaseError:
        return RegStatus.NO_PHONE

def reg_user(user_chat_id, telephone_number):
    """Add user chat_id with phone"""

    PDB.insert(USERS_TABLE, chat_id=user_chat_id, telephone_number=telephone_number)

def update_room(user_chat_id, room):
    """Update user room"""

    LOGGER.info('Try update room: {0} | {1}'.format(user_chat_id, room))

    if len(room) != 5 or not str.isdigit(room):
        return False

    PDB.update(USERS_TABLE, PDB.get(USERS_TABLE, dict(chat_id=user_chat_id)), room=room)

    LOGGER.info('Update room: {0} | {1}'.format(user_chat_id, room))

    return True

def add_complaint(user_chat_id, text):
    """Add user complaint"""

    PDB.insert(COMPLAINTS_TABLE, chat_id=user_chat_id, text=text)

def get_room(user_chat_id):
    """Returns user room"""

    user = dict(chat_id=user_chat_id)
    PDB.get(USERS_TABLE, user)

    return user['room']

def change_room_status(room, text):
    """Change room status"""

    status = dict(room=room)

    try:
        PDB.get(STATUS_TABLE, status)
        PDB.update(STATUS_TABLE, status, timestamp=datetime.now(),  text=text)

    except pg.DatabaseError:
        PDB.insert(STATUS_TABLE, room=room, timestamp=datetime.now(), text=text)
