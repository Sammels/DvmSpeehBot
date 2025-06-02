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
from logs import TelegramLogsHandler
from diagflow_script import detect_intent_text


logger = logging.getLogger("tg_bot")


def start(update: Update, context: CallbackContext):
    """Start messaging bot"""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте")


def response_message(update: Update, context: CallbackContext):
    """Func return  user message."""
    project_id = GOOGLE_PROJECT_ID
    session_id = "test-sess"
    language_code = GOOGLE_LANGUAGE_CODE

    text_update = detect_intent_text(
        project_id, session_id, update.message.text, language_code
    )

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=text_update[0].encode().decode()
    )


def main(token: str):
    """Main function running code."""

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s- %(message)s", level=logging.INFO
    )
    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(TELEGRAM_LOGGER, TELEGRAM_LOGER_CHAT_ID))
    logger.info("Bot start")
    try:
        updater = Updater(token=TELEGRAM_TOKEN)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(
            MessageHandler(Filters.text & (~Filters.command), response_message)
        )

        updater.start_polling()
        updater.idle()
    except Exception as err:
        logging.error(err, exc_info=True)


if __name__ == "__main__":
    env.read_env()
    TELEGRAM_TOKEN = env("TELEGRAM_TOKEN")
    TELEGRAM_LOGGER = env("TG_BOT_LOGGER_TOKEN")
    TELEGRAM_LOGER_CHAT_ID = env("TG_CHAT_ID")
    GOOGLE_PROJECT_ID = env("PROJECT_ID")
    GOOGLE_LANGUAGE_CODE = env("LANGUAGE_CODE")

    main(TELEGRAM_TOKEN)
