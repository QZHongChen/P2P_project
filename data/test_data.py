import random
import utils

# 注册、充值获取图片验证码
img_code_data = [(random.random(), 200), (random.randint(100000000, 999999999), 200), ("", 404), (utils.get_string(), 400)]

register_phone = "15851779036"
register_phone2 = "15851779037"
register_phone3 = "15851779038"
register_phone4 = "15851779039"
register_phone5 = "15851779040"
register_phone6 = "15851779041"
password = "xq123456"
# 注册测试数据
BASE_REGISTER_DATA = [(200, 200, "注册成功", register_phone, password, 8888, 666666, "on", ""),
                      (200, 200, "注册成功", register_phone2, password, 8888, 666666, "on", "19651775177"),
                      (200, 100, "验证码错误!", register_phone3, password, 8889, 666666, "on", ""),
                      (200, 100, "验证码错误", register_phone3, password, 8888, 666667, "on", ""),
                      (200, 100, "手机已存在!", register_phone, password, 8888, 666666, "on", ""),
                      (200, 100, "密码不能为空", register_phone4, "", 8888, 666666, "on", ""),
                      (200, 100, "请同意我们的条款", register_phone5, password, 8888, 666666, "off", "")]

password_fail = "xq12345"
# 登录测试数据
BASE_LOGIN_DATA = [(200, 200, "登录成功", register_phone, "xq123456"),
                   (200, 100, "用户不存在", "17558581314", "xq123456")]

realname = "小徐"
realname2 = "金王"
card_id = "130102199003078312"
card_id2 = "130102199003071110"
# 实名认证数据
BASE_CERTIFIED = [(register_phone, password, realname, card_id, 200, 200, "提交成功!"),
                  (register_phone2, password, "", card_id2, 100, 100, "姓名不能为空"),
                  (register_phone2, password, realname2, "error", 100, 100, "身份证号格式错误"),
                  (register_phone5, password, realname2, "", 100, 100, "身份证号不能为空"),
                  (register_phone2, password, realname2, card_id, 100, 100, "身份证号已被认证")]

# 充值数据--phone, password, number, amount, valicode, status_code, status, description
BASE_RECHARGE = [(register_phone, password, random.random(), 10000000, 8888, 200, 200, "form"),
                 (register_phone, password, random.random(), 10000000, "", 200, 100, "验证码错误"),
                 (register_phone, password, random.random(), 10000000, "8889", 200, 100, "验证码错误")]

# 投资测试数据--phone, password, depositCertificate, amount, status_code, status, description
BASE_INVESTMENT = [(register_phone, password, -1, 100, 200, 200, "form"),
                   (register_phone, password, -1, "", 200, 100, "不是正确的金额"),
                   (register_phone, password, "", 100, 200, 100, "投资密码不能为空"),
                   (register_phone, password, -1, 1000000000, 200, 100, "投标金额不能超过最高投标金额")]

# 获取投资列表数据-phone, password, page, status, status_code, status_name, isCert
BASE_TENDER_LIST = [(register_phone, password, 1, "recover", 200, "回款中", "2"),
                    (register_phone, password, 1, "tender", 200, "投标中", "2"),
                    (register_phone, password, 1, "recover_yes", 200, "已结清", "2"),
                    (register_phone, password, 1, "over", 200, "已流标", "2")]

