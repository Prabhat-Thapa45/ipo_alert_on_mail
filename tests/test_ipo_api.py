from unittest.mock import patch

from src.ipo_details import Ipo

data = [{'companyid': 1138, 'ratio_value': None, 'total_units': '712220.00', 'issue_price': '116.00', 'opening_date': '2023-08-30', 'closing_date': '2023-09-01', 'final_date': '2023-09-05', 'right_eligibility_link': None, 'announcement_link': 'https://www.sharesansar.com/announcementdetail/bhagawati-hydropower-development-company-limited-has-published-an-offer-letter-to-issue-712220-units-ipo-shares-to-the-general-public-from-bhadra-5-8-2080-2023-08-14', 'issue_manager': 'Siddhartha Capital Ltd', 'listing_date': '', 'displayable_share_type': 'Others', 'company': {'id': 1138, 'symbol': "<a href='https://www.sharesansar.com/company/bhpdcl'>BHPDCL</a>", 'companyname': "<a href='https://www.sharesansar.com/company/bhpdcl'>Bhagawati Hydropower Development Company Limited</a>"}}]


class TestIpo():
    ipo = Ipo()
    # when ipo is opened the today
    def test_check_opening_date(self):
        details = self.ipo.get_ipos_opened_today(data)
        assert details
        self.details = details

    def test_search_company_details(self):
        # WHEN symbol is passed
        # THEN the company's symbol is returned similarly for companyname
        assert self.ipo.search_company_details(data[0]['company']['symbol']) == "BHPDCL"
        assert self.ipo.search_company_details(data[0]['company']['companyname']) == "Bhagawati Hydropower Development Company Limited"


    @patch("src.mail.compose_mail_message")
    @patch("src.ipo_details.Ipo.get_data_from_web")
    def test_handler(self, mock_get_data_from_web, mock_compose_mail_message):
        mock_get_data_from_web.return_value = data
        self.ipo.handler()
        assert mock_compose_mail_message.called_once()

