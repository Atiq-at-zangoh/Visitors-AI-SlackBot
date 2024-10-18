import os
import base64
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def create_message_with_attachment(sender, to, subject, body_text, file):
    """Create a message for an email with an attachment.
    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      body_text: The body of the email message.
      file: The path to the file to be attached.
    Returns:
      An object containing a base64url encoded email object.
    """
    # Create the MIME message
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    # Attach the body text to the message
    message.attach(MIMEText(body_text, 'plain'))

    # Attach the file
    with open(file, 'rb') as attachment:
        mime_base = MIMEBase('application', 'octet-stream')
        mime_base.set_payload(attachment.read())
        encoders.encode_base64(mime_base)
        mime_base.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file)}"')
        message.attach(mime_base)

    # Encode the message to base64
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    return {'raw': raw_message}

def load_credentials_from_env():
    """Loads credentials from the environment variable."""
    # Get the Base64 encoded credentials from the environment
    encoded_credentials = os.getenv('GMAIL_API_CREDENTIALS')
    if not encoded_credentials:
        raise EnvironmentError("GMAIL_API_CREDENTIALS environment variable not set.")

    # Decode the Base64 string
    decoded_credentials = base64.b64decode(encoded_credentials)

    # Save decoded credentials temporarily for authorization
    with open('temp_credentials.json', 'wb') as temp_cred_file:
        temp_cred_file.write(decoded_credentials)

    return 'temp_credentials.json'

def auth_and_send(recipient, email_body, attachment):
    """Shows basic usage of the Gmail API.
    Sends an email with an attachment.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Load credentials from the environment variable instead of file
            credentials_path = load_credentials_from_env()
            
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the Gmail service
    service = build('gmail', 'v1', credentials=creds)

    # Sender and receiver details
    sender = "atiq@zangoh.com"
    to = recipient
    subject = "Event Update: ``Integrate Generative AI natively into modern products`` webinar"
    body_text = email_body

    # Create the email message with the attachment
    message = create_message_with_attachment(sender, to, subject, body_text, file=attachment)

    # Send the email
    try:
        service.users().messages().send(userId="me", body=message).execute()
        print("Email sent successfully.")
        return "Email sent successfully."
    except Exception as error:
        print(f"An error occurred: {error}")
        return f"An error occurred: {error}"

