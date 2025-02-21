import random
from environs import env

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from google.cloud import dialogflow


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

    if response.query_result.intent.is_fallback:
        return None
    else:
        return response.query_result.fulfillment_text


def echo(event, vk_api):
    project_id = GOOGLE_PROJECT_ID
    session_id = "test-sess"
    language_code = GOOGLE_LANGUAGE_CODE

    text_update = detect_intent_texts(project_id, session_id, event.text, language_code)
    if text_update is not None:
        vk_api.messages.send(
            user_id=event.user_id,
            message=text_update,
            random_id=random.randint(1, 1000),
        )


if __name__ == "__main__":
    env.read_env()
    VK_GROUP_TOKEN = env("VK_GROUP_TOKEN")
    GOOGLE_PROJECT_ID = env("PROJECT_ID")
    GOOGLE_LANGUAGE_CODE = env("LANGUAGE_CODE")

    vk_session = vk.VkApi(token=VK_GROUP_TOKEN)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)
