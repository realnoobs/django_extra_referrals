from django.contrib import admin
from .models import Donation, Withdraw

admin.site.register(Donation, admin.ModelAdmin)
admin.site.register(Withdraw, admin.ModelAdmin)
