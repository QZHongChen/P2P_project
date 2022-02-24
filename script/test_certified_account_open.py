import unittest
import requests
import utils
from api.certified_account_open_api import CertifiedAccountOpenAPI
from api.register_login_api import RegisterLoginAPI
from parameterized import parameterized
import re

from data import test_data


class TestCertifiedAccountOpen(unittest.TestCase):

    def setUp(self):
        self.register_login_api = RegisterLoginAPI()
        self.certified_account_open = CertifiedAccountOpenAPI()
        self.session = requests.Session()

    def tearDown(self):
        self.session.close()

    @parameterized.expand(test_data.BASE_CERTIFIED)
    def test01_certified(self, phone, password, realname, card_id, status_code, status, description):
        response = self.register_login_api.get_login(self.session, phone, password)
        print(response.text)
        response = self.certified_account_open.get_certified(self.session, realname, card_id)
        print(response.text)
        utils.assert_utils(self, response, status_code, status, description)

    def test02_get_certified_info_success(self):
        self.register_login_api.get_login(self.session, test_data.register_phone, test_data.password)
        self.certified_account_open.get_certified(self.session, "小徐", "350781196403078763")
        response = self.certified_account_open.get_certified_info(self.session)
        print(response.text)
        self.assertEqual(200, response.status_code)
        self.assertEqual("-1", response.json().get("is_email_open"))

    def test03_get_certified_info_fail(self):
        self.register_login_api.get_login(self.session, test_data.register_phone5, test_data.password)
        self.certified_account_open.get_certified(self.session, "", "")
        response = self.certified_account_open.get_certified_info(self.session)
        print(response.text)
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))

    # 开户成功
    def test04_get_account_open(self):
        self.register_login_api.get_login(self.session, test_data.register_phone, test_data.password)
        self.certified_account_open.get_certified(self.session, test_data.realname, test_data.card_id)
        response = self.certified_account_open.account_open(self.session)
        print(response.text)
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))

    # 请求第三方开户成功
    def test05_get_third_party_account_open(self):
        self.register_login_api.get_login(self.session, test_data.register_phone, test_data.password)
        self.certified_account_open.get_certified(self.session, test_data.realname, test_data.card_id)
        response = self.certified_account_open.account_open(self.session)
        data = utils.get_third_party_data(response)
        print(data)
        response = self.session.post(data[0], data[1])
        self.assertEqual(200, response.status_code)
        self.assertEqual("UserRegister OK", response.text)


