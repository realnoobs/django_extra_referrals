from django.db import models
from django.utils import translation
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django_referrals.models import Referral, Transaction
from django_referrals.feeschema import FlatFeeSchema

_ = translation.ugettext_lazy


class Donation(models.Model):
    creator = models.ForeignKey(
        get_user_model(), null=True, blank=True,
        on_delete=models.CASCADE)
    referral = models.ForeignKey(Referral, null=True, blank=True, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    transaction = GenericRelation(Transaction, related_query_name='donations')

    def __str__(self):
        return self.creator.username


class Withdraw(models.Model):
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    referral = models.ForeignKey(Referral, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    checkout = GenericRelation(Transaction, related_query_name='withdraws')

    def __str__(self):
        return self.fullname
