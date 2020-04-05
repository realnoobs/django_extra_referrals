from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.apps import apps

from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
from mptt.admin import MPTTModelAdmin

from .models import (
    Grade,
    Rate,
    Rule,
    GradeRule,
    GradeRate,
    Referral,
    ReferralTransaction
)


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'description'
    ]


@admin.register(Rule)
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


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    inlines = [GradeRuleInline, GradeRateInline]
    list_display = [
        'name',
        'slug',
        'description'
    ]


@admin.register(Referral)
class ReferralAdmin(MPTTModelAdmin):
    search_fields = ['account__first_name', 'account__last_name']
    list_select_related = ['account', 'parent']
    list_display = ['inner_id', 'account', 'parent', 'decendants', 'downlines', 'level', 'created_at', 'balance']

    # def has_delete_permission(self, request, obj=None):
    #     return False
    #
    # def has_change_permission(self, request, obj=None):
    #     return False
    #
    # def has_add_permission(self, request):
    #     return False

    def decendants(self, obj):
        return obj.get_descendant_count()

    def downlines(self, obj):
        return obj.downlines.count()

    def get_queryset(self, request):
        return super().get_queryset(request).only('inner_id', 'account', 'parent')


@admin.register(ReferralTransaction)
class ReferralTransactionAdmin(PolymorphicParentModelAdmin):
    """ Parent admin Referal Transaction Model, set child model in settings """
    list_filter = ['created_at', 'flow']
    list_display = ['inner_id', 'referral', 'flow', 'note', 'amount', 'balance', 'created_at']

    def get_child_models(self):
        child_models_list = getattr(settings, 'REFERRAL_TRANSACTION_CHILD_MODELS', None)
        if not child_models_list:
            raise NotImplementedError(
                "Implement REFERRAL_TRANSACTION_CHILD_MODELS in settings"
            )
        try:
            models = [apps.get_model(child_models, require_ready=True) for child_models in child_models_list]
            return models
        except ValueError:
            raise ImproperlyConfigured(
                "REFERRAL_TRANSACTION_CHILD_MODELS item must "
                "be of the form 'app_label.model_name'"
            )
        except LookupError:
            raise ImproperlyConfigured(
                "Make sure all of REFERRAL_TRANSACTION_CHILD_MODELS is installed"
            )


class ReferralTransactionChildAdmin(PolymorphicChildModelAdmin):
    base_model = ReferralTransaction
