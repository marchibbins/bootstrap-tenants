from django.views.generic import DetailView, ListView
from index.models import CustomUser, Industry, Location


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
        queryset = CustomUser.objects.all()
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
