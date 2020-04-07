from django.db import models
from django.utils import translation
from django_referrals.models import AbstractPayable, AbstractReceivable

_ = translation.ugettext_lazy


class Donation(AbstractReceivable):
    class Meta:
        abstract = True

    fullname = models.CharField(max_length=150)

    def __str__(self):
        return self.fullname


class Withdraw(AbstractPayable):
    class Meta:
        abstract = True

    fullname = models.CharField(max_length=150)

    def __str__(self):
        return self.fullname
