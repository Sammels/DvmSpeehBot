import argparse
import json

from environs import env

from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """
    Create an intent of the given intent type.
    """

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

def create_parser():
    parser = argparse.ArgumentParser(
        prog="Create DialogFlow intents from json file",
    )
    parser.add_argument("filepath",
                        nargs="?",
                        help="You can spesify filepath to the intents' data in json format",
                        default="../questions.json",
                        )

    return parser


def main():
    """
    Run main module script
    """
    env.read_env()

    google_project_id = env("PROJECT_ID")
    parser = create_parser()
    args = parser.parse_args()
    with open(args.filepath, 'r') as intents_file:
        intents = intents_file.read()

    intents = json.loads(intents)

    for intent in intents:
        create_intent(
            google_project_id,
            intent,
            intents[intent]["questions"],
            intents[intent]["answer"],
        )
        



if __name__ == "__main__":
    main()
