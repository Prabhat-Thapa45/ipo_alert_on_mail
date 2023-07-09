import pandas as pd
import dotenv as denv
import os
import nepali_datetime
import requests
from fuzzywuzzy import process
from src.mail import send_mail


class Ipo:
    def __init__(self):
        denv.load_dotenv()
        self.url = os.getenv('URL')
        self.sender_email = os.getenv('EMAIL')
        self.password = os.getenv('PASSWORD')
        self.receivers_mail = os.getenv('RECEIVERS')
        self.res = requests.get(self.url)
        self.data = pd.read_html(self.res.text, flavor='bs4')[0]
        self.date_open = self.data["Open"]

    def reformat_opening_date(self):
        if type(self.data["Open"][0]) is str:
            ipo_open_date = []
            for date in self.date_open:
                month_in_nepali, day = date.split()
                months_in_nepali = nepali_datetime._FULLMONTHNAMES
                month_in_nepali2 = process.extractOne(query=month_in_nepali, choices=months_in_nepali)[0]
                month_in_number = months_in_nepali.index(month_in_nepali2)
                ipo_open_date.append(nepali_datetime.datetime.strptime(
                    f'{day}-{month_in_number}-{nepali_datetime.datetime.now().year}', '%d-%m-%Y').date())
            self.data["Open"] = pd.Series(ipo_open_date)

    def available_ipo(self):
        self.reformat_opening_date()
        return self.data[self.data["Open"] == nepali_datetime.datetime.now().date()]

    def call_send_mail(self):
        data = self.available_ipo()
        available_company = data.__len__()
        if available_company:
            subject = f"{data['Company'].to_string(index=False)} IPO Open"
            if available_company == 1:
                body = f"{data['Company'].to_string(index=False)} कम्पनीको आईपीओ(IPO) " \
                       f"{data['For'].to_string(index=False)} को लागि खुलिएको छ। यस कम्पनीको आईपीओ " \
                       f"{data['Open'].to_string(index=False)} बाट {data['Close'].to_string(index=False)} " \
                       f"सम्म खुला रहनेछ। \n\nहार्दिक शुभकामना\nप्रभात थापा\nIPO alerts परिवार"
            else:
                body = f"आज {', '.join(self.data['Company'][:-1].astype(str))} र {data['Company'][-1]} " \
                       f"कम्पनीहरूको आईपिओ खुलेका छन्। \n\nहार्दिक शुभकामना\nप्रभात थापा\nIPO alerts परिवार"

            send_mail(self.sender_email, self.password, self.receivers_mail, subject, body)
