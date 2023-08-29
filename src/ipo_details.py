import re
from datetime import date
import dotenv as denv
import os
import requests
import json

from src.mail import compose_mail_message


class Ipo:
    def __init__(self):
        denv.load_dotenv()
        self.url = os.getenv('URL')
        self.sender_email = os.getenv('EMAIL')
        self.password = os.getenv('PASSWORD')
        self.receivers_mail = os.getenv('RECEIVERS')

    def get_data_from_web(self):
        res = requests.get(self.url, headers={"X-Requested-With": "XMLHttpRequest"}).text
        return json.loads(res)['data']
