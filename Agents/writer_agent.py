from autogen import ConversableAgent, AssistantAgent
import autogen
import base64, os, json


def load_credentials_from_env():
    """Loads credentials from the environment variable."""
    # Get the Base64 encoded credentials from the environment
    encoded_credentials = os.getenv('GEMINI_CREDENTIALS')
    if not encoded_credentials:
        raise EnvironmentError("GEMINI_CREDENTIALS environment variable not set.")

    # Decode the Base64 string
    decoded_credentials = base64.b64decode(encoded_credentials)

    # Save decoded credentials temporarily for authorization
    with open('gemini_credentials.json', 'wb') as temp_cred_file:
        temp_cred_file.write(decoded_credentials)

    return 'gemini_credentials.json'

def generate_email(receipant_name):

    credentials_path = load_credentials_from_env()

    config_list_gemini = autogen.config_list_from_json(credentials_path)

    email_writer = ConversableAgent(
        name="Email Writer",
        system_message="Act as an email writer, Your task is to write a beautiful, eye catching and easy understanding mail for below event: "
        "   Zangoh studio is a leading organization in Generative ai field. They are organizing an event on 1st November 2024. Time 10 am to 11 am"
        "Topic of event is ```Integrate generative AI natively into modern products```"
        "zangoh located at `401, Atulya IT park, Indore"
        "The body of email should be in two paragraphs"
        "only return body of mail and do not include subject of mail with Warm regards",
        llm_config = {"config_list" : config_list_gemini},
        code_execution_config = False,
        human_input_mode = "NEVER",
    
)
    context = f"Write a mail to {receipant_name}  inviting for event at Zangoh studio. Mention all the details"

    reply = email_writer.generate_reply(messages=[{"content": context, "role": "user"}])
    return reply['content']



