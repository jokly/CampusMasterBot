"""Main module"""

import logging
import os

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)

import ParseConfig
from DBWorker import RegStatus
import DBWorker

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

PHONE, ROOM = range(2)

def start(bot, update):
    """ /start command"""

    if DBWorker.get_reg_status(update.message.chat_id) != RegStatus.NO_PHONE:
        update.message.reply_text('У меня уже есть твой мобильный :)')
        return ConversationHandler.END

    phone_btn = KeyboardButton(text="Отправить номер", request_contact=True)
    keyboard = ReplyKeyboardMarkup([[phone_btn]], one_time_keyboard=True)

    update.message.reply_text('Привет! Мне нужен твой номер телеофна.',
                              reply_markup=keyboard)

    return PHONE

def phone(bot, update):
    chat_id = update.message.chat_id
    phone_number = update.message.contact.phone_number

    DBWorker.reg_user(chat_id, phone_number)

    LOGGER.info(str(chat_id) + ' : ' + str(phone_number))

    update.message.reply_text('Ты успешно зарегестрирован!', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def cancel(bot, update):
    user = update.message.from_user
    LOGGER.info("Пользователь %s закончил диалог", user.first_name)
    update.message.reply_text('Пока :)',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def error(bot, update, error):
    """Logg error caused by updates"""
    LOGGER.warning('Update "%s" caused error "%s"', update, error)

def main():
    """Start bot"""
    token = ParseConfig.get_token()
    port = int(os.environ.get('PORT', '5000'))
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

    updater.start_webhook(listen="0.0.0.0", port=port, url_path=token)
    updater.bot.set_webhook("https://master-campus-bot.herokuapp.com/" + token)

    updater.idle()

if __name__ == '__main__':
    main()
