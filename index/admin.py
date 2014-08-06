from django.contrib import admin
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.views import login
from index.models import CustomUser, Industry, Location
from index.forms import CustomAdminAuthenticationForm, CustomUserChangeForm, CustomUserCreationForm


class CustomUserAdmin(UserAdmin):

    """ Extends the built-in Django UserAdmin, overriding definitions
    referring to username, inheriting all others. """

    fieldsets = (
        (None, {
            'fields': ('email', 'first_name', 'last_name', 'password')
        }),
        ('Information', {
            'fields': ('bio', 'website', 'company', 'industries', 'location', 'date_moved_in', 'birthday', 'in_tenant_index', 'in_staff_index')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')
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
            'fields': ('bio', 'company', 'industries', 'location', 'date_moved_in', 'birthday', 'in_tenant_index', 'in_staff_index')
        }),
    )

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    add_form_template = 'user/admin/add_form.html'

    list_display = ('email', 'first_name', 'last_name', 'company', 'get_industries', 'location', 'date_moved_in', 'in_tenant_index', 'in_staff_index', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('industries', 'location', 'in_tenant_index', 'in_staff_index', 'is_staff', 'is_active', 'is_superuser', 'groups')
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


def admin_permission(request):
    """
    Overrides built-in method to allow non-staff superuser access.
    """
    return request.user.is_active and (request.user.is_staff or request.user.is_superuser)


def admin_login(request, extra_context=None):
    """
    Displays the login form for the given HttpRequest, overrides authentication form.
    """
    context = {
        'title': 'Log in',
        'app_path': request.get_full_path(),
        REDIRECT_FIELD_NAME: request.get_full_path(),
    }
    context.update(extra_context or {})

    defaults = {
        'extra_context': context,
        'current_app': 'admin',
        'authentication_form': CustomAdminAuthenticationForm,
        'template_name': 'admin/login.html',
    }
    return login(request, **defaults)


admin.site.has_permission = admin_permission
admin.site.login = admin_login
