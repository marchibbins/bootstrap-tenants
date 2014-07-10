from django.utils.timezone import now
from django.conf import settings
from index.models import CustomUser
import logging
from inspector_panel import debug

class SetLastVisitMiddleware(object):

    """
    Set last visit date on each authenticated user request with building ip.
    """

    def get_client_ip(self, request):
        """
        Get client ip address.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip


    def process_response(self, request, response):
        if request.path.startswith('/admin/') == False:
            # If client is in the building(s).
            if (request.user.is_authenticated() 
                and self.get_client_ip(request) in settings.LOCATION_IPS):
                # Update last visit time.
                CustomUser.objects.filter(pk=request.user.pk).update(last_visit=now())
        return response