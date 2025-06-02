from environs import env
from google.cloud import dialogflow


def detect_intent_text(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    request = dialogflow.DetectIntentRequest(session=session, query_input=query_input)
    response = session_client.detect_intent(request=request)
    return (
        response.query_result.fulfillment_text,
        response.query_result.intent.is_fallback,
    )


def main():
    env.read_env()
    project_id = env.str("PROJECT_ID")


if __name__ == "__main__":
    main()
