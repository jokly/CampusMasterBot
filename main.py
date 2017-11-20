"""Main module"""

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ParseConfig

TOKEN = ParseConfig.get_token()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def echo(bot, update):
    update.message.reply_text(update.message.text)

def start(bot, update):
    """ /start command"""
    update.message.reply_text('Start bot!')

def help(bot, update):
    """ /help command"""
    update.message.reply_text('For start bot type /start')

def error(bot, update, error):
    """Logg error caused by updates"""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    """Start bot"""
    token = ParseConfig.get_token()
    updater = Updater(token)
    dpt = updater.dispatcher

    dpt.add_handler(CommandHandler('start', start))
    dpt.add_handler(CommandHandler('help', help))

    dpt.add_handler(MessageHandler(Filters.text, echo))

    dpt.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
