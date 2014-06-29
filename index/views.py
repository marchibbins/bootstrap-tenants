from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView, FormView, ListView, View
from index.models import CustomUser, Industry, Location
import urlparse


class LoginView(FormView):

    """ Class-based login view. """

    form_class = AuthenticationForm
    template_name = 'registration/login.html'

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        """
        Protects all options.
        """
        return super(LoginView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Sets test cookie on GET, redirects if user is already authenticated.
        """
        if request.user.is_authenticated():
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

        self.request.session.set_test_cookie()
        return super(LoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Checks and deletes test cookie, logs in user.
        """
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        # CSRF protection will have thrown a 403 on dispatch if cookie failed

        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        """
        Resets test cookie after invalid credentials, render form with errors.
        """
        self.request.session.set_test_cookie()
        return super(LoginView, self).form_invalid(form)

    def get_success_url(self):
        """
        Returns redirect URL after valid form submission.
        """
        redirect_to = self.request.REQUEST.get('next')

        netloc = urlparse.urlparse(redirect_to)[1]
        if netloc and netloc != self.request.get_host():
            # Prevent redirect to different host
            redirect_to = settings.LOGIN_REDIRECT_URL

        return redirect_to

    def get_context_data(self, **kwargs):
        """
        Handles redirect URL from request.
        """
        context = super(LoginView, self).get_context_data(**kwargs)
        context['next'] = self.request.REQUEST.get('next', settings.LOGIN_REDIRECT_URL)
        return context


class LogoutView(View):

    """ Class-based logout view. """

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)


class UserListView(ListView):

    """
    Render detail view for a User.
    """

    orderable_columns = ('first_name', 'last_name', 'company', 'location', 'date_moved_in')
    orderable_default = 'last_name'

    template_name = 'user_list.html'

    def get_queryset(self):
        """
        Returns ordered queryset based on GET params.
        Stores filter combination on instance for template context.
        """
        queryset = CustomUser.objects.filter(is_staff=False)
        self.filters = {
            'querystring': '?'
        }

        # Filters
        industry = self.request.GET.get('industry')
        if industry:
            queryset = queryset.filter(industries__id=industry)
            self.filters['querystring'] += '&industry=%s' % industry
            self.filters['selected_industry'] = int(industry)

        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(location=location)
            self.filters['querystring'] += '&location=%s' % location
            self.filters['selected_location'] = int(location)

        # Ordering
        order_by = self.request.GET.get('order_by')
        if order_by not in self.orderable_columns:
            order_by = self.orderable_default
        self.filters['order_by'] = order_by

        order = self.request.GET.get('order', 'asc')
        if order == 'desc':
            order_by = '-' + order_by
        self.filters['order'] = order

        return queryset.order_by(order_by)

    def get_context_data(self, **kwargs):
        """
        Adds Industry and Location objects for filter options.
        """
        context = super(UserListView, self).get_context_data(**kwargs)
        context.update(self.filters)
        context['industries'] = Industry.objects.all()
        context['locations'] = Location.objects.all()
        return context


class UserDetailView(DetailView):

    """
    Render detail view for a User.
    """

    model = CustomUser
    template_name = 'user_detail.html'
