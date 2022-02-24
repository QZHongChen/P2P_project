import random
import unittest
import requests
from parameterized import parameterized
import utils
from api.recharge_api import RechargeAPI
from api.register_login_api import RegisterLoginAPI
from data import test_data


class TestRecharge(unittest.TestCase):

    def setUp(self):
        self.register_login_api = RegisterLoginAPI()
        self.recharge_api = RechargeAPI()
        self.session = requests.Session()

    def tearDown(self):
        self.session.close()

    # 获取充值验证码
    @parameterized.expand(test_data.img_code_data)
    def test01_get_recharge_img_code(self, number, status_code):
        self.register_login_api.get_login(self.session, test_data.register_phone, test_data.password)
        response = self.recharge_api.get_recharge_img_code(self.session, number)
        print(response.text)
        self.assertEqual(status_code, response.status_code)

    # 充值
    @parameterized.expand(test_data.BASE_RECHARGE)
    def test02_recharge(self, phone, password, number, amount, valicode, status_code, status, description):
        self.register_login_api.get_login(self.session, phone, password)
        self.recharge_api.get_recharge_img_code(self.session, number)
        response = self.recharge_api.recharge(self.session, amount, valicode)
        print(response.text)
        self.assertEqual(status_code, response.status_code)
        self.assertEqual(status, response.json().get("status"))
        if status == 200:
            self.assertIn(description, response.json().get("description").get("form"))
        else:
            self.assertIn(description, response.json().get("description"))

    def test03_get_third_party_recharge(self):
        self.register_login_api.get_login(self.session, test_data.register_phone, test_data.password)
        self.recharge_api.get_recharge_img_code(self.session, random.random())
        response = self.recharge_api.recharge(self.session, 10000000, 8888)
        data = utils.get_third_party_data(response)
        print(data)
        response = self.session.post(data[0], data[1])
        self.assertEqual(200, response.status_code)
        self.assertEqual("NetSave OK", response.text)

