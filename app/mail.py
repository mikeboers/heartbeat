import smtplib
from email.mime.text import MIMEText

from .main import app


def sendmail(**kwargs):

    sender = kwargs.pop('sender', None) or app.config['MAIL_DEFAULT_SENDER']
    recipients = kwargs.pop('recipients')
    subject = kwargs.pop('subject')
    body = kwargs.pop('body')

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    smtp = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
    if app.config['MAIL_USERNAME']:
        smtp.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])

    smtp.sendmail(sender, recipients, msg.as_string())
    smtp.quit()

