import config


class CertifiedAccountOpenAPI:

    def __init__(self):
        self.url_certified = config.P2P_URL + "/member/realname/approverealname"
        self.url_certified_info = config.P2P_URL + "/member/member/getapprove"
        self.url_account_open = config.P2P_URL + "/trust/trust/register"

    # 认证
    def get_certified(self, session, realname, card_id):
        data = {
            "realname": realname,
            "card_id": card_id
        }
        # files={'x': 'y'}--> 构造多消息体格式的数据
        return session.post(self.url_certified, data, files={'x': 'y'})

    # 获取认证信息
    def get_certified_info(self, session):
        return session.post(self.url_certified_info)

    # 开户
    def account_open(self, session):
        return session.post(self.url_account_open)