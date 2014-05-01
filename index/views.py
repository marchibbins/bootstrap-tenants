from django.contrib.auth.models import User
from django.shortcuts import render


def list(request):
    """ Renders sortable list of Users. """

    sort = request.GET.get('sort', 'last_name')
    if sort.split('-').pop() not in ['first_name', 'last_name', 'email']:
        sort = 'last_name'

    users = User.objects.order_by(sort)
    return render(request, 'index.html', {'users': users})
