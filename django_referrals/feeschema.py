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
