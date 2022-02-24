import config


class RegisterLoginAPI:

    def __init__(self):
        self.url_img_verify_code = config.P2P_URL + "/common/public/verifycode1/"
        self.url_sms_code = config.P2P_URL + "/member/public/sendSms"
        self.url_register = config.P2P_URL + "/member/public/reg"
        self.url_login = config.P2P_URL + "/member/public/login"

    # 获取图片验证码
    def get_img_verify_code(self, session, number):
        url = self.url_img_verify_code + str(number)
        return session.get(url)

    # 获取短信验证码
    def get_sms_code(self, session, phone, img_code):
        data = {
            "phone": phone,
            "imgVerifyCode": img_code,
            "type": "reg"
        }
        return session.post(url=self.url_sms_code, params=data)

    # 注册
    def get_register(self, session, phone, password, verifycode="8888", phone_code="666666", dy_server="on", invite_phone="19651775177"):
        data = {
            "phone": phone,
            "password": password,
            "verifycode": verifycode,
            "phone_code": phone_code,
            "dy_server": dy_server,
            "invite_phone": invite_phone
        }
        return session.post(url=self.url_register, params=data)

    # 登录
    def get_login(self, session, phone, password):
        data = {
            "keywords": phone,
            "password": password
        }
        return session.post(self.url_login, data)
