from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django_referrals.admin import ReferralInline


@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    ordering = ('username',)
    search_fields = ('username', 'person__fullname', 'email')
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_referral', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_referral', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_referral',
                'is_staff',
                'groups',
                'user_permissions'
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    inlines = [ReferralInline]
