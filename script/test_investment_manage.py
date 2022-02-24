import re
import unittest
import requests
from parameterized import parameterized

import utils
from api.register_login_api import RegisterLoginAPI
from api.investment_manage_api import InvestmentManageAPI
from data import test_data


class TestInvestmentManage(unittest.TestCase):

    def setUp(self):
        self.register_login_api = RegisterLoginAPI()
        self.investment_manage_api = InvestmentManageAPI()
        self.session = requests.session()

    def tearDown(self):
        self.session.close()

    # 投资
    @parameterized.expand(test_data.BASE_INVESTMENT)
    def test01_investment(self, phone, password, depositCertificate, amount, status_code, status, description):
        self.register_login_api.get_login(self.session, phone, password)
        response = self.investment_manage_api.investment(self.session, depositCertificate, amount)
        print(response.text)
        self.assertEqual(status_code, response.status_code)
        self.assertEqual(status, response.json().get("status"))
        if status == 200:
            self.assertIn(description, response.json().get("description").get("form"))
        else:
            self.assertEqual(description, response.json().get("description"))

    # 请求第三方投资
    def test02_get_third_party_investment(self):
        self.register_login_api.get_login(self.session, test_data.register_phone, test_data.password)
        response = self.investment_manage_api.investment(self.session, -1, 100)
        data = utils.get_third_party_data(response)
        print(data)
        response = self.session.post(data[0], data[1])
        self.assertEqual(200, response.status_code)
        self.assertEqual("InitiativeTender OK", response.text)

    @parameterized.expand(test_data.BASE_TENDER_LIST)
    def test03_get_tender_list(self, phone, password, page, status, status_code, status_name, isCert):
        self.register_login_api.get_login(self.session, phone, password)
        response = self.investment_manage_api.get_tender_list(self.session, page, status)
        print(response.text)
        self.assertEqual(status_code, response.status_code)
        if response.json().get("items"):
            self.assertEqual(status_name, response.json().get("items")[0].get("status_name"))
            print(response.json().get("items")[0].get("status_name"))
        self.assertEqual(isCert, response.json().get("isCert"))