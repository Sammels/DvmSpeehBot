import logging
import random
from environs import env

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from diagflow_script import detect_intent_text
from logs import TelegramLogsHandler


logger = logging.getLogger("vk_bot")


def perform_intent(event, vk_api, project_id, language_code):
    session_id = "vk-{event.user_id}"

    text_update = detect_intent_text(
        project_id=project_id,
        session_id=session_id,
        text=event.text,
        language_code=language_code,
    )
    if text_update is not None:
        vk_api.messages.send(
            user_id=event.user_id,
            message=text_update[0],
            random_id=random.randint(1, 1000),
        )


def main():

    env.read_env()
    config = {
        "vk_group_token": env("VK_GROUP_TOKEN"),
        "telegramm_logger": env("TG_BOT_LOGGER_TOKEN"),
        "telegramm_logger_chat_id": env("TG_CHAT_ID"),
        "google_project_id": env("PROJECT_ID"),
        "google_language_code": env("LANGUAGE_CODE")
    }

    
    logging.basicConfig(
        format="%(asctime)s - %(funcName)s -  %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(config["telegramm_logger"], config["telegramm_logger_chat_id"]))
    try:
        logger.info("VK Bot run")
        vk_session = vk.VkApi(token=config["vk_group_token"])
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                perform_intent(event, 
                               vk_api,
                               config["google_project_id"],
                               config["google_language_code"])
                
    except Exception as error:
        logging.exception("VK BOT DOWN!!!", error, exc_info=True)


if __name__ == "__main__":


    main()
