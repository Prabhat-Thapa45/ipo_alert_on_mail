import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging

logging.basicConfig(level=logging.INFO)


def compose_mail_message(sender_email, password, receivers_mail, symbol, name, closing_date):
    subject = f"{name} IPO Open"
    body = f"कम्पनीको नाम: {name} ({symbol}) \n" \
           f"आज {symbol} कम्पनीको आईपीओ(IPO) खुलेको छ। यस कम्पनीको आईपीओ " \
           f"{str(datetime.date.today())} बाट {closing_date} " \
           f"सम्म खुला रहनेछ। \n\nहार्दिक शुभकामना\nप्रभात थापा\nIPO alerts परिवार"
    logging.info('[3] Message has been composed')
    send_mail(sender_email, password, receivers_mail, subject, body)

def send_mail(sender, password, receivers, subject, body):
    server = gmail_login(sender, password)
    logging.info("[4] Successfully logged into gmail server")

    for receiver in receivers.split(','):
        try:
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = receiver
            msg.attach(MIMEText(body, 'plain'))
            server.send_message(msg)
        except Exception as e:
            return f'Error: {e}'
    logging.info("[5] Message sent to recipient")
    return "Message sent to recipient"
    server.quit()



def gmail_login(sender, password):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    logging.info("[4] Failed to login invalid credentials")
    return server
