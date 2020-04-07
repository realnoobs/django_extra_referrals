from django_referrals.feeschema import get_fee_schema
from django_referrals.models import Transaction


def make_commit(obj):
    model_name = str(obj._meta.model_name).title()
    amount = getattr(obj, 'amount', None)
    if not bool(amount):
        raise ValueError(
            "%s amount invalid" % model_name
        )

    creator = getattr(obj, 'creator', None)
    if not creator:
        return

    referral = getattr(creator, 'referral', None)
    if not referral:
        return

    uplines = referral.get_uplines()
    schema = get_fee_schema(referral)

    for idx in range(uplines.count()):
        fee_rate = schema.get_upline_rates()[idx]
        upline = uplines[idx]
        transaction = Transaction(
            content_object=obj,
            rate=fee_rate,
            amount=obj.amount,
            referral=upline,
            note='%s verified' % model_name
        )
        transaction.save()
        upline.update_balance(transaction.balance)


def make_cancel(obj, flow='IN'):
    model_name = str(obj._meta.model_name).title()
    reverse_flow = {'IN': 'OUT', 'OUT': 'IN'}
    if flow not in ['IN', 'OUT']:
        raise ValueError('flow must be IN or OUT')

    transactions = Transaction.objects.filter(object_id=obj.id, flow='IN')
    for trx in transactions:
        transaction = Transaction(
            flow=reverse_flow[flow],
            rate=trx.rate,
            amount=trx.amount,
            referral=trx.referral,
            content_object=obj,
            note='%s canceled' % model_name
        )
        transaction.save()
        trx.referral.update_balance(transaction.balance)


def make_withdraw(obj):
    model_name = str(obj._meta.model_name).title()
    amount = getattr(obj, 'amount', None)
    if not bool(amount):
        raise ValueError("%s amount invalid" % model_name)

    referral = getattr(obj, 'referral', None)
    if not referral:
        return

    transaction = Transaction(
        flow='OUT',
        content_object=obj,
        rate=100,
        amount=obj.amount,
        referral=referral,
        note='%s confirmed' % model_name
    )
    transaction.save()
    referral.update_balance(transaction.balance)
