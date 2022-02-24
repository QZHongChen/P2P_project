import unittest
import time
from lib.HTMLTestRunner import HTMLTestRunner
from script.test_bidding_process import TestBiddingProcess
from script.test_certified_account_open import TestCertifiedAccountOpen
from script.test_register_login import TestRegisterLogin
from script.test_recharge import TestRecharge
from script.test_investment_manage import TestInvestmentManage
import config

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestRegisterLogin))
suite.addTest(unittest.makeSuite(TestCertifiedAccountOpen))
suite.addTest(unittest.makeSuite(TestRecharge))
suite.addTest(unittest.makeSuite(TestInvestmentManage))
suite.addTest(unittest.makeSuite(TestBiddingProcess))

fileName = config.BASE_DIR + "/report/report{}.html".format(time.strftime("%Y%m%d-%H%M%S"))
with open(fileName, "wb") as f:
    runner = HTMLTestRunner(f, title="金融项目测试报告")
    runner.run(suite)
