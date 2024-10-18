import smtplib
import dns.resolver  # Requires: pip install dnspython

def validate_email_smtp(email):
    # Split the email into the local-part and domain
    domain = email.split('@')[-1]

    try:
        # Step 1: Get the MX record of the domain
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(records[0].exchange)
        
        # Step 2: Connect to the mail server
        server = smtplib.SMTP()
        server.set_debuglevel(0)  # Optional: set to 1 to see communication with the server
        server.connect(mx_record)
        server.helo(server.local_hostname)  # Greet the server
        server.mail('test@example.com')  # Mail from a test email
        code, message = server.rcpt(email)  # Check if the recipient email exists
        
        server.quit()

        if code == 250:
            return True  # Email exists
        else:
            return False  # Email does not exist
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

