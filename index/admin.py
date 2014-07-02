from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from index.models import CustomUser, Industry, Location
from index.forms import CustomUserChangeForm, CustomUserCreationForm


class CustomUserAdmin(UserAdmin):

    """ Extends the built-in Django UserAdmin, overriding definitions
    referring to username, inheriting all others. """

    fieldsets = (
        (None, {
            'fields': ('email', 'first_name', 'last_name', 'password')
        }),
        ('Information', {
            'fields': ('bio', 'website', 'company', 'industries', 'location', 'date_moved_in')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_in_index', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')
        }),
        ('Information', {
            'fields': ('bio', 'company', 'industries', 'location', 'date_moved_in')
        }),
    )

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'company', 'get_industries', 'location', 'date_moved_in', 'is_staff', 'is_in_index', 'is_superuser')
    list_filter = ('industries', 'location', 'is_staff', 'is_superuser', 'is_active', 'is_in_index', 'groups')
    search_fields = ('email', 'first_name', 'last_name', 'location__building')
    ordering = ('last_name', 'email')

    def get_industries(self, obj):
        """
        Joins M2M industries field for reading.
        """
        return ', '.join([industry.name for industry in obj.industries.all()])

    get_industries.short_description = 'Industries'


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Industry)
admin.site.register(Location)
