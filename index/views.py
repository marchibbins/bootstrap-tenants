from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.views.generic.detail import DetailView


def user_list(request):
    users = get_user_model().objects.all()
    output = ', '.join([u.get_full_name() for u in users])
    return HttpResponse(output)


class UserDetailView(DetailView):
    """
    Render detail view for a User.
    """
    model = get_user_model()
    template_name = 'profile.html'
