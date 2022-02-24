import logging
import random
import unittest
from lib.UtilsDataBase import DataBaseUtils
import requests
import utils
from api.investment_manage_api import InvestmentManageAPI
from api.certified_account_open_api import CertifiedAccountOpenAPI
from api.recharge_api import RechargeAPI
from api.register_login_api import RegisterLoginAPI
from data import test_data


class TestBiddingProcess(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.registerLoginAPI = RegisterLoginAPI()
        cls.certifiedAccountOpenAPI = CertifiedAccountOpenAPI()
        cls.rechargeAPI = RechargeAPI()
        cls.investmentManageAPI = InvestmentManageAPI()
        cls.session = requests.Session()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        sql1 = "delete from mb_member_register_log where phone in ('15851779036','15851779037','15851779038','15851779039','15851779040','15851779041');"
        DataBaseUtils.execute_sql(sql1)
        logging.info("delete sql = {}".format(sql1))
        sql2 = "delete i.* from mb_member_login_log i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone in ('15851779036','15851779037','15851779038','15851779039','15851779040','15851779041');"
        DataBaseUtils.execute_sql(sql2)
        logging.info("delete sq2 = {}".format(sql2))
        sql3 = "delete i.* from mb_member_info i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone in ('15851779036','15851779037','15851779038','15851779039','15851779040','15851779041');"
        DataBaseUtils.execute_sql(sql3)
        logging.info("delete sq2 = {}".format(sql3))
        sql4 = "delete from mb_member WHERE phone in ('15851779036','15851779037','15851779038','15851779039','15851779040','15851779041');"
        DataBaseUtils.execute_sql(sql4)
        logging.info("delete sq2 = {}".format(sql4))

    def test01_register(self):
        # 注册--图片验证码
        response = self.registerLoginAPI.get_img_verify_code(self.session, random.random())
        self.assertEqual(200, response.status_code)
        # 注册--短信验证码
        response = self.registerLoginAPI.get_sms_code(self.session, test_data.register_phone6, "8888")
        print(response.text)
        utils.assert_utils(self, response, 200, 200, "短信发送成功")
        # 注册
        response = self.registerLoginAPI.get_register(self.session, test_data.register_phone6, test_data.password)
        print(response.text)
        utils.assert_utils(self, response, 200, 200, "注册成功")

    def test02_get_login(self):
        # 登录
        response = self.registerLoginAPI.get_login(self.session, test_data.register_phone6, test_data.password)
        print(response.text)
        utils.assert_utils(self, response, 200, 200, "登录成功")

    def test03_get_certified(self):
        self.registerLoginAPI.get_login(self.session, test_data.register_phone6, test_data.password)
        # 认证
        response = self.certifiedAccountOpenAPI.get_certified(self.session, "君君", "350781196403075044")
        print(response.text)
        utils.assert_utils(self, response, 200, 200, "提交成功!")
        # 获取认证信息
        response = self.certifiedAccountOpenAPI.get_certified_info(self.session)
        print(response.text)
        self.assertEqual(200, response.status_code)
        self.assertEqual("-1", response.json().get("is_email_open"))

    def test04_account_open(self):
        self.registerLoginAPI.get_login(self.session, test_data.register_phone6, test_data.password)
        # 开户
        response = self.certifiedAccountOpenAPI.account_open(self.session)
        print(response.text)
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 第三方开户请求
        data = utils.get_third_party_data(response)
        print(data)
        response = self.session.post(data[0], data[1])
        self.assertEqual(200, response.status_code)
        self.assertEqual("UserRegister OK", response.text)
        print(response.text)

    def test05_get_recharge(self):
        self.registerLoginAPI.get_login(self.session, test_data.register_phone6, test_data.password)
        # 获取充值验证码
        response = self.rechargeAPI.get_recharge_img_code(self.session, random.random())
        self.assertEqual(200, response.status_code)
        # 充值
        response = self.rechargeAPI.recharge(self.session, 10000000, 8888)
        print(response.text)
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        self.assertIn("form", response.json().get("description").get("form"))
        # 第三方充值请求
        data = utils.get_third_party_data(response)
        print(data)
        response = self.session.post(data[0], data[1])
        self.assertEqual(200, response.status_code)
        self.assertEqual("NetSave OK", response.text)

    def test06_bidding_progress(self):
        self.registerLoginAPI.get_login(self.session, test_data.register_phone6, test_data.password)
        # 投资
        response = self.investmentManageAPI.investment(self.session, -1, 100)
        print(response.text)
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        self.assertIn("form", response.json().get("description").get("form"))
        # 第三方投资请求
        data = utils.get_third_party_data(response)
        print(data)
        response = self.session.post(data[0], data[1])
        self.assertEqual(200, response.status_code)
        self.assertEqual("InitiativeTender OK", response.text)
        # 获取投资列表
        response = self.investmentManageAPI.get_tender_list(self.session, 1, "tender")
        print(response.text)
        self.assertEqual(200, response.status_code)
        if response.json().get("items"):
            self.assertEqual("投标中", response.json().get("items")[0].get("status_name"))
            print(response.json().get("items")[0].get("status_name"))
        self.assertEqual("2", response.json().get("isCert"))



