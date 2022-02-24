import json
import logging
import os
import random
import re
from datetime import time
from logging import handlers

import config


# 获取随机字符串
def get_string():
    array = random.sample('zyxwvutsrqponmlkjihgfedcba', 9)
    string = ""
    for i in array:
        string = string + i
    return string


# 初始化日志配置
def init_logger():
    # 1、初始化日志对象
    logger = logging.getLogger()
    # 2、设置日志级别
    logger.setLevel(logging.INFO)
    # 3、创建控制台日志处理器和文件日志处理器
    sh = logging.StreamHandler()

    # 创建文件处理器
    file_name = config.BASE_DIR + os.sep + "log" + os.sep + "P2P{}.log".format(time.strftime("%Y%m%d-%H%M%S"))
    fh = handlers.TimedRotatingFileHandler(file_name, when="M", interval=3, backupCount=5, encoding="UTF-8")
    # 4、设置日志格式，创建格式化器
    fmt = '%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:% (lineno)d)] - %(message)s'
    formatter = logging.Formatter(fmt)
    # 5、将格式化器设置到日志器中
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)
    # 6、将日志处理器添加到日志对象
    logger.addHandler(sh)
    logger.addHandler(fh)


# 获取短信验证码数据
def get_sms_code_data():
    sms_code_data = []
    file_path = config.BASE_DIR + "\data\sms_code_data.json"
    with open(file_path, encoding="utf-8") as file:
        json_data = json.load(file)
        for data in json_data:
            status_code = data.get("status_code")
            status = data.get("status")
            description = data.get("description")
            phone = data.get("phone")
            img_code = data.get("imgVerifyCode")
            sms_code_data.append((status_code, status, description, phone, img_code))
    return sms_code_data


def assert_utils(self, response, status_code, status, description):
    self.assertEqual(status_code, response.status_code)
    self.assertEqual(status, response.json().get("status"))
    self.assertEqual(description, response.json().get("description"))


# 请求第三方的函数
def get_third_party_data(response):
    data = []
    description = {}
    form = response.json().get("description").get("form")
    url = re.findall(r"method='post' action='(.+?)'><input name", form)[0]
    json_data = re.findall(r"<input name='(.+?)' type='hidden' value='(.+?)'/>", form)
    for i in json_data:
        description[i[0]] = i[1]
    data.append(url)
    data.append(description)
    return data


def get_params_data(file_name, method_name, params_name):
    params_data = []
    file_path = config.BASE_DIR + "/data/" + file_name
    with open(file_path, encoding="utf-8") as file:
        json_data = json.load(file).get(method_name)
        for data in json_data:
            case = []
            for string in params_name.split(", "):
                case.append(data.get(string))
            params_data.append(case)
    return params_data


s = "status_code, status, description, phone, password, img_code, phone_code, dy_server, invite_phone"
string = s.split(", ")
print(string)
print(get_params_data("register.json", "test_register_data", "status_code, status, description, phone, password, img_code, phone_code, dy_server, invite_phone"))