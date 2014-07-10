from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView, FormView, ListView, TemplateView
from django.views.generic.edit import UpdateView
from index.forms import MessageForm, CustomUserUpdateForm
from index.models import CustomUser, Industry, Location
import urlparse


class MessageFormView(FormView):

    """ Handles sending messages to Users (or Admins) without exposing email addresses. """

    recipient = None
    form_class = MessageForm
    template_name = 'message/form.html'
    success_url = reverse_lazy('message_sent')

    def get_initial(self):
        """
        Attemps to populate (optional) recipient User object from POST or URL,
        throws 404 if User not found.
        """
        initial = super(MessageFormView, self).get_initial()
        user_id = self.request.POST.get('recipient', self.kwargs.get('user'))
        if user_id:
            self.recipient = get_object_or_404(CustomUser.objects.public(), pk=user_id)
            initial['recipient'] = self.recipient.id
        return initial

    def form_valid(self, form):
        """
        Sends message as email to Admins or recipient if specified.
        """
        recipient_list = [admin[1] for admin in settings.ADMINS]
        user_id = form.cleaned_data.get('recipient')
        if user_id:
            self.recipient = get_object_or_404(CustomUser.objects.public(), pk=user_id)
            recipient_list = [self.recipient.email]

        context = {
            'sender': self.request.user,
            'recipient': self.recipient,
            'subject': form.cleaned_data.get('subject'),
            'message': form.cleaned_data.get('message'),
            'site': Site.objects.get_current(),
        }
        subject = loader.render_to_string('message/new_message_subject.txt', context).strip()
        body = loader.render_to_string('message/new_message.txt', context).strip()
        email = EmailMessage(subject=subject, body=body, from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipient_list, headers={'Reply-To': self.request.user.email})
        email.send()

        return super(MessageFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Adds (optional) recipient object to template data.
        """
        context = super(MessageFormView, self).get_context_data(**kwargs)
        context['recipient'] = self.recipient
        return context


class MessageSentView(TemplateView):

    """ Simple static template message. """

    template_name = 'message/sent.html'


class LoginView(FormView):

    """ Class-based login view. """

    form_class = AuthenticationForm
    template_name = 'auth/login.html'

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


class LogoutView(TemplateView):

    """ Class-based logout view. """

    template_name = 'auth/logout.html'

    def get(self, request, *args, **kwargs):
        """
        Renders logout form on GET to perform state change on POST.
        """
        if not request.user.is_authenticated():
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

        return super(LogoutView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Performs logout.
        """
        if request.user.is_authenticated():
            logout(request)

        return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)


class UserListView(ListView):

    """ Render detail view for a User. """

    orderable_columns = ('first_name', 'last_name', 'company', 'location', 'date_moved_in')
    orderable_default = 'last_name'
    paginate_by = 10
    
    template_name = 'user/list.html'

    def get_queryset(self):
        """
        Returns ordered queryset based on GET params.
        Stores filter combination on instance for template context.
        """
        queryset = CustomUser.objects.public()
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

        search_term = self.request.GET.get('search')
        if search_term:
            queryset = queryset.filter(
                Q(first_name__icontains=search_term) |
                Q(last_name__icontains=search_term) |
                Q(company__icontains=search_term))
            self.filters['search_term'] = search_term

        # Ordering
        order_by = self.request.GET.get('order_by')
        if order_by not in self.orderable_columns:
            order_by = self.orderable_default
        self.filters['order_by'] = order_by

        order = self.request.GET.get('order', 'asc')
        if order == 'desc':
            order_by = '-' + order_by
        self.filters['order'] = order

        return queryset.order_by(order_by, self.orderable_default)

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

    """ Render detail view for a User. """

    template_name = 'user/detail.html'

    def get_queryset(self):
        """
        Only allows Users in index to show profile view.
        """
        return CustomUser.objects.public()


class UserUpdateView(UpdateView):

    """ Render update form view for current User. """

    model = CustomUser
    form_class = CustomUserUpdateForm
    success_url = reverse_lazy('user_update')
    template_name = 'user/update.html'

    def get_object(self, queryset=None):
        """
        Return current authenticated user.
        """
        return self.request.user


def error403(request, reason=''):
    """
    Generic 403 view, also CSRF and cookie failure.
    """
    return render(request, '403.html', {'reason': reason}, status=403)


def error404(request):
    """
    Generic 404 view.
    """
    return render(request, '404.html', status=404)


def error500(request):
    """
    Generic 500 view.
    """
    return render(request, '500.html', status=500)
