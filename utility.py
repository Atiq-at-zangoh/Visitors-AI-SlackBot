import re
import os
from PIL import Image
import google.generativeai as genai
import json
import pandas as pd
from csv import writer
import requests
import requests
from urllib.parse import urlencode
import string
from dotenv import load_dotenv
load_dotenv() 

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def create_csv():

    if not os.path.exists("visitors.csv"):

        visitor_details_table = pd.DataFrame(columns=["Name", "Contact", "Email", "Company", "Designation"])

        visitor_details_table.to_csv("visitors.csv")
        
def update_csv(new_visitor: list):

    with open('visitors.csv', 'a') as f:
 
        writer_object = writer(f)
 
        writer_object.writerow(new_visitor)
 
        f.close()

def get_gemini_response(image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = """
             An image is given to you, now your task is to extract the following information from image: Name, Email, contact, company, designation.
             And response should be in python dictionary format - 
             {
              "name": "name extracted from image",
              "email": email address extracted from image in form of ``dummy@example.com``,
              "contact": "contact extracted from image",
              "company": "company extracted from image",
              "designation": "designation extracted from image",
             }
             if any information is not found then return `None`
               for example: `company not found` then output should be -
               {
              "name": "name extracted from image",
              "email": email address extracted from image in form of ``dummy@examle.com``,
              "contact": "contact extracted from image",
              "company": "None",
              "designation": "designation extracted from image",
             }    
             Be careful regarding email, it have to be correct.  

                """
    response = model.generate_content([prompt,image])

    return response.text

def extract_email(text):
    # Regular expression pattern to match email addresses
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    
    # Find all email addresses in the text
    email_matches = re.findall(email_pattern, text)
    
    # Return the email addresses found
    return email_matches

def image_to_dict(user_img):
    image = Image.open(user_img)
    user_data= (get_gemini_response(image))
    match = re.search(r'\{(.*?)\}', user_data, re.DOTALL)
    json_str = '{' + match.group(1) + '}'
    data_dict=json.loads(json_str)
    return data_dict

def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

def clean_mobile_number(mobile_number):
    # Remove all punctuation from the mobile number
    cleaned_number = ''.join(char for char in mobile_number if char not in string.punctuation)
    return cleaned_number

def submit_lead(name, email, contact, company, designation):
    try:
        # Step 1: Refresh the token
        refresh_token_data = {
            'refresh_token': os.getenv("ZOHO_REFRESH_TOKEN"),
            'grant_type': 'refresh_token',
            'client_id': os.getenv("ZOHO_CLIENT_ID"),
            'client_secret': os.getenv("ZOHO_CLIENT_SECRET") 
        }

        refresh_token_options = {
            'url': "https://accounts.zoho.in/oauth/v2/token",
            'headers': {"Content-Type": "application/x-www-form-urlencoded"},
            'data': urlencode(refresh_token_data)
        }

        response_refresh_token = requests.post(refresh_token_options['url'], headers=refresh_token_options['headers'], data=refresh_token_options['data'])
        
        if response_refresh_token.status_code != 200:
            raise Exception("Failed to refresh token")

        access_token = response_refresh_token.json().get('access_token')

        # Step 2: Prepare the lead data
        lead_data = {
            'data': [{
                'First_Name': name,
                'Last_Name': "///",  # Default value if not provided
                'Email': email,
                'Mobile': contact,
                'Company': company,
                'Designation': designation,  # Optional field
                'Description': "----***----",  # Optional field
                'type':  'other' # Default value if not provided
            }]
        }

        print("Lead Data being sent to Zoho:", lead_data)

        # Step 3: Send lead data to Zoho CRM
        crm_response = requests.post(
            "https://www.zohoapis.in/crm/v2/Leads",
            json=lead_data,
            headers={
                'Authorization': f'Zoho-oauthtoken {access_token}',
                'Content-Type': 'application/json'
            }
        )

        if crm_response.status_code in [200, 201]:
            success_response = {
                'statusCode': 200,
                'headers': generate_cors_headers(),
                'body': {"message": "Someone from Zangoh will reach out to you."}
            }
            return success_response
            
        else:
            print("Error response from Zoho CRM:", crm_response.json())
           
    except Exception as e:
        error_details = {
            'message': str(e),
            'response': e.response.json() if hasattr(e, 'response') else None,
            'config': e.__dict__,
            'code': e.__class__.__name__
        }
        print("Error in submit_lead:", error_details)
        
# Helper functions for CORS headers and error response
def generate_cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST",
        "Access-Control-Allow-Headers": "Content-Type, Authorization"
    }

def generate_error_response(message):
    return {
        'statusCode': 500,
        'headers': generate_cors_headers(),
        'body': {"error": message}
    }



# Example usage
# text = "END AN EMAIL TO '<MAILTO:DEMO28751@GMAIL.COM|DEMO28751@GMAIL.COM>'"
# emails = (extract_email(text))
# print(emails[0])


