import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(sender, password, receivers, subject, body):
    server = gmail_login(sender, password)

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
    server.quit()


# def welcome_mail(receivers):
#     ...
#
#
def gmail_login(sender, password):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    return server
