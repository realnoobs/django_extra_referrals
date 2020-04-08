from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

SCHEMA_AVAILABLE = ['FLAT']
REFERRAL_SCHEMA = getattr(settings, 'REFERRAL_SCHEMA', 'FLAT')
REFERRAL_FLAT_CAMPAIGN_RATE = getattr(settings, 'REFERRAL_CAMPAIGN_RATE', 4)
REFERRAL_FLAT_UPLINES_RATE = getattr(settings, 'REFERRAL_UPLINES_RATE', [5, 2, 1])

if REFERRAL_SCHEMA not in SCHEMA_AVAILABLE:
    raise ImproperlyConfigured(
        'Please make sure REFERRAL_SCHEMA is one of {}'.format(
            ",".join(SCHEMA_AVAILABLE)
        )
    )


class FeeSchema:
    referral = None

    def __init__(self, referral=None):
        self.referral = referral

    def get_upline_rates(self):
        raise NotImplemented

    def get_campaign_rates(self):
        raise NotImplemented


class FlatFeeSchema(FeeSchema):
    """ Fee calculator for flat based fee"""

    CAMPAIGN_RATE = REFERRAL_FLAT_CAMPAIGN_RATE
    UPLINES_RATE = REFERRAL_FLAT_UPLINES_RATE

    def __init__(self, referral=None):
        super().__init__(referral)

    def get_upline_rates(self):
        return FlatFeeSchema.UPLINES_RATE

    def get_campaign_rates(self):
        return FlatFeeSchema.CAMPAIGN_RATE


def get_fee_schema_class():
    schema_class = {
        'FLAT': FlatFeeSchema
    }
    return schema_class[REFERRAL_SCHEMA]
