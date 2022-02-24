import config


class RechargeAPI:

    def __init__(self):
        self.url_recharge_img_code = config.P2P_URL + "/common/public/verifycode/"
        self.url_recharge = config.P2P_URL + "/trust/trust/recharge"

    #  充值-获取图图片验证码
    def get_recharge_img_code(self, session, number):
        return session.get(self.url_recharge_img_code + str(number))

    # 充值
    def recharge(self, session, amount, valicode):
        data = {
            "paymentType": "chinapnrTrust",
            "formStr": "reForm",
            "amount": str(amount),
            "valicode": str(valicode)
        }
        return session.post(self.url_recharge, data=data)


