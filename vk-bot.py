import logging
import random
from environs import env

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from DvmSpeehBot.diagflow_script import detect_intent_text
from logs import TelegramLogsHandler


logger = logging.getLogger("vk_bot")


def perform_intent(event, vk_api):
    project_id = GOOGLE_PROJECT_ID
    session_id = "test-sess"
    language_code = GOOGLE_LANGUAGE_CODE

    text_update = detect_intent_text(project_id, session_id, event.text, language_code)
    if text_update is not None:
        vk_api.messages.send(
            user_id=event.user_id,
            message=text_update[0],
            random_id=random.randint(1, 1000),
        )


def main(tg_logger, tg_logger_chat, vk_group):
    logging.basicConfig(
        format="%(asctime)s - %(funcName)s -  %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(tg_logger, tg_logger_chat))
    try:
        logger.info("VK Bot run")
        vk_session = vk.VkApi(token=vk_group)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                perform_intent(event, vk_api)
    except Exception as err:
        logger.error(err, exc_info=True)


if __name__ == "__main__":
    env.read_env()
    VK_GROUP_TOKEN = env("VK_GROUP_TOKEN")
    TELEGRAM_LOGGER = env("TG_BOT_LOGGER_TOKEN")
    TELEGRAM_LOGER_CHAT_ID = env("TG_CHAT_ID")
    GOOGLE_PROJECT_ID = env("PROJECT_ID")
    GOOGLE_LANGUAGE_CODE = env("LANGUAGE_CODE")

    main(TELEGRAM_LOGGER, TELEGRAM_LOGER_CHAT_ID, VK_GROUP_TOKEN)
