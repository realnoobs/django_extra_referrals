import uuid
import enum
from django.db import models
from django.utils import timezone, translation
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django_numerators.models import NumeratorMixin
from mptt.models import MPTTModel, TreeForeignKey, TreeManager

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
        editable=False,
        verbose_name=_("Balance"))
    created_at = models.DateTimeField(
        default=timezone.now, editable=False)

    def __str__(self):
        return (
            self.account.username
            if self.account.get_full_name() in ['', None]
            else self.account.get_full_name()
        )

    def get_referral_limit(self):
        return getattr(settings, 'REFERRAL_DOWNLINE_LIMIT', None) or self.limit

    def get_uplines(self):
        return self.get_ancestors(include_self=False, ascending=True)[:self.get_referral_limit()]


class Transaction(NumeratorMixin):
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
        verbose_name=_("Amount"))
    rate = models.DecimalField(
        default=0.00,
        max_digits=4,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        verbose_name=_('Fee Rate'))
    fee = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_("Fee"))
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
    is_verified = models.BooleanField(
        default=False)
    verified_at = models.DateTimeField(
        null=True, blank=True,
        editable=False,
        verbose_name=_("Verified at"))

    content_type = models.ForeignKey(
        ContentType,
        models.SET_NULL,
        blank=True, null=True,
        verbose_name=_('reference type'))
    object_id = models.CharField(
        _('reference id'),
        max_length=100,
        blank=True, null=True)
    content_object = GenericForeignKey()

    def __str__(self):
        return self.inner_id
