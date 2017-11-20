"""Main module"""

import logging
from pg import DB

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import ParseConfig

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = ParseConfig.get_token()
DB_CONFIG = ParseConfig.get_db_config()

PDB = DB(dbname=DB_CONFIG['dbname'], host=DB_CONFIG['host'], port=DB_CONFIG['port'],\
         user=DB_CONFIG['user'], passwd=DB_CONFIG['passwd'])

PHONE, ROOM = range(2)

def start(bot, update):
    """ /start command"""

    phone_btn = KeyboardButton(text="Отправить номер", request_contact=True)
    keyboard = ReplyKeyboardMarkup([[phone_btn]], one_time_keyboard=True)

    update.message.reply_text('Привет! Мне нужен твой номер телеофна.',
                              reply_markup=keyboard)

    return PHONE

def phone(bot, update):
    chat_id = update.message.chat_id
    phone_number = update.message.contact.phone_number
    logger.info(str(chat_id) + ' : ' + str(phone_number))

    return ConversationHandler.END

def cancel(bot, update):
    user = update.message.from_user
    logger.info("Пользователь %s закончил диалог", user.first_name)
    update.message.reply_text('Пока :)',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def error(bot, update, error):
    """Logg error caused by updates"""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    """Start bot"""
    token = ParseConfig.get_token()
    updater = Updater(token)
    dpt = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            PHONE: [MessageHandler(Filters.contact, phone)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dpt.add_handler(conv_handler)

    dpt.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
