"""Module for working with database"""

import logging
from enum import Enum
import pg
import ParseConfig

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

DB_CONFIG = ParseConfig.get_db_config()
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
        PDB.get('users', user)

        if user['room'] is None:
            return RegStatus.NO_ROOM

        return RegStatus.COMPLETE

    except pg.DatabaseError:
        return RegStatus.NO_PHONE

def reg_user(user_chat_id, telephone_number):
    """Add user chat_id with phone"""

    PDB.insert('users', chat_id=user_chat_id, telephone_number=telephone_number)

def update_room(user_chat_id, room):
    """Update user room"""

    LOGGER.info('Try update room: {0} | {1}'.format(user_chat_id, room))

    if len(room) != 4 or not str.isdigit(room):
        return False

    PDB.update('users', PDB.get('users', dict(chat_id=user_chat_id)), room=room)

    LOGGER.info('Update room: {0} | {1}'.format(user_chat_id, room))

    return True

def add_complaint(user_chat_id, text):
    """Add user complaint"""

    PDB.insert('complaints', chat_id=user_chat_id, text=text)
