from os import environ as env
import smtplib
import ssl
from email.utils import formatdate
from email.mime.text import MIMEText


SMTP_FROM = env['SMTP_FROM']
SMTP_ADDRESS = env['SMTP_ADDRESS']
SMTP_USERNAME = env['SMTP_USERNAME']
SMTP_PASSWORD = env['SMTP_PASSWORD']
SMTP_PORT = int(env['SMTP_PORT'])


def send(to, subject, body):
    with smtplib.SMTP(SMTP_ADDRESS, port=SMTP_PORT) as smtp:
        ssl_context = ssl.create_default_context()
        smtp.starttls(context=ssl_context)
        smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        # smtp.set_debuglevel(1)
        message = generate_message(to, subject, body)
        print(message)
        smtp.sendmail(SMTP_FROM, to, message)


def generate_message(to, subject, body):
    msg = MIMEText(body)

    msg['Subject'] = subject
    msg['From'] = SMTP_FROM
    msg['To'] = to
    msg["Date"] = formatdate(localtime=True)

    return msg.as_string()
