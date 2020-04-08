from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.apps import apps

from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
from mptt.admin import MPTTModelAdmin

from .models import (
    Rate,
    Rule,
    Grade,
    GradeRule,
    GradeRate,
    Referral,
    Transaction
)


# TODO Next Release
# @admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'description'
    ]


# TODO Next Release
# @admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'description',
        'weighting'
    ]


class GradeRateInline(admin.TabularInline):
    extra = 0
    model = GradeRate


class GradeRuleInline(admin.TabularInline):
    extra = 0
    model = GradeRule


# TODO Next Release
# @admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    inlines = [GradeRuleInline, GradeRateInline]
    list_display = [
        'name',
        'slug',
        'description'
    ]


@admin.register(Referral)
class ReferralAdmin(MPTTModelAdmin):
    list_filter = ['level']
    list_select_related = ['account', 'parent']
    search_fields = ['account__first_name', 'account__last_name']
    list_display = ['inner_id', 'account', 'parent', 'decendants', 'downlines', 'level', 'created_at', 'balance']

    def decendants(self, obj):
        return obj.get_descendant_count()

    def downlines(self, obj):
        return obj.downlines.count()

    def get_queryset(self, request):
        return super().get_queryset(request).only('inner_id', 'account', 'parent')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_filter = ['created_at', 'flow']
    search_fields = ['referral__account__first_name', 'referral__account__username']
    list_display = ['inner_id', 'referral', 'note', 'flow', 'rate', 'total', 'balance', 'created_at']




class ReferralInline(admin.TabularInline):
    model = Referral
    can_delete = False
    extra = 1
    max_num = 1
