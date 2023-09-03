import re
from datetime import date
from json import JSONDecodeError
import backoff
import dotenv as denv
import os
import requests
import json
import logging
logging.basicConfig(level=logging.INFO)
from src.mail import compose_mail_message


class Ipo:
    def __init__(self):
        denv.load_dotenv()
        self.url = os.getenv('URL')
        self.sender_email = os.getenv('EMAIL')
        self.password = os.getenv('PASSWORD')
        self.receivers_mail = os.getenv('RECEIVERS')


    @backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, JSONDecodeError), max_tries=3)
    def get_data_from_web(self):
        res = requests.get(self.url, timeout=60*30, headers={"X-Requested-With": "XMLHttpRequest"}).text
        return json.loads(res)['data']

    @staticmethod
    def get_ipos_opened_today(data):
        ipos = []
        for item in data:
            if item['opening_date'] == str(date.today()):
                ipos.append(item)
        return ipos

    @staticmethod
    def search_company_details(s: str) -> str:
        return re.search('>(.*)<', s).group(1)

    def handler(self):
        try:
            data = self.get_data_from_web()
            logging.info("[2] Successfully retrieved data from web")
        except JSONDecodeError:
            logging.info("[2] Failed to get data from web 'JSONDecodeError'")
            return "Unable to get data"
        ipos = self.get_ipos_opened_today(data)
        for ipo in ipos:
            company = ipo['company']
            company_symbol = self.search_company_details(company['symbol'])
            company_name = self.search_company_details(company['companyname'])
            closing_date = ipo['closing_date']
            compose_mail_message(self.sender_email, self.password, self.receivers_mail, company_symbol, company_name, closing_date)
        logging.info("[4] No Ipos for today")
        return "We don't have any IPO opening today"