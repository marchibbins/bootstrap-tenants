from django.contrib.sites.models import Site


def site(request):
    current = Site.objects.get_current()
    return {
        'SITE_DOMAIN': current.domain,
        'SITE_NAME': current.name
    }
