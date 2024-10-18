# from  slack.gmail_api.mail_with_attachment import auth_and_send
from PIL import Image
from utility import image_to_dict, submit_lead, clean_mobile_number
import aiohttp
import json
import re
# user_img="user_img/Red Modern Business Card.png"
# img=str(image_to_dict(user_img=user_img))
# print(img)
# print(type(img))

# print(auth_and_send(recipient='demo28751@gmail.com', email_body="Body of email", attachment="Poster.png"))

# card_name = data_dict['name']
# card_email = data_dict['email']
# card_phone= data_dict['contact'], 
# card_company= data_dict['company'], 
# card_designation= data_dict['designation']

# if card_name and validate_email(email=card_email):
#     ## Agent wil generate a mail
    
#     email_body = generate_email(card_name)
#     # Email details
    
#     # Send the email
#     auth_and_send(recipient=card_email, email_body=email_body, attachment=file_path)
                    
print(submit_lead("trefgdf","afsd@jflks.com", clean_mobile_number("34-5809-83-]66"),"trt","sfs"))
# print(image_to_dict("user_img/Red Modern Business Card-2.png"))

