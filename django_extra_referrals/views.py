from django.utils import timezone
from .feeschema import get_fee_schema_class
from .models import Transaction


def post_referral_transaction(obj, referral, rate, flow):
    opts = obj._meta
    transaction = Transaction(
        flow=flow,
        content_object=obj,
        rate=rate,
        amount=obj.amount,
        referral=referral,
        is_verified=True,
        verified_at=timezone.now(),
        note='%s %s committed' % (opts.model_name.title(), obj.inner_id)
    )
    transaction.save()
    referral.update_balance(transaction.balance)


def receive_referral_balance(obj):
    opts = obj._meta
    referral = getattr(obj, 'referral', None)
    campaingner = getattr(obj, 'campaingner', None)
    amount = getattr(obj, 'amount', None)

    if not bool(amount):
        raise ValueError("%s amount invalid" % opts.model_name.title())

    if referral:
        uplines = referral.get_uplines()
        schema = get_fee_schema_class()(referral)
        for idx in range(uplines.count()):
            rate = schema.get_upline_rates()[idx]
            upline = uplines[idx]
            post_referral_transaction(obj, upline, rate, 'IN')

    if campaingner and not referral:
        Schema = get_fee_schema_class()
        rate = Schema.CAMPAIGN_RATE
        post_referral_transaction(obj, campaingner, rate, 'IN')

    obj.is_paid = True
    obj.save()


def send_referral_balance(obj):
    model_name = str(obj._meta.model_name).title()
    amount = getattr(obj, 'amount', None)
    if not bool(amount):
        raise ValueError("%s amount invalid" % model_name)

    referral = getattr(obj, 'referral', None)
    if not referral:
        return

    if amount > referral.balance:
        raise ValueError("%s amount too large, %s balance is %s" % (
            model_name, str(referral.account), referral.balance
        ))

    post_referral_transaction(obj, referral, 100, 'OUT')
    obj.is_paid = True
    obj.save()


def cancel_referral_transaction(obj, flow):
    opts = obj._meta
    reverse_flow = {'IN': 'OUT', 'OUT': 'IN'}

    if flow not in ['IN', 'OUT']:
        raise ValueError('flow must be IN or OUT')

    transactions = obj.transaction.filter(flow=flow)
    for trx in transactions:
        if reverse_flow[flow] == 'OUT' and trx.total > trx.referral.balance:
            raise ValueError("%s amount too large, %s balance is %s" % (
                opts.model_name, str(trx.referral.account), trx.referral.balance
            ))
        post_referral_transaction(obj, trx.referral, trx.rate, reverse_flow[flow])

    obj.is_paid = False
    obj.is_cancelled = True
    obj.save()