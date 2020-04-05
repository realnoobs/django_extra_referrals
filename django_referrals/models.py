import uuid
import enum
import decimal
from django.db import models
from django.db.models.functions import Coalesce
from django.db.utils import cached_property
from django.apps import apps
from django.utils import timezone, translation
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

from django_numerators.models import NumeratorMixin
from mptt.models import MPTTModel, TreeForeignKey, TreeManager
from polymorphic.models import PolymorphicModel

# from .calculator import FlatFeeCalculator

_ = translation.ugettext_lazy


class GradeClass(enum.Enum):
    CLASS_A = 'A'
    CLASS_B = 'B'
    CLASS_C = 'C'
    CLASS_D = 'D'
    CLASS_E = 'E'


class RuleClass(enum.Enum):
    RULE_A = 'A'
    RULE_B = 'B'
    RULE_C = 'C'
    RULE_D = 'D'
    RULE_E = 'E'


class FeeClass(enum.Enum):
    FLAT = 'FLAT'
    LEVEL = 'LEVEL'


class Grade(models.Model):
    class Meta:
        ordering = ['slug']
        verbose_name = _('Grade')
        verbose_name_plural = _('Grade')

    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        verbose_name='uuid')
    slug = models.SlugField(
        unique=True,
        max_length=80,
        choices=[(str(x.value), str(x.name.replace('_', ' '))) for x in GradeClass],
        default=GradeClass.CLASS_A.value,
        verbose_name=_("Slug"))
    name = models.CharField(
        max_length=80, unique=True,
        verbose_name=_('Name'))
    description = models.CharField(
        max_length=500, blank=True)

    def __str__(self):
        return self.name


class Rate(models.Model):
    class Meta:
        verbose_name = _('Rate')
        verbose_name_plural = _('Rate')
        ordering = ['slug']

    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        verbose_name='uuid')
    slug = models.SlugField(
        unique=True,
        max_length=80,
        choices=[(str(x.value), str(x.name.replace('_', ' '))) for x in GradeClass],
        default=GradeClass.CLASS_A.value,
        verbose_name=_("Slug"))
    name = models.CharField(
        max_length=80, unique=True,
        verbose_name=_('Name'))
    description = models.CharField(
        max_length=500, blank=True)

    def __str__(self):
        return self.name


class Rule(models.Model):
    class Meta:
        verbose_name = _('Rule')
        verbose_name_plural = _('Rule')
        ordering = ['slug']

    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        verbose_name='uuid')
    slug = models.SlugField(
        unique=True,
        max_length=80,
        choices=[(str(x.value), str(x.name.replace('_', ' '))) for x in RuleClass],
        default=RuleClass.RULE_A.value,
        verbose_name=_("Slug"))
    name = models.CharField(
        max_length=80, unique=True,
        verbose_name=_('Name'))
    description = models.CharField(
        max_length=500, blank=True)
    weighting = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    def __str__(self):
        return self.name


class GradeRate(models.Model):
    class Meta:
        verbose_name = _('Grade Rate')
        verbose_name_plural = _('Grade Rates')
        unique_together = ('grade', 'rate')
        ordering = ['rate__slug']

    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        verbose_name='uuid')
    grade = models.ForeignKey(
        Grade, on_delete=models.CASCADE,
        verbose_name=_("Grade"))
    rate = models.ForeignKey(
        Rate, on_delete=models.CASCADE,
        verbose_name=_("Rate"))
    fee_rate = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    def __str__(self):
        return "%s %s" % (self.grade.name, self.rate.name)


class GradeRule(models.Model):
    class Meta:
        verbose_name = _('Grade Rule')
        verbose_name_plural = _('Grade Rules')
        unique_together = ('grade', 'rule')
        ordering = ['rule__slug']

    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        verbose_name='uuid')
    grade = models.ForeignKey(
        Grade, on_delete=models.CASCADE,
        verbose_name=_("Grade"))
    rule = models.ForeignKey(
        Rule, on_delete=models.CASCADE,
        verbose_name=_("Rule"))
    min_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5000000000)
        ]
    )
    max_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5000000000)
        ]
    )

    def __str__(self):
        return "%s %s" % (self.grade.name, self.rule.name)


class ReferralManager(TreeManager):
    pass


