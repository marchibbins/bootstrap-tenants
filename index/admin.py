from django import forms
from django.contrib import admin
from index.models import Tenant, Location, Industry
import logging


class IndustryAdmin(admin.ModelAdmin):
    verbose_name_plural = 'industries'


class TenantForm(forms.ModelForm):
    # first_name = forms.CharField()
    # last_name = forms.CharField()
    # email_address = forms.EmailField()

    class Meta:
        model = Tenant
        fields = ['bio', 'company', 'moved_in_date', 'industries', 'location']


class TenantAdmin(admin.ModelAdmin):
    form = TenantForm
    logging.debug('Debug Message')

admin.site.register(Tenant, TenantAdmin)
admin.site.register(Location)
admin.site.register(Industry, IndustryAdmin)
