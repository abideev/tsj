import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def send_email(to, subject, template):
    smtp_server="smtp.gmail.com"
    port=587
    login='ah.bideev@gmail.com'
    receiver='ah.bideev@gmail.com'
    password='TEST'
    sender='ah.bideev@gmail.com'


    message=MIMEMultipart()
    message['From'] = receiver
    message['To'] = to
    message['Subject'] = subject
    message.attach(MIMEText(template, "html"))

    text=message.as_string()

    s=smtplib.SMTP(smtp_server, port)
    s.ehlo()
    s.starttls()
    s.login(login, password)  # See https://support.google.com/accounts/answer/6010255
    try:
        s.sendmail(sender, to, text.encode('utf-8'))
    except Exception as e:
        print(e)


