from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from local_settings import TELE_TOKEN
from database import db_session, User, Company, Agreements


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def echo(bot, update):
    """Echo the user message."""
    bot.send_message(chat_id=update.channel_post['chat']['id'], text='Test from bot')
    if 'register me' in update.channel_post.text:
        # logger.info('1')
        with open('registred_users.csv', 'w') as f:
            # logger.info('2')
            f.write(str(update.channel_post['chat']['id']))
            # logger.info('3')

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def clients(bot, update):
    msg_clients = []
    clients_list = db_session.query(Company.company_name).order_by(Company.company_name).all()
    for client in clients_list:
        msg_clients.append(client.company_name)
    update.message.reply_text('\n'.join(msg_clients))


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TELE_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("clients", clients))
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
    # import telegram
    # bot = telegram.Bot('536269409:AAG9L47EFdLcpGJMLcNDwzpWep6fMgqiAB8')
    # bot.send_message(chat_id=-1001305314053, text='Test from bot')