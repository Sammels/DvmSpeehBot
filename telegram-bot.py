import logging

from environs import env
from functools import partial
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


def response_message(
    update: Update, context: CallbackContext, project_id, language_code
):
    """Func return  user message."""
    chat_id = update.message.chat_id

    text_update = detect_intent_text(
        project_id=project_id,
        session_id=f"tg-{chat_id}",
        text=update.message.text,
        language_code=language_code,
    )

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=text_update[0].encode().decode()
    )


def main():
    """Main function running code."""

    env.read_env()
    telegramm_token = env("TELEGRAM_TOKEN")
    telegram_logger = env("TG_BOT_LOGGER_TOKEN")
    telegram_logger_chat_id = env("TG_CHAT_ID")
    project_id = env("PROJECT_ID")
    language_code = env("LANGUAGE_CODE")
    

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s- %(message)s", level=logging.INFO
    )
    logger.setLevel(logging.DEBUG)
    logger.addHandler(
        TelegramLogsHandler(
            telegram_logger, telegram_logger_chat_id
        )
    )

    logger.info("Bot start")
    try:
        updater = Updater(token=telegramm_token)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(
            MessageHandler(
                Filters.text & ~Filters.command,
                partial(
                    response_message,
                    project_id=project_id,
                    language_code=language_code,
                ),
            )
        )

        updater.start_polling()
        updater.idle()
    except Exception as error:
        logging.exception("TG BOT DOWN!!!", error, exc_info=True)


if __name__ == "__main__":
    main()