class Referral(NumeratorMixin, MPTTModel, models.Model):
    class Meta:
        verbose_name = _('Referral')
        verbose_name_plural = _('Referral')
        unique_together = ('parent', 'account')

    limit = 3

    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        verbose_name='uuid')
    fee_class = models.SlugField(
        max_length=80,
        choices=[(str(x.value), str(x.name.replace('_', ' '))) for x in FeeClass],
        default=FeeClass.FLAT.value,
        verbose_name=_("fee class"))
    parent = TreeForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='downlines',
        verbose_name=_('Up Line'))
    account = models.OneToOneField(
        get_user_model(), editable=False,
        on_delete=models.CASCADE,
        verbose_name=_('account'))
    balance = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_("Balance"))
    created_at = models.DateTimeField(
        default=timezone.now, editable=False)

    def __str__(self):
        return str(self.account)

    def get_referral_limit(self):
        return getattr(settings, 'REFERRAL_DOWNLINE_LIMIT', None) or self.limit

    def get_uplines(self):
        return self.get_ancestors(include_self=False, ascending=True)[:self.get_referral_limit()]


    # def get_downlines(self, level=0):
    #     return self.get_descendants(include_self=False).filter(
    #         level=getattr(self, 'level') + 1 + level
    #     ).annotate(
    #         total_donations=self.downline_donations_subquery()
    #     )
    #
    # def downline_donations_subquery(self, extra_filter=None):
    #     donation_model = apps.get_model('dutaziswaf_donations', 'donation')
    #     filter = {
    #         'referral_id': models.OuterRef('pk'),
    #         'is_paid': True
    #     }
    #     if extra_filter:
    #         filter.update(extra_filter)
    #     sqs = Coalesce(
    #         models.Subquery(
    #             donation_model.objects.filter(**filter).order_by().values('referral_id').annotate(
    #                 total=models.Sum('total_amount')
    #             ).values('total'),
    #             output_field=models.DecimalField()
    #         ), decimal.Decimal(0.00))
    #     return sqs
    #
    # def get_fundraised_by_campaigns(self):
    #     campaigns = self.campaigns.all().filter(is_paid=True)
    #     return (
    #         decimal.Decimal(0.00) if not campaigns.count()
    #         else campaigns.aggregate(total=models.Sum('total_amount'))['total']
    #     )
    #
    # def get_fundraised_by_downlines(self, level=0):
    #     downlines = self.get_downlines(level=level)
    #     aggregated = downlines.aggregate(total_fundraised=models.Sum('total_donations'))
    #     return aggregated['total_fundraised'] or decimal.Decimal(0.00)
    #
    # @property
    # def calculator(self):
    #     """ Get Fee calculator """
    #     fee_class = {
    #         FeeClass.FLAT.value: FlatFeeCalculator,
    #     }
    #     return fee_class[str(self.fee_class)](self)
    #
    # @property
    # def fee_campaign(self):
    #     return self.calculator.get_campaign_fee()
    #
    # @property
    # def fee_downline_0(self):
    #     return self.calculator.get_downline_fee(level=0)
    #
    # @property
    # def fee_downline_1(self):
    #     return self.calculator.get_downline_fee(level=1)
    #
    # @property
    # def fee_downline_2(self):
    #     return self.calculator.get_downline_fee(level=2)
    #
    # @cached_property
    # def total_fee(self):
    #     total = (
    #         self.fee_campaign
    #         + self.fee_downline_0
    #         + self.fee_downline_1
    #         + self.fee_downline_2
    #     )
    #     return total
    #
    # @cached_property
    # def total_fundraised(self):
    #     return self.get_fundraised_by_campaigns() + self.get_fundraised_by_downlines(level=0)
    #
    # @cached_property
    # def total_donation(self):
    #     donations = self.donations.all().filter(is_paid=True)
    #     return donations.aggregate(total=models.Sum('total_amount'))['total'] or decimal.Decimal(0.00)


class ReferralTransaction(NumeratorMixin, PolymorphicModel):
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        verbose_name='uuid')
    flow = models.CharField(
        max_length=3,
        choices=(('IN', 'In'), ('OUT', 'Out')),
        default='IN', verbose_name=_('Flow'))
    referral = models.ForeignKey(
        Referral, on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name=_("Referral"))
    amount = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        editable=False,
        verbose_name=_("Amount"))
    old_balance = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        editable=False,
        verbose_name=_("Old Balance"))
    balance = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        editable=False,
        verbose_name=_("Balance"))
    note = models.CharField(
        max_length=250,
        null=True, blank=True,
        verbose_name=_('Note'))
    created_at = models.DateTimeField(
        default=timezone.now, editable=False)

    def __str__(self):
        return self.inner_id

    @property
    def reference(self):
        return self.get_real_instance().get_reference()

    def get_reference(self):
        raise NotImplementedError

    def get_amount(self):
        raise NotImplementedError

    def increase_balance(self):
        self.balance = self.referral.balance + self.amount
        return self.balance

    def decrease_balance(self):
        self.balance = self.referral.balance - self.amount
        return self.balance

    def calculate_balance(self):
        return {'IN': self.increase_balance, 'OUT': self.decrease_balance}[self.flow]()

    def save(self, *args, **kwargs):
        self.old_balance = self.referral.balance
        self.amount = self.get_amount()
        self.calculate_balance()
        super().save(*args, **kwargs)
