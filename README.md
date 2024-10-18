# SlackBot with Image Handling and Email Automation

This repository contains a Slack bot that listens for mentions in Slack channels, processes images (such as business cards), and automates sending emails using a Gmail API. Additionally, it validates email addresses via SMTP and submits leads to Zoho CRM.

## Features

- **Slack Integration:** Listens for mentions and responds to text or image uploads.
- **Image Processing:** Downloads and processes images uploaded to Slack, extracting relevant information (e.g., name, email, phone number).
- **Email Automation:** Generates and sends custom emails using the Gmail API.
- **Email Validation:** Validates email addresses using SMTP.
- **Lead Management:** Submits valid leads to Zoho CRM after processing the image or manual input.
  
## Installation

### Prerequisites
- Python 3.7+
- [Slack API](https://api.slack.com/)
- [Gmail API](https://developers.google.com/gmail/api)
- [Zoho CRM API](https://www.zoho.com/crm/)
- [Ngrok](https://ngrok.com/) (for tunneling)
- Install required Python libraries from `requirements.txt`

### Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Atiq-at-zangoh/Visitors-Slack-Bot.git
    cd Visitors-Slack-Bot
    ```

2. **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
   Create a `.env` file in the project root with the following content:
    ```env
    SLACK_BOT_TOKEN = "xxxxx->> Enter your's <<-xxxxx"
    SLACK_SIGNING_SECRET = "xxxxx->> Enter your's <<-xxxxx"
    SLACK_BOT_USER_ID = "xxxxx->> Enter your's <<-xxxxx"
    GOOGLE_API_KEY= "xxxxx->> Enter your's <<-xxxxx"

    ZOHO_CLIENT_ID= "xxxxx->> Enter your's <<-xxxxx"
    ZOHO_CLIENT_SECRET= "xxxxx->> Enter your's <<-xxxxx"
    ZOHO_REFRESH_TOKEN= "xxxxx->> Enter your's <<-xxxxx"

    GMAIL_API_CREDENTIALS= "xxxxx->> Enter your's <<-xxxxx"

    GEMINI_CREDENTIALS= "xxxxx->> Enter your's <<-xxxxx"
    ```

5. **Configure SSL Certificate:**
   The bot requires SSL certificates for secure API requests:
    ```python
    import certifi
    os.environ['SSL_CERT_FILE'] = certifi.where()
    ```

6. **Run the Slack bot server:**
    ```bash
    python app.py
    ```

### Slack App Configuration

1. Go to your [Slack API Apps page](https://api.slack.com/apps).
2. Create a new app and configure **OAuth Scopes** (e.g., `chat:write`, `files:read`, `files:write`, etc.).
3. Set up the event subscription URL to: `https://your-server-url/slack/events`.

### Using Ngrok for Local Development

Ngrok is used to expose your local Flask server to the internet, allowing Slack to send event data. Follow these steps:

1. **Install Ngrok** if you haven't already:
    ```bash
    brew install ngrok  # For Mac
    sudo apt-get install ngrok  # For Ubuntu
    ```

2. **Start Ngrok**:
    ```bash
    ngrok http 5000
    ```

    This will expose your local server running on port 5000 to the internet. You'll get a forwarding URL like this:
    ```
    Forwarding https://95f0-125-99-189-110.ngrok-free.app -> http://localhost:5000
    ```

3. **Update Slack Event Subscription**: Go to your Slack app settings and update the **Request URL** for **Event Subscriptions** to your Ngrok forwarding URL:
    ```
    https://95f0-125-99-189-110.ngrok-free.app/slack/events
    ```

    **Note:** Ngrok URLs change every time you restart it, so you'll need to update this URL in Slack settings each time you restart Ngrok.

4. **Monitor Ngrok Traffic**: You can monitor the incoming traffic and request logs through the Ngrok web interface at:
    ```
    http://127.0.0.1:4040
    ```

### Gmail API Configuration

1. Enable the Gmail API in the Google Developer Console.
2. Set up OAuth 2.0 credentials and download the `client_secret.json`.
3. Follow the steps to authenticate the bot to send emails on behalf of a Gmail account.

### Zoho CRM API Configuration

1. Enable API access in Zoho CRM.
2. Set up OAuth credentials and configure access tokens for lead submission.

## Usage

- **Mention the Bot in Slack:** 
  The bot listens for mentions and processes any attached images or email addresses.
  
  Example:
  - Send an image of a business card, and the bot will extract information and send an email to the identified address.
  - Mention the bot with an email address, and it will validate the address and send a custom email.

- **Email Sending:** The bot automatically sends emails based on image-extracted data or manual input, using the Gmail API.

- **Lead Submission:** The bot submits valid leads to Zoho CRM after successfully processing an image or text.

## File Structure

- `app.py`: Main application file containing the Slack bot logic and Flask server.
- `gmail_api/`: Folder containing email automation functions using the Gmail API.
- `Agents/writer_agent.py`: Generates email content.
- `check_email.py`: Validates email addresses via SMTP.
- `utility.py`: Contains utility functions like image processing, CSV creation, and lead submission.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for improvements and bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
