# Django Extra Referrals
Simpel referrals app for Django with simple multilevel fee system
## Installation
```
$ pip install django-extra-referrals
```
or
```
$ pip install git+https://github.com/sasriawesome/django_extra_referrals.git#egg=django-extra-referrals
```

## Settings

```
REFERRAL_MODEL = 'django_extra_referrals.Referral'
REFERRAL_COOKIE_KEY = 'ref_id'
REFERRAL_PARAM_KEY = 'ref_id
REFERRAL_MAX_DAY = 7 * 24 * 60 * 60 # a week
REFERRAL_SCHEMA = 'FLAT'
REFERRAL_FLAT_CAMPAIGN_RATE = 4
REFERRAL_FLAT_UPLINES_RATE = [5, 2, 1]

```