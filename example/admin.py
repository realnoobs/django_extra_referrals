from django.db import transaction
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import reverse

from django_referrals.views import (
    receive_referral_balance,
    send_referral_balance,
    cancel_referral_transaction,
)

from .models import Donation, Withdraw


class DonationAdmin(admin.ModelAdmin):
    list_display = ['inner_id', 'fullname', 'amount', 'creator', 'referral', 'is_paid', 'is_cancelled']
    actions = ['confirm_donation', 'cancel_donation']

    def confirm_donation(self, request, queryset):
        with transaction.atomic():
            qs = queryset.filter(is_paid=False)
            for donation in qs:
                receive_referral_balance(donation)
                donation.is_paid = True
                donation.save()

    confirm_donation.short_description = 'Confirm donations'

    def cancel_donation(self, request, queryset):
        with transaction.atomic():
            qs = queryset.filter(is_paid=True)
            for donation in qs:
                if donation.creator:
                    cancel_referral_transaction(donation, flow='IN')
                donation.is_paid = False
                donation.is_cancelled = True
                donation.save()

    cancel_donation.short_description = 'Cancel donations'

    def has_change_permission(self, request, obj=None):
        if obj:
            return not obj.is_cancelled
        return super().has_change_permission(request, obj)


class WithdrawAdmin(admin.ModelAdmin):
    list_display = ['inner_id', 'fullname', 'amount', 'creator', 'referral', 'is_paid', 'is_cancelled']
    actions = ['confirm_withdraw', 'cancel_withdraw']

    def confirm_withdraw(self, request, queryset):
        """ Confirm withdraw, post referral transaction """
        with transaction.atomic():
            qs = queryset.filter(is_paid=False)
            for withdraw in qs:
                if withdraw.referral:
                    send_referral_balance(withdraw)
                withdraw.is_paid = True
                withdraw.save()

    def cancel_withdraw(self, request, queryset):
        """ Cancel withdraw """
        with transaction.atomic():
            qs = queryset.filter(is_paid=True)
            for withdraw in qs:
                cancel_referral_transaction(withdraw, flow='OUT')
                withdraw.is_paid = False
                withdraw.is_cancelled = True
                withdraw.save()

    cancel_withdraw.short_description = 'Cancel withdraw'


admin.site.register(Donation, DonationAdmin)
admin.site.register(Withdraw, WithdrawAdmin)
