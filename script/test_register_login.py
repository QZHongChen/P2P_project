import logging
import time
import unittest
import requests
import random
import utils
from api.register_login_api import RegisterLoginAPI
from parameterized import parameterized
from data import test_data
from lib.UtilsDataBase import DataBaseUtils


class TestRegisterLogin(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     sql1 = "delete from mb_member_register_log where phone in ('15851779036','15851779037','15851779038','15851779039','15851779040','15851779041');"
    #     DataBaseUtils.execute_sql(sql1)
    #     logging.info("delete sql = {}".format(sql1))
    #     sql2 = "delete i.* from mb_member_login_log i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone in ('15851779036','15851779037','15851779038','15851779039','15851779040','15851779041');"
    #     DataBaseUtils.execute_sql(sql2)
    #     logging.info("delete sq2 = {}".format(sql2))
    #     sql3 = "delete i.* from mb_member_info i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone in ('15851779036','15851779037','15851779038','15851779039','15851779040','15851779041');"
    #     DataBaseUtils.execute_sql(sql3)
    #     logging.info("delete sq2 = {}".format(sql3))
    #     sql4 = "delete from mb_member WHERE phone in ('15851779036','15851779037','15851779038','15851779039','15851779040','15851779041');"
    #     DataBaseUtils.execute_sql(sql4)
    #     logging.info("delete sq2 = {}".format(sql4))

    def setUp(self):
        self.register_login_api = RegisterLoginAPI()
        self.session = requests.Session()

    def tearDown(self):
        self.session.close()

    # 随机小数，随机整数，空参数，随机字符串--注册获取图片验证码
    @parameterized.expand(test_data.img_code_data)
    def test01_img_code_random(self, number, status_code):
        response = self.register_login_api.get_img_verify_code(self.session, number)
        self.assertEqual(status_code, response.status_code)

    # 短信获取验证码
    @parameterized.expand(utils.get_sms_code_data())
    def test02_phone_code(self, status_code, status, description, phone, img_code):
        if img_code:
            self.register_login_api.get_img_verify_code(self.session, random.random())
            response = self.register_login_api.get_sms_code(self.session, phone, img_code)
            print(response.text)
            utils.assert_utils(self, response, status_code, status, description)
        else:
            response = self.register_login_api.get_sms_code(self.session, phone, img_code)
            print(response.text)
            utils.assert_utils(self, response, status_code, status, description)

    # 注册
    @parameterized.expand(utils.get_params_data("register.json", "test_register_data", "status_code, status, description, phone, password, img_code, phone_code, dy_server, invite_phone"))
    def test03_register(self, status_code, status, description, phone, password, img_code, phone_code, dy_server, invite_phone):
        self.register_login_api.get_img_verify_code(self.session, random.random())
        self.register_login_api.get_sms_code(self.session, phone, img_code)
        response = self.register_login_api.get_register(self.session, phone, password, img_code, phone_code, dy_server, invite_phone)
        print(response.text)
        utils.assert_utils(self, response, status_code, status, description)

    # 登录
    @parameterized.expand(test_data.BASE_LOGIN_DATA)
    def test04_login(self, status_code, status, description, phone, password):
        response = self.register_login_api.get_login(self.session, phone, password)
        print(response.text)
        utils.assert_utils(self, response, status_code, status, description)

    def test05_login_fail_02(self):
        response = self.register_login_api.get_login(self.session, test_data.register_phone, test_data.password_fail)
        print(response.text)
        utils.assert_utils(self, response, 200, 100, "密码错误1次,达到3次将锁定账户")

        response = self.register_login_api.get_login(self.session, test_data.register_phone, test_data.password_fail)
        print(response.text)
        utils.assert_utils(self, response, 200, 100, "密码错误2次,达到3次将锁定账户")

        response = self.register_login_api.get_login(self.session, test_data.register_phone, test_data.password_fail)
        print(response.text)
        utils.assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")

        response = self.register_login_api.get_login(self.session, test_data.register_phone, test_data.password_fail)
        print(response.text)
        utils.assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")

        time.sleep(60)
        response = self.register_login_api.get_login(self.session, test_data.register_phone, test_data.password)
        print(response.text)
        utils.assert_utils(self, response, 200, 200, "登录成功")



