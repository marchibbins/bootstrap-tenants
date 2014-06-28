from django.contrib.auth import get_user_model
from django.views.generic import DetailView, ListView


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
        """
        order_by = self.request.GET.get('order_by')
        if order_by not in self.orderable_columns:
            order_by = self.orderable_default

        order = self.request.GET.get('order', 'asc')
        if order == 'desc':
            order_by = '-' + order_by

        return get_user_model().objects.order_by(order_by)


class UserDetailView(DetailView):

    """
    Render detail view for a User.
    """

    model = get_user_model()
    template_name = 'user_detail.html'
