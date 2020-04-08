from django_extra_referrals.utils.version import get_version

default_app_config = 'django_extra_referrals.apps.AppConfig'

# major.minor.patch.release.number
# release must be one of alpha, beta, rc, or final
VERSION = (0, 0, 2, 'alpha', 1)

__version__ = get_version(VERSION)
