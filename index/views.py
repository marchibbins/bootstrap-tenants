from django.contrib.auth import get_user_model
from django.http import HttpResponse


def list(request):
    users = get_user_model().objects.all()
    output = ', '.join([u.get_full_name() for u in users])
    return HttpResponse(output)
