import logging

from environs import env
from telegram import Update, ForceReply
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s- %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    "Start messaging bot"
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте")


def echo(update: Update, context: CallbackContext):
    "Func Echo return  user message"
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def main(token: str):
    """Main function running code"""
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()


if __name__ == "__main__":
    env.read_env()
    TELEGRAM_TOKEN = env("TELEGRAM_TOKEN")
    main(TELEGRAM_TOKEN)
