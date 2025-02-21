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
from google.cloud import dialogflow

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s- %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    """Start messaging bot"""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте")


def response_message(update: Update, context: CallbackContext):
    """Func Echo return  user message."""
    project_id = GOOGLE_PROJECT_ID
    session_id = "test-sess"
    language_code = GOOGLE_LANGUAGE_CODE

    text_update = detect_intent_texts(
        project_id, session_id, update.message.text, language_code
    )

    context.bot.send_message(chat_id=update.effective_chat.id, text=text_update)


def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))
    text_input = dialogflow.TextInput(text=texts, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text


def main(token: str):
    """Main function running code."""

    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), response_message)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()


if __name__ == "__main__":
    env.read_env()
    TELEGRAM_TOKEN = env("TELEGRAM_TOKEN")
    GOOGLE_PROJECT_ID = env("PROJECT_ID")
    GOOGLE_LANGUAGE_CODE = env("LANGUAGE_CODE")
    main(TELEGRAM_TOKEN)
