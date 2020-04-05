import decimal


class FeeSchema:
    referral = None

    def __init__(self, referral):
        self.referral = referral

    def get_rates(self):
        raise NotImplemented


class FlatFeeSchema(FeeSchema):
    """ Fee calculator for flat based fee"""
    rate_campaign = decimal.Decimal(5.0)
    rate_downline_0 = decimal.Decimal(5.0)
    rate_downline_1 = decimal.Decimal(2.0)
    rate_downline_2 = decimal.Decimal(1.0)

    def __init__(self, referral):
        super().__init__(referral)

    def get_rates(self):
        return [
            self.rate_downline_0,
            self.rate_downline_1,
            self.rate_downline_2,
        ]

    # def get_downline_fee(self, level=0):
    #     rate = self.get_rates()[level]
    #     fundraised = self.referral.get_fundraised_by_downlines(level=level)
    #     fee = (fundraised * rate) / 100
    #     return decimal.Decimal(fee)
    #
    # def get_campaign_fee(self):
    #     campaigns = self.referral.get_fundraised_by_campaigns()
    #     fee = (campaigns * self.rate_campaign) / 100
    #     return decimal.Decimal(fee)
    #
    # def calculate_upline_fee(self, amount, level):
    #     rate = self.get_rates()[level]
    #     return (amount * rate) / 100


class LevelFeeCalculator(FeeSchema):
    """ Fee calculator for level based fee by referral group"""

    def __init__(self, referral):
        super().__init__(referral)
