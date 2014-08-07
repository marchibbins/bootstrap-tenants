from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect
from django.utils.timezone import now
from index.models import CustomUser


class DomainRedirectMiddleware(object):

    """ Handles domain forwarding for multiple sites. """

    def process_request(self, request):
        """
        Forward any request is made for a site other than the current.
        """
        site = Site.objects.get_current()
        if request.get_host() == site.domain:
            return None

        url = '%s://%s' % (request.is_secure() and 'https' or 'http', site.domain)
        return HttpResponsePermanentRedirect(url)


class SetLastVisitMiddleware(object):

    """ Set last visit date on each authenticated user request with building IP. """

    def get_client_ip(self, request):
        """
        Get client IP address.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def process_response(self, request, response):
        """
        Sets new date if User is within locations and not visiting the admin.
        """
        if hasattr(request, 'user') and request.path.startswith(reverse('admin:index')) == False:
            # Last use of website.
            if request.user.is_authenticated():
                user = CustomUser.objects.get(pk=request.user.pk)
                user.last_visit = now()
                # Last use of website within the building.
                if self.get_client_ip(request) in settings.LOCATION_IPS:
                    user.last_on_site = now()
                user.save()
        return response
