import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl 
from email.message import EmailMessage
from secret import APP_PASSWORD

def send_email(recEmail):
    
    sender = "distantdeveloper.official@gmail.com"
    #reciever = ""
    password = APP_PASSWORD

    subject = "Verified Email; Distant Developer"
    body = "Your code is"

    em = EmailMessage()
    em["From"] = sender
    em["To"] = recEmail
    em["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, recEmail, em.as_string())