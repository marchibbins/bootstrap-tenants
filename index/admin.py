from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from index.models import CustomUser, Industry, Location
from index.forms import CustomUserChangeForm, CustomUserCreationForm


class CustomUserAdmin(UserAdmin):

    """ Extends the built-in Django UserAdmin, overriding definitions
    referring to username, inheriting all others. """

    fieldsets = (
        (None, {
            'fields': ('email', 'first_name', 'last_name', 'password')
        }),
        (_('Information'), {
            'fields': ('industries', 'location')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')}
         ),
    )

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('last_name',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Industry)
admin.site.register(Location)
