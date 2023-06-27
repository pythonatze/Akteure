
import time
import pandas as pd
from datetime import datetime
from datetime import timedelta
import smtplib
import ssl
from email.message import EmailMessage
timestr = time.strftime("%Y%m%d")
print (timestr)


def kauf_note():
    email_sender = 'mavaball@gmail.com'
    email_password = 'Doggestan1971!'
    email_receiver = 'mavaball@posteo.de'

    subject = 'Kaufsignale'

    body = 'Hallöle'
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

kauf_note()