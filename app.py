import os
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
from dotenv import find_dotenv, load_dotenv
from flask import Flask, request
# from functions import draft_email
import certifi
from gmail_api.mail_with_attachment import auth_and_send
from utility import image_to_dict, validate_email, create_csv, update_csv, submit_lead, clean_mobile_number, extract_email
from Agents.writer_agent import generate_email
from check_email import validate_email_smtp


# Load environment variables from .env file
load_dotenv(find_dotenv())

os.environ['SSL_CERT_FILE'] = certifi.where()

# Set Slack API credentials
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_BOT_USER_ID = os.environ["SLACK_BOT_USER_ID"]

# Initialize the Slack app
app = App(token=SLACK_BOT_TOKEN)

# Initialize the Flask app
# Flask is a web application framework written in Python
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


def get_bot_user_id():
    """
    Get the bot user ID using the Slack API.
    Returns:
        str: The bot user ID.
    """
    try:
        # Initialize the Slack client with your bot token
        slack_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
        response = slack_client.auth_test()
        return response["user_id"]
    except SlackApiError as e:
        print(f"Error: {e}")

def my_function(text):
    """
    Custom function to process the text and return a response.
    In this example, the function converts the input text to uppercase.

    Args:
        text (str): The input text to process.

    Returns:
        str: The processed text.
    """
    response = text.upper()
    return response

def download_image(file_url, file_name):
    """
    Download the image from Slack using the file URL with requests.

    Args:
        file_url (str): The URL of the file to download.
        file_id (str): The file ID.
    """
    try:
        
        # Set up the headers to authenticate the request with the bot token
        headers = {
            "Authorization": f"Bearer {os.environ['SLACK_BOT_TOKEN']}"
        }

        # Download the image using the authenticated request
        image_response = requests.get(file_url, headers=headers)

        # Check if the request was successful
        if image_response.status_code == 200:

            # Save the image to a local file
            img_path= f"user_img/{file_name}"

            with open(img_path, "wb") as f:
                f.write(image_response.content)
            print("Image successfully downloaded!")
            return img_path
        else:
            print(f"Failed to download image. Status code: {image_response.status_code}")
            return None
    
    except SlackApiError as e:
        print(f"Error fetching file info: {e}")



@app.event("app_mention")
def handle_mentions(body, say):
    """
    Event listener for mentions in Slack.
    When the bot is mentioned, this function processes the text and sends a response.

    Args:
        body (dict): The event data received from Slack.
        say (callable): A function for sending a response to the channel.
    """

    event = body["event"]
    
    say(f"I got it")
    
    # Check if there's a file attached to the event
    if "files" in event:
        files = event["files"]
        
        # Loop through files (if multiple files uploaded)
        for file_info in files:
            # Check if the file type is an image
            if file_info["mimetype"].startswith("image/"):
                file_id = file_info["id"]
                file_name = file_info["name"]
                file_url = file_info["url_private_download"]
                
                say(f"Image '{file_name}' received! Retrieving the image...")
                
                # Call a function to download the image or perform any action
                image_path=download_image(file_url=file_url, file_name=file_name)

                ## Extract info from image
                img_info = image_to_dict(image_path)
                print(img_info)

                ## Send mail 
                card_name = img_info['name']
                card_email = img_info['email']
                card_phone= img_info['contact'], 
                card_company= img_info['company'], 
                card_designation= img_info['designation']

                
                say(str(img_info))

                if  validate_email_smtp(email=card_email):
                    ## Agent wil generate a mail

                    email_body = generate_email(card_name)
                    
                    # Email details

                    # Send the email
                    auth_and_send(recipient=card_email, email_body=email_body, attachment="Poster.png")
                    say(f"Email sent successfully to: '{card_email}'")

                    ## Update in Zoho
                
                    submit_lead(name=str(card_name), 
                            email=str(card_email), 
                            contact=clean_mobile_number(card_phone), 
                            company= str(card_company), 
                            designation= str(card_designation))

                else:
                    say(f"{card_email} is not valid.")
                    say("Again mention me and Please enter email manually.")

    else:
        # Process text (if no files are attached)
        text = event["text"]
        mention = f"<@{SLACK_BOT_USER_ID}>"
        
        text = text.replace(mention, "").strip()
        
        say(f"You said: {text}")
        
        email_address=extract_email(text=text)
        email= email_address[0]
        print(email)
        
        if validate_email_smtp(email=email):

            say(f"Sure, I'll send mail on : {email}")
            
            name = email.split("@")[0]

            ## Generate body of mail
            email_body = generate_email(name)

            ## Send mail
            auth_and_send(recipient=email, email_body=email_body, attachment="Poster.png")
            say(f"Invitation sent on: {email}")

            ## Update Zoho CRM

            submit_lead(name=str(card_name), 
                            email=str(card_email), 
                            contact=clean_mobile_number(card_phone), 
                            company= str(card_company), 
                            designation= str(card_designation))

        else:
            say(f"{email} does not exists.")
            print(f"{email} does not exists.")
            say("Check it carefully.")


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    """
    Route for handling Slack events.
    This function passes the incoming HTTP request to the SlackRequestHandler for processing.

    Returns:
        Response: The result of handling the request.
    """
    return handler.handle(request)


# Run the Flask app
if __name__ == "__main__":
    flask_app.run(host='0.0.0.0', port=5000)