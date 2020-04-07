from django.conf import settings
from django.apps import apps

REFERRAL_MODEL = getattr(settings, 'REFERRAL_MODEL', 'django_referrals.Referral')
REFERRAL_COOKIE_KEY = getattr(settings, 'REFERRAL_COOKIE_KEY', 'ref_id')
REFERRAL_PARAM_KEY = getattr(settings, 'REFERRAL_PARAM_KEY', 'ref_id')
REFERRAL_MAX_DAY = getattr(settings, 'REFERRAL_COOKIE_AGE', 7 * 24 * 60 * 60)


class ReferralLinkMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        Referral = apps.get_model(REFERRAL_MODEL, require_ready=True)
        cookie_age = REFERRAL_MAX_DAY
        response = self.get_response(request)
        cookie = request.COOKIES.get(REFERRAL_COOKIE_KEY)
        if cookie:
            try:
                response.referral = Referral.objects.get(pk=cookie)
            except Exception as err:
                pass
        if not cookie and request.method == 'GET' and REFERRAL_PARAM_KEY in request.GET:
            ref_id = request.GET.get(REFERRAL_PARAM_KEY)
            try:
                response.referral = Referral.objects.get(inner_id=ref_id)
                response.set_cookie(REFERRAL_PARAM_KEY, str(response.referral.id).replace('-', ''), max_age=cookie_age)
            except Referral.DoesNotExist:
                pass
        return response
