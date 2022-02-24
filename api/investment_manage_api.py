import config


class InvestmentManageAPI:

    def __init__(self):
        self.url_investment = config.P2P_URL + "/trust/trust/tender"
        self.url_risk_assessment = config.P2P_URL + " /risk/answer/submit"
        self.url_get_tender_list = config.P2P_URL + "/loan/tender/mytenderlist"

    # 投资
    def investment(self, session, depositCertificate, amount):
        data = {
            "id": 1324,
            "depositCertificate": depositCertificate,
            "amount": amount
        }
        return session.post(self.url_investment, data)

    # 风险测评
    def set_risk_assessment(self, session, answers_1, answers_2, answers_3, answers_4, answers_5, answers_6, answers_7, answers_8, answers_9, answers_10):
        data = {
            "answers_1": answers_1,
            "answers_2": answers_2,
            "answers_3": answers_3,
            "answers_4": answers_4,
            "answers_5": answers_5,
            "answers_6": answers_6,
            "answers_7": answers_7,
            "answers_8": answers_8,
            "answers_9": answers_9,
            "answers_10": answers_10
        }
        return session.post(self.url_risk_assessment, data)

    # 获取投资列表
    def get_tender_list(self, session, page, status):
        data = {
            "page": page,
            "status": status
        }
        return session.post(self.url_get_tender_list, data)

