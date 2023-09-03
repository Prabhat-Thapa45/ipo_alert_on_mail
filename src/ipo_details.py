import re
from datetime import date
from json import JSONDecodeError
import backoff
import dotenv as denv
import os
import requests
import logging
from requests_html import HTMLSession

logging.basicConfig(level=logging.INFO)
from src.mail import compose_mail_message


class Ipo:
    def __init__(self):
        denv.load_dotenv()
        self.url = os.getenv('URL')
        self.sender_email = os.getenv('EMAIL')
        self.password = os.getenv('PASSWORD')
        self.receivers_mail = os.getenv('RECEIVERS')

    @backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, JSONDecodeError), max_tries=9)
    def get_data_from_web(self):
        session = HTMLSession()
        response = session.get(url=self.url, headers={"X-Requested-With": "XMLHttpRequest"})
        response.html.render(timeout=2000)  # Waits for JavaScript to load
        return response.json()['data']

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
            data = [{'companyid': 1260, 'ratio_value': None, 'total_units': '3825000.00', 'issue_price': '100.00',
                     'opening_date': '', 'closing_date': '', 'final_date': '', 'right_eligibility_link': None,
                     'announcement_link': None, 'issue_manager': 'Muktinath Capital Ltd.', 'listing_date': '',
                     'displayable_share_type': 'Others',
                     'company': {'id': 1260, 'symbol': "<a href='https://www.sharesansar.com/company/vlcl'>VLCL</a>",
                                 'companyname': "<a href='https://www.sharesansar.com/company/vlcl'>Vision Lumbini Urja Company Limited</a>"},
                     'status': -2, 'bkstatus': -2, 'view': '<i class="fa fa-times" aria-hidden="true"></i>',
                     'DT_Row_Index': 1},
                    {'companyid': 765, 'ratio_value': None, 'total_units': '9000000.00', 'issue_price': '244.00',
                     'opening_date': '2023-09-01', 'closing_date': '2023-09-05', 'final_date': '2023-09-15',
                     'right_eligibility_link': None,
                     'announcement_link': 'https://www.sharesansar.com/announcementdetail/citizen-life-insurance-company-limited-has-published-an-offer-letter-to-issue-9000000-units-ipo-shares-to-the-general-public-from-15th-bhadra-to-19th-bhadra-2080-2023-08-23',
                     'issue_manager': 'NIMB Ace Capital Limited', 'listing_date': '',
                     'displayable_share_type': 'Others',
                     'company': {'id': 765, 'symbol': "<a href='https://www.sharesansar.com/company/clicl'>CLICL</a>",
                                 'companyname': "<a href='https://www.sharesansar.com/company/clicl'>Citizen Life Insurance Company Limited</a>"},
                     'status': 0, 'bkstatus': -1,
                     'view': "<a href='https://www.sharesansar.com/announcementdetail/citizen-life-insurance-company-limited-has-published-an-offer-letter-to-issue-9000000-units-ipo-shares-to-the-general-public-from-15th-bhadra-to-19th-bhadra-2080-2023-08-23' target='_blank'><i class='fa fa-file' aria-hidden='true'></i><a>",
                     'DT_Row_Index': 2},
                    {'companyid': 1243, 'ratio_value': None, 'total_units': '1205320.00', 'issue_price': '206.00',
                     'opening_date': '2023-08-27', 'closing_date': '2023-08-30', 'final_date': '2023-09-10',
                     'right_eligibility_link': None,
                     'announcement_link': 'https://www.sharesansar.com/announcementdetail/mandu-hydropower-limited-has-published-an-offer-letter-to-issue-1205320-units-ipo-shares-to-the-general-public-from-10th-bhadra-to-24th-bhadra-2080-2023-08-19',
                     'issue_manager': 'Prabhu Capital limited', 'listing_date': '', 'displayable_share_type': 'Others',
                     'company': {'id': 1243, 'symbol': "<a href='https://www.sharesansar.com/company/mahl'>MAHL</a>",
                                 'companyname': "<a href='https://www.sharesansar.com/company/mahl'>Mandu Hydropower Limited</a>"},
                     'status': 1, 'bkstatus': -1,
                     'view': "<a href='https://www.sharesansar.com/announcementdetail/mandu-hydropower-limited-has-published-an-offer-letter-to-issue-1205320-units-ipo-shares-to-the-general-public-from-10th-bhadra-to-24th-bhadra-2080-2023-08-19' target='_blank'><i class='fa fa-file' aria-hidden='true'></i><a>",
                     'DT_Row_Index': 3},
                    {'companyid': 1138, 'ratio_value': None, 'total_units': '712220.00', 'issue_price': '116.00',
                     'opening_date': '2023-08-22', 'closing_date': '2023-08-25', 'final_date': '2023-09-05',
                     'right_eligibility_link': None,
                     'announcement_link': 'https://www.sharesansar.com/announcementdetail/bhagawati-hydropower-development-company-limited-has-published-an-offer-letter-to-issue-712220-units-ipo-shares-to-the-general-public-from-bhadra-5-8-2080-2023-08-14',
                     'issue_manager': 'Siddhartha Capital Ltd', 'listing_date': '', 'displayable_share_type': 'Others',
                     'company': {'id': 1138,
                                 'symbol': "<a href='https://www.sharesansar.com/company/bhpdcl'>BHPDCL</a>",
                                 'companyname': "<a href='https://www.sharesansar.com/company/bhpdcl'>Bhagawati Hydropower Development Company Limited</a>"},
                     'status': 1, 'bkstatus': -1,
                     'view': "<a href='https://www.sharesansar.com/announcementdetail/bhagawati-hydropower-development-company-limited-has-published-an-offer-letter-to-issue-712220-units-ipo-shares-to-the-general-public-from-bhadra-5-8-2080-2023-08-14' target='_blank'><i class='fa fa-file' aria-hidden='true'></i><a>",
                     'DT_Row_Index': 4},
                    {'companyid': 760, 'ratio_value': None, 'total_units': '7680000.00', 'issue_price': '239.00',
                     'opening_date': '2023-08-17', 'closing_date': '2023-08-21', 'final_date': '2023-08-31',
                     'right_eligibility_link': None,
                     'announcement_link': 'https://www.sharesansar.com/announcementdetail/sun-nepal-life-insurance-company-limited-has-published-an-offer-letter-to-issue-7680000-units-ipo-shares-to-the-general-public-from-32nd-shrawan-to-4th-bhadra-2080-2023-08-09',
                     'issue_manager': 'Nepal SBI Merchant Banking Limited', 'listing_date': '',
                     'displayable_share_type': 'Others',
                     'company': {'id': 760, 'symbol': "<a href='https://www.sharesansar.com/company/snlicl'>SNLICL</a>",
                                 'companyname': "<a href='https://www.sharesansar.com/company/snlicl'>Sun Nepal Life Insurance Company Limited</a>"},
                     'status': 1, 'bkstatus': 0,
                     'view': "<a href='https://www.sharesansar.com/announcementdetail/sun-nepal-life-insurance-company-limited-has-published-an-offer-letter-to-issue-7680000-units-ipo-shares-to-the-general-public-from-32nd-shrawan-to-4th-bhadra-2080-2023-08-09' target='_blank'><i class='fa fa-file' aria-hidden='true'></i><a>",
                     'DT_Row_Index': 5},
                    {'companyid': 1250, 'ratio_value': None, 'total_units': '2276620.00', 'issue_price': '100.00',
                     'opening_date': '2023-08-13', 'closing_date': '2023-08-16', 'final_date': '2023-08-27',
                     'right_eligibility_link': None,
                     'announcement_link': 'https://www.sharesansar.com/announcementdetail/manakamana-engineering-hydropower-limited-has-published-an-offer-letter-to-issue-2276620-units-ipo-shares-to-the-general-public-from-28th-shrawan-to-31st-shrawan-2080-2023-08-04',
                     'issue_manager': 'B.O.K Capital Market Ltd', 'listing_date': '',
                     'displayable_share_type': 'Others',
                     'company': {'id': 1250, 'symbol': "<a href='https://www.sharesansar.com/company/mehl'>MEHL</a>",
                                 'companyname': "<a href='https://www.sharesansar.com/company/mehl'>Manakamana Engineering Hydropower Limited</a>"},
                     'status': 1, 'bkstatus': 0,
                     'view': "<a href='https://www.sharesansar.com/announcementdetail/manakamana-engineering-hydropower-limited-has-published-an-offer-letter-to-issue-2276620-units-ipo-shares-to-the-general-public-from-28th-shrawan-to-31st-shrawan-2080-2023-08-04' target='_blank'><i class='fa fa-file' aria-hidden='true'></i><a>",
                     'DT_Row_Index': 6},
                    {'companyid': 737, 'ratio_value': None, 'total_units': '9600000.00', 'issue_price': '257.00',
                     'opening_date': '2023-08-08', 'closing_date': '2023-08-11', 'final_date': '2023-08-22',
                     'right_eligibility_link': None,
                     'announcement_link': 'https://www.sharesansar.com/announcementdetail/reliable-nepal-life-insurance-company-limited-has-published-an-offer-letter-to-issue-9600000-units-ipo-shares-to-the-general-public-from-23rd-shrawan-to-26th-shrawan-2080-2023-07-31',
                     'issue_manager': 'Civil Capital Market Ltd.', 'listing_date': '',
                     'displayable_share_type': 'Others', 'company': {'id': 737,
                                                                     'symbol': "<a href='https://www.sharesansar.com/company/renlicl'>RENLICL</a>",
                                                                     'companyname': "<a href='https://www.sharesansar.com/company/renlicl'>Reliable Nepal Life Insurance Limited</a>"},
                     'status': 1, 'bkstatus': 0,
                     'view': "<a href='https://www.sharesansar.com/announcementdetail/reliable-nepal-life-insurance-company-limited-has-published-an-offer-letter-to-issue-9600000-units-ipo-shares-to-the-general-public-from-23rd-shrawan-to-26th-shrawan-2080-2023-07-31' target='_blank'><i class='fa fa-file' aria-hidden='true'></i><a>",
                     'DT_Row_Index': 7},
                    {'companyid': 1224, 'ratio_value': None, 'total_units': '1953279.00', 'issue_price': '100.00',
                     'opening_date': '2023-08-03', 'closing_date': '2023-08-07', 'final_date': '2023-08-17',
                     'right_eligibility_link': None,
                     'announcement_link': 'https://www.sharesansar.com/announcementdetail/upper-lohore-khola-hydropower-company-limited-has-published-an-offer-letter-to-issue-1953279-units-ipo-shares-to-the-general-public-from-18th-shrawan-to-22nd-shrawan-2080-2023-07-27',
                     'issue_manager': 'NIC Asia Capital Ltd', 'listing_date': '', 'displayable_share_type': 'Others',
                     'company': {'id': 1224,
                                 'symbol': "<a href='https://www.sharesansar.com/company/ulkhcl'>ULKHCL</a>",
                                 'companyname': "<a href='https://www.sharesansar.com/company/ulkhcl'>Upper Lohore Khola Hydropower Company Limited</a>"},
                     'status': 1, 'bkstatus': 0,
                     'view': "<a href='https://www.sharesansar.com/announcementdetail/upper-lohore-khola-hydropower-company-limited-has-published-an-offer-letter-to-issue-1953279-units-ipo-shares-to-the-general-public-from-18th-shrawan-to-22nd-shrawan-2080-2023-07-27' target='_blank'><i class='fa fa-file' aria-hidden='true'></i><a>",
                     'DT_Row_Index': 8},
                    {'companyid': 1193, 'ratio_value': None, 'total_units': '12300200.00', 'issue_price': '237.58',
                     'opening_date': '', 'closing_date': '', 'final_date': '', 'right_eligibility_link': None,
                     'announcement_link': None, 'issue_manager': 'NIMB Ace Capital Limited', 'listing_date': '',
                     'displayable_share_type': 'Others',
                     'company': {'id': 1193, 'symbol': "<a href='https://www.sharesansar.com/company/smol'>SMOL</a>",
                                 'companyname': "<a href='https://www.sharesansar.com/company/smol'>Sonapur Minerals and Oil Limited</a>"},
                     'status': -2, 'bkstatus': -2, 'view': '<i class="fa fa-times" aria-hidden="true"></i>',
                     'DT_Row_Index': 9},
                    {'companyid': 1229, 'ratio_value': None, 'total_units': '1200000.00', 'issue_price': '100.00',
                     'opening_date': '', 'closing_date': '', 'final_date': '', 'right_eligibility_link': None,
                     'announcement_link': None, 'issue_manager': 'RBB Merchant Banking Ltd.', 'listing_date': '',
                     'displayable_share_type': 'Others',
                     'company': {'id': 1229, 'symbol': "<a href='https://www.sharesansar.com/company/chpl'>CHPL</a>",
                                 'companyname': "<a href='https://www.sharesansar.com/company/chpl'>Chirkhwa Hydro Power Limited</a>"},
                     'status': -2, 'bkstatus': -2, 'view': '<i class="fa fa-times" aria-hidden="true"></i>',
                     'DT_Row_Index': 10},
                    {'companyid': 966, 'ratio_value': None, 'total_units': '2500000.00', 'issue_price': '100.00',
                     'opening_date': '', 'closing_date': '', 'final_date': '', 'right_eligibility_link': None,
                     'announcement_link': None, 'issue_manager': 'Sanima Capital Ltd', 'listing_date': '',
                     'displayable_share_type': 'Others',
                     'company': {'id': 966, 'symbol': "<a href='https://www.sharesansar.com/company/mmkjl'>MMKJL</a>",
                                 'companyname': "<a href='https://www.sharesansar.com/company/mmkjl'>Mathillo Mailun Khola Jalvidhyut Limited</a>"},
                     'status': -2, 'bkstatus': -2, 'view': '<i class="fa fa-times" aria-hidden="true"></i>',
                     'DT_Row_Index': 11},
                    {'companyid': 1170, 'ratio_value': None, 'total_units': '1496800.00', 'issue_price': '100.00',
                     'opening_date': '', 'closing_date': '', 'final_date': '', 'right_eligibility_link': None,
                     'announcement_link': None, 'issue_manager': 'NIC Asia Capital Ltd', 'listing_date': '',
                     'displayable_share_type': 'Others',
                     'company': {'id': 1170, 'symbol': "<a href='https://www.sharesansar.com/company/mshcl'>MSHCL</a>",
                                 'companyname': "<a href='https://www.sharesansar.com/company/mshcl'>Mid Solu Hydropower Company Limited</a>"},
                     'status': -2, 'bkstatus': -2, 'view': '<i class="fa fa-times" aria-hidden="true"></i>',
                     'DT_Row_Index': 12},
                    {'companyid': 1022, 'ratio_value': None, 'total_units': '2925000.00', 'issue_price': '50.00',
                     'opening_date': '', 'closing_date': '', 'final_date': '', 'right_eligibility_link': None,
                     'announcement_link': None, 'issue_manager': 'Global IME Capital Limited', 'listing_date': '',
                     'displayable_share_type': 'Others',
                     'company': {'id': 1022, 'symbol': "<a href='https://www.sharesansar.com/company/hinl'>HINL</a>",
                                 'companyname': "<a href='https://www.sharesansar.com/company/hinl'>Hathway Investment Nepal Limited</a>"},
                     'status': -2, 'bkstatus': -2, 'view': '<i class="fa fa-times" aria-hidden="true"></i>',
                     'DT_Row_Index': 13},
                    {'companyid': 1199, 'ratio_value': None, 'total_units': '6911670.00', 'issue_price': '435.00',
                     'opening_date': '2023-07-07', 'closing_date': '2023-07-10', 'final_date': '2023-07-10',
                     'right_eligibility_link': None,
                     'announcement_link': 'https://www.sharesansar.com/announcementdetail/ghorahi-cement-industry-limited-has-published-an-offer-letter-to-issue-6911670-units-ipo-shares-to-the-general-public-from-32nd-jestha-to-4th-ashar-2080-2023-06-07',
                     'issue_manager': 'Himalayan Capital Ltd.', 'listing_date': '2023-08-10',
                     'displayable_share_type': 'Others',
                     'company': {'id': 1199, 'symbol': "<a href='https://www.sharesansar.com/company/gcil'>GCIL</a>",
                                 'companyname': "<a href='https://www.sharesansar.com/company/gcil'>Ghorahi Cement Industry Limited</a>"},
                     'status': 1, 'bkstatus': 0,
                     'view': "<a href='https://www.sharesansar.com/announcementdetail/ghorahi-cement-industry-limited-has-published-an-offer-letter-to-issue-6911670-units-ipo-shares-to-the-general-public-from-32nd-jestha-to-4th-ashar-2080-2023-06-07' target='_blank'><i class='fa fa-file' aria-hidden='true'></i><a>",
                     'DT_Row_Index': 14},
                    {'companyid': 1279, 'ratio_value': None, 'total_units': '101151.00', 'issue_price': '100.00',
                     'opening_date': '2023-07-11', 'closing_date': '2023-07-14', 'final_date': '2023-07-25',
                     'right_eligibility_link': None,
                     'announcement_link': 'https://www.sharesansar.com/announcementdetail/kutheli-bukhari-small-hydropower-limited-has-published-an-offer-letter-to-issue-101151-units-at-rs100-per-unit-to-the-general-public-from-26th-ashad-to-29th-ashad-2080-2023-06-29',
                     'issue_manager': 'NMB Capital Limited', 'listing_date': '2023-08-20',
                     'displayable_share_type': 'Others',
                     'company': {'id': 1279, 'symbol': "<a href='https://www.sharesansar.com/company/kbsh'>KBSH</a>",
                                 'companyname': "<a href='https://www.sharesansar.com/company/kbsh'>Kutheli Bukhari Small Hydropower Limited</a>"},
                     'status': 1, 'bkstatus': 0,
                     'view': "<a href='https://www.sharesansar.com/announcementdetail/kutheli-bukhari-small-hydropower-limited-has-published-an-offer-letter-to-issue-101151-units-at-rs100-per-unit-to-the-general-public-from-26th-ashad-to-29th-ashad-2080-2023-06-29' target='_blank'><i class='fa fa-file' aria-hidden='true'></i><a>",
                     'DT_Row_Index': 15},
                    {'companyid': 735, 'ratio_value': None, 'total_units': '9600000.00', 'issue_price': '236.91',
                     'opening_date': '2023-07-06', 'closing_date': '2023-07-10', 'final_date': '2023-07-20',
                     'right_eligibility_link': None,
                     'announcement_link': 'https://www.sharesansar.com/announcementdetail/ime-life-insurance-company-limited-has-published-an-offer-letter-to-issue-9600000-units-ipo-shares-to-the-general-public-from-20th-ashar-to-24th-ashar-and-1200000-units-ipo-shares-to-foreign-nepalese-migrants-from-1st-ashar-to-15th-ashar-2080-2023-06-09',
                     'issue_manager': 'Civil Capital Market Ltd.', 'listing_date': '2023-08-03',
                     'displayable_share_type': 'Others',
                     'company': {'id': 735, 'symbol': "<a href='https://www.sharesansar.com/company/ili'>ILI</a>",
                                 'companyname': "<a href='https://www.sharesansar.com/company/ili'>IME Life Insurance Company Limited</a>"},
                     'status': 1, 'bkstatus': 0,
                     'view': "<a href='https://www.sharesansar.com/announcementdetail/ime-life-insurance-company-limited-has-published-an-offer-letter-to-issue-9600000-units-ipo-shares-to-the-general-public-from-20th-ashar-to-24th-ashar-and-1200000-units-ipo-shares-to-foreign-nepalese-migrants-from-1st-ashar-to-15th-ashar-2080-2023-06-09' target='_blank'><i class='fa fa-file' aria-hidden='true'></i><a>",
                     'DT_Row_Index': 16},
                    {'companyid': 752, 'ratio_value': None, 'total_units': '539500.00', 'issue_price': '100.00',
                     'opening_date': '2023-06-25', 'closing_date': '2023-06-28', 'final_date': '2023-07-09',
                     'right_eligibility_link': None,
                     'announcement_link': 'https://www.sharesansar.com/announcementdetail/upper-syange-hydropower-limited-has-published-an-offer-letter-to-issue-539500-units-ipo-shares-to-the-general-public-from-10th-ashad-to-13th-ashad-2080-2023-06-16',
                     'issue_manager': 'Siddhartha Capital Limited', 'listing_date': '2023-08-10',
                     'displayable_share_type': 'Others',
                     'company': {'id': 752, 'symbol': "<a href='https://www.sharesansar.com/company/ushl'>USHL</a>",
                                 'companyname': "<a href='https://www.sharesansar.com/company/ushl'>Upper Syange Hydropower Limited</a>"},
                     'status': 1, 'bkstatus': 0,
                     'view': "<a href='https://www.sharesansar.com/announcementdetail/upper-syange-hydropower-limited-has-published-an-offer-letter-to-issue-539500-units-ipo-shares-to-the-general-public-from-10th-ashad-to-13th-ashad-2080-2023-06-16' target='_blank'><i class='fa fa-file' aria-hidden='true'></i><a>",
                     'DT_Row_Index': 17},
                    {'companyid': 871, 'ratio_value': None, 'total_units': '613162.00', 'issue_price': '100.00',
                     'opening_date': '2023-06-20', 'closing_date': '2023-06-23', 'final_date': '2023-07-04',
                     'right_eligibility_link': None,
                     'announcement_link': 'https://www.sharesansar.com/announcementdetail/three-star-hydropower-limited-has-published-an-offer-letter-to-issue-613162-units-ipo-shares-to-the-general-public-from-5th-ashad-to-8th-ashad-2080-2023-06-12#',
                     'issue_manager': 'Himalayan Capital Ltd', 'listing_date': '2023-08-10',
                     'displayable_share_type': 'Others',
                     'company': {'id': 871, 'symbol': "<a href='https://www.sharesansar.com/company/tshl'>TSHL</a>",
                                 'companyname': "<a href='https://www.sharesansar.com/company/tshl'>Three Star Hydropower Limited</a>"},
                     'status': 1, 'bkstatus': 0,
                     'view': "<a href='https://www.sharesansar.com/announcementdetail/three-star-hydropower-limited-has-published-an-offer-letter-to-issue-613162-units-ipo-shares-to-the-general-public-from-5th-ashad-to-8th-ashad-2080-2023-06-12#' target='_blank'><i class='fa fa-file' aria-hidden='true'></i><a>",
                     'DT_Row_Index': 18},
                    {'companyid': 1228, 'ratio_value': None, 'total_units': '4353000.00', 'issue_price': '100.00',
                     'opening_date': '2023-06-09', 'closing_date': '2023-06-13', 'final_date': '2023-06-23',
                     'right_eligibility_link': None,
                     'announcement_link': 'https://www.sharesansar.com/announcementdetail/nepal-republic-media-limited-has-published-an-offer-letter-to-issue-3525930-units-ipo-shares-to-the-general-public-from-26th-jestha-to-30th-jestha-and-435300-units-ipo-shares-to-foreign-nepalese-employees-from-31st-baisakh-to-14th-jestha-2080-2023-05-04',
                     'issue_manager': 'Mega Capital Markets Ltd.', 'listing_date': '2023-08-03',
                     'displayable_share_type': 'Others',
                     'company': {'id': 1228, 'symbol': "<a href='https://www.sharesansar.com/company/nrm'>NRM</a>",
                                 'companyname': "<a href='https://www.sharesansar.com/company/nrm'>Nepal Republic Media Limited</a>"},
                     'status': 1, 'bkstatus': 0,
                     'view': "<a href='https://www.sharesansar.com/announcementdetail/nepal-republic-media-limited-has-published-an-offer-letter-to-issue-3525930-units-ipo-shares-to-the-general-public-from-26th-jestha-to-30th-jestha-and-435300-units-ipo-shares-to-foreign-nepalese-employees-from-31st-baisakh-to-14th-jestha-2080-2023-05-04' target='_blank'><i class='fa fa-file' aria-hidden='true'></i><a>",
                     'DT_Row_Index': 19},
                    {'companyid': 1202, 'ratio_value': None, 'total_units': '643667.00', 'issue_price': '100.00',
                     'opening_date': '2023-06-01', 'closing_date': '2023-06-05', 'final_date': '2023-06-15',
                     'right_eligibility_link': None,
                     'announcement_link': 'https://www.sharesansar.com/announcementdetail/rawa-energy-development-limited-has-published-an-offer-letter-to-issue-643667units-at-rs100-per-unit-to-the-general-public-from-18th-jestha-to-22nd-jestha-2080-2023-05-22',
                     'issue_manager': 'Prabhu Capital Limited', 'listing_date': '2023-07-04',
                     'displayable_share_type': 'Others',
                     'company': {'id': 1202, 'symbol': "<a href='https://www.sharesansar.com/company/rawa'>RAWA</a>",
                                 'companyname': "<a href='https://www.sharesansar.com/company/rawa'>Rawa Energy Development Ltd.</a>"},
                     'status': 1, 'bkstatus': 0,
                     'view': "<a href='https://www.sharesansar.com/announcementdetail/rawa-energy-development-limited-has-published-an-offer-letter-to-issue-643667units-at-rs100-per-unit-to-the-general-public-from-18th-jestha-to-22nd-jestha-2080-2023-05-22' target='_blank'><i class='fa fa-file' aria-hidden='true'></i><a>",
                     'DT_Row_Index': 20}]
            logging.error("[2] Failed to get data from web 'JSONDecodeError'")
        ipos = self.get_ipos_opened_today(data)
        for ipo in ipos:
            company = ipo['company']
            company_symbol = self.search_company_details(company['symbol'])
            company_name = self.search_company_details(company['companyname'])
            closing_date = ipo['closing_date']
            compose_mail_message(self.sender_email, self.password, self.receivers_mail, company_symbol, company_name,
                                 closing_date)
        logging.info("[3] No Ipos for today")
        return "We don't have any IPO opening today"
