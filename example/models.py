from django.db import models
from django.utils import translation
from django_referrals.models import AbstractPayable, AbstractReceivable

_ = translation.ugettext_lazy


class Donation(AbstractReceivable):
    fullname = models.CharField(max_length=150)

    def __str__(self):
        return self.fullname


class Withdraw(AbstractPayable):
    fullname = models.CharField(max_length=150)

    def __str__(self):
        return self.fullname
