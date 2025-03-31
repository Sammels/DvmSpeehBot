import json

from environs import env

from google.cloud import dialogflow


def open_json(objects):
    """
    Open JSON file in project folder.


    Args:
            objects (str): filename

    Returns:
            dict : files
    """
    with open(f"{objects}.json", "r", encoding="utf-8") as file:
        questions_json = file.read()

    load_questions = json.loads(questions_json)
    return load_questions


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=[message_texts])
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))



# TODO: Отрефакторить, чтобы запускался их этого модуля, не изменяя дату.

# def detect_intent_texts(project_id, session_id, texts, language_code):
#     """Returns the result of detect intent with texts as inputs.

#     Using the same `session_id` between requests allows continuation
#     of the conversation."""

#     session_client = dialogflow.SessionsClient()

#     session = session_client.session_path(project_id, session_id)
#     print("Session path: {}\n".format(session))
#     text_input = dialogflow.TextInput(text=texts, language_code=language_code)

#     query_input = dialogflow.QueryInput(text=text_input)

#     response = session_client.detect_intent(
#         request={"session": session, "query_input": query_input}
#     )

#     if response.query_result.intent.is_fallback:
#         return None
#     else:
#         return response.query_result.fulfillment_text



def main():
    """
    Run main module script
    """
    fills = open_json("questions")

    for testing in fills:
        create_intent(
            GOOGLE_PROJECT_ID,
            testing,
            fills[testing]["questions"],
            fills[testing]["answer"],
        )


if __name__ == "__main__":
    env.read_env()
    GOOGLE_PROJECT_ID = env("PROJECT_ID")
    main()
