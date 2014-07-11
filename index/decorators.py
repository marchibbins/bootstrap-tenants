from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import login
from functools import wraps
from index.forms import CustomAdminAuthenticationForm


def admin_member_required(view_func):
    """
    Overrides built-in decorator to allow non-staff superuser access.
    """
    @wraps(view_func)
    def _checklogin(request, *args, **kwargs):
        if request.user.is_active and (request.user.is_staff or request.user.is_superuser):
            # The user is valid. Continue to the admin page.
            return view_func(request, *args, **kwargs)

        assert hasattr(request, 'session'), "The Django admin requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."
        defaults = {
            'template_name': 'admin/login.html',
            'authentication_form': CustomAdminAuthenticationForm,
            'extra_context': {
                'title': 'Log in',
                'app_path': request.get_full_path(),
                REDIRECT_FIELD_NAME: request.get_full_path(),
            },
        }
        return login(request, **defaults)
    return _checklogin

staff_member_required = admin_member_required
