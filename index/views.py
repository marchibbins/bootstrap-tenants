from django.contrib.auth import get_user_model
from django.views.generic import DetailView, ListView


class UserListView(ListView):

    """
    Render detail view for a User.
    """

    model = get_user_model()
    template_name = 'list.html'


class UserDetailView(DetailView):

    """
    Render detail view for a User.
    """

    model = get_user_model()
    template_name = 'profile.html'
