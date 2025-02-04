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
    "Start messaging bot"
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте")


def echo(update: Update, context: CallbackContext):
    "Func Echo return  user message"
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )
        print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))


def main(token: str, GOOGLE_PROJECT_ID: str, GOOGLE_LANGUAGE_CODE: str):
    """Main function running code"""
    project_id = GOOGLE_PROJECT_ID
    session_id = "test-sess"
    texts = ["Привет"]
    language_code = GOOGLE_LANGUAGE_CODE
    detect_intent_texts(project_id, session_id, texts, language_code)

    # updater = Updater(token=token)
    # dispatcher = updater.dispatcher

    # start_handler = CommandHandler("start", start)
    # dispatcher.add_handler(start_handler)

    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dispatcher.add_handler(echo_handler)

    # updater.start_polling()


if __name__ == "__main__":
    env.read_env()
    TELEGRAM_TOKEN = env("TELEGRAM_TOKEN")
    GOOGLE_PROJECT_ID = env("PROJECT_ID")
    GOOGLE_LANGUAGE_CODE = env("LANGUAGE_CODE")
    main(TELEGRAM_TOKEN, GOOGLE_PROJECT_ID, GOOGLE_LANGUAGE_CODE)
