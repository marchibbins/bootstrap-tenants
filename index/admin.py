from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from index.models import Tenant, Location, Industry

import logging
	
class TenantInline(admin.StackedInline):
    model = Tenant
    can_delete = False
    verbose_name_plural = 'tenants'

class UserAdmin(UserAdmin):
    inlines = (TenantInline,)
    # fieldset
    # list_display = ('email', 'first_name', 'last_name', 'is_active', 'date_joined', 'is_staff')


class IndustryAdmin(admin.ModelAdmin):
    verbose_name_plural = 'industries'

class TenantForm(forms.ModelForm):

    class Meta:
        model = Tenant
        exclude = ['user']

class TenantAdmin(admin.ModelAdmin):
	form = TenantForm
	logging.debug('Debug Message')

try:
    admin.site.unregister(User)
finally:
    admin.site.register(User, UserAdmin)

admin.site.register(Tenant, TenantAdmin)
admin.site.register(Location)
admin.site.register(Industry, IndustryAdmin)

