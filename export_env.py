import os
import json
import base64

# Load the credentials file
with open('model_config.json', 'rb') as file:
    credentials = file.read()

# Encode the credentials to Base64
encoded_credentials = base64.b64encode(credentials).decode('utf-8')

print("ENCODED CREDS",encoded_credentials)  # This will print the Base64 string

# Get the Base64 string from the environment variable
encoded_credentials = os.getenv('GEMINI_CREDENTIALS')

# Decode the Base64 string
decoded_credentials = base64.b64decode(encoded_credentials)

# Load the JSON data
credentials = json.loads(decoded_credentials)

# Now you can use the credentials as a dictionary
print("DECODED CREDS",credentials)
