import json

from environs import env

from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
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


def main():
    """
    Run main module script
    """
    json_filename = "questions"

    with open(f"{json_filename}.json", "r", encoding="utf-8") as file:
        questions_json = file.read()

    intents = json.loads(questions_json)

    for intent in intents:
        create_intent(
            GOOGLE_PROJECT_ID,
            intent,
            intents[intent]["questions"],
            intents[intent]["answer"],
        )
        



if __name__ == "__main__":
    env.read_env()
    GOOGLE_PROJECT_ID = env("PROJECT_ID")
    main()
