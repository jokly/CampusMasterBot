"""Main module"""

import logging
import os
import re

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, ChatAction)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)

import ParseConfig
from DBWorker import RegStatus
import DBWorker

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

REG_BTNS = ParseConfig.get_reg_btns()
PHONE, ROOM = range(2)

MAIN_MENU_BTNS = ParseConfig.get_main_menu_btns()
MAIN_MENU, UPDATE_ROOM, COMPLAINT, CHANGE_STATUS = range(4)

def start(bot, update):
    """/start command"""

    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

    reg_status = DBWorker.get_reg_status(update.message.chat_id)

    if reg_status == RegStatus.NO_ROOM:
        update.message.reply_text('У меня уже есть твой мобильный.' +
                                  'Теперь тебе надо ввести номер своей комнаты.')

        return ROOM
    elif reg_status == RegStatus.COMPLETE:
        update.message.reply_text('Ты уже зарегестрирован ;) Для начала введи /main')

        return ConversationHandler.END

    phone_btn = KeyboardButton(text=REG_BTNS['share_phone_number'], request_contact=True)
    keyboard = ReplyKeyboardMarkup([[phone_btn]], one_time_keyboard=True)

    update.message.reply_text('Привет! Мне нужен твой номер телефона :)',
                              reply_markup=keyboard)

    return PHONE

def phone(bot, update):
    """Get user phone"""

    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

    chat_id = update.message.chat_id
    phone_number = update.message.contact.phone_number

    LOGGER.info('New user: ' + str(chat_id) + ' | ' + str(phone_number))

    phone_number = re.sub('[()+-]', '', phone_number)

    DBWorker.reg_user(chat_id, phone_number)

    LOGGER.info('User was registered: ' + str(chat_id) + ' | ' + str(phone_number))

    update.message.reply_text('Теперь введи номер своей комнаты. Он должен состоять из 5-ти цифр.',
                              reply_markup=ReplyKeyboardRemove())

    return ROOM

def room(bot, update):
    """Register user room"""

    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

    if not DBWorker.update_room(update.message.chat_id, update.message.text):
        update.message.reply_text('Некоректный номер комнаты. Попробуй еще раз :)')
        return ROOM

    update.message.reply_text('Спасибо! Введи /main, чтобы увидеть на что я способен.')

    return ConversationHandler.END

def main_menu(bot, update):
    """Show main menu"""

    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

    if DBWorker.get_reg_status(update.message.chat_id) != RegStatus.COMPLETE:
        update.message.reply_text('Вы заполнили не все данные о себе. '
                                  'Введи /start для регистрации.')

        return ConversationHandler.END

    change_room_btn = KeyboardButton(text=MAIN_MENU_BTNS['change_room'])
    send_complaint_btn = KeyboardButton(text=MAIN_MENU_BTNS['send_complaint'])
    change_status_btn = KeyboardButton(text=MAIN_MENU_BTNS['change_status'])

    keyboard = ReplyKeyboardMarkup([[change_room_btn, send_complaint_btn], [change_status_btn]],
                                   one_time_keyboard=True)

    update.message.reply_text('Главное меню',
                              reply_markup=keyboard)

    return MAIN_MENU

def main_menu_handler(bot, update):
    """Main menu buttons handler"""

    cmd = update.message.text

    if cmd == MAIN_MENU_BTNS['change_room']:
        update.message.reply_text('Введите новый номер комнаты. Он должен состоять из 5-ти цифр.')
        return ROOM
    elif cmd == MAIN_MENU_BTNS['send_complaint']:
        update.message.reply_text('Введите свою жалобу.')
        return COMPLAINT
    elif cmd == MAIN_MENU_BTNS['change_status']:
        update.message.reply_text('Введите статус своей комнаты.')
        return CHANGE_STATUS

def main_menu_update_room(bot, update):
    """Update room number from main menu"""

    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

    if not DBWorker.update_room(update.message.chat_id, update.message.text):
        update.message.reply_text('Некоректный номер комнаты. Попробуй еще раз :)')
        return UPDATE_ROOM

    update.message.reply_text('Комната успешно изменена.')

    return MAIN_MENU

def add_complaint(bot, update):
    """Add complaint"""

    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

    DBWorker.add_complaint(update.message.chat_id, update.message.text)
    update.message.reply_text('Спасибо. Мы попытаемся решить вашу проблему :)')

    return MAIN_MENU

def change_room_status(bot, update):
    """Change room status"""

    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    DBWorker.change_room_status(DBWorker.get_room(update.message.chat_id), update.message.text)
    update.message.reply_text('Статус успешно изменен.')

    return MAIN_MENU

def help(bot, update):
    """Show help information"""

    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

    update.message.reply_text('Для регистрации или ее продолжения введите - /start. \n' +
                              'Для вывода главного меню введите - /main.')

def error(bot, update, error_msg):
    """Logg error caused by updates"""

    LOGGER.warning('Update "%s" caused error "%s"', update, error_msg)

def main():
    """Start bot"""

    token = ParseConfig.get_token()
    port = int(os.environ.get('PORT', '5000'))
    updater = Updater(token)
    dpt = updater.dispatcher

    reg_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            PHONE: [MessageHandler(Filters.contact, phone)],
            ROOM: [MessageHandler(Filters.text, room)]
        },

        fallbacks=[CommandHandler('start', start)]
    )

    main_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('main', main_menu)],

        states={
            MAIN_MENU: [MessageHandler(Filters.text, main_menu_handler)],
            UPDATE_ROOM: [MessageHandler(Filters.text, main_menu_update_room)],
            COMPLAINT: [MessageHandler(Filters.text, add_complaint)],
            CHANGE_STATUS: [MessageHandler(Filters.text, change_room_status)]
        },

        fallbacks=[CommandHandler('main', main_menu)]
    )

    dpt.add_handler(reg_conv_handler)
    dpt.add_handler(main_conv_handler)
    dpt.add_handler(CommandHandler('help', help))

    dpt.add_error_handler(error)

    env = ParseConfig.get_env()
    if env == 'prod':
        LOGGER.info('------Production environment------')
        updater.start_webhook(listen="0.0.0.0", port=port, url_path=token)
        updater.bot.set_webhook('https://' + ParseConfig.get_url() + '.herokuapp.com/' + token)
    elif env == 'dev':
        LOGGER.info('------Development environment------')
        updater.start_polling()
    else:
        LOGGER.info('------Unkonwn environment------')

    updater.idle()

if __name__ == '__main__':
    main()
