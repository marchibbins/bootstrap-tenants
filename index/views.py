from django.contrib.auth.models import User
from django.shortcuts import render

from index.models import Tenant

def list(request):
    """ Renders sortable list of Users. """

    user_fields = ['first_name', 'last_name', 'email']
    sort = request.GET.get('sort', 'last_name')
    reverse = (sort[0:1] == '-')

    if sort.split('-').pop() in user_fields:
        sort = 'user__'+sort.split('-').pop()
        if reverse == True:
            sort = '-'+sort

    tenants = Tenant.objects.order_by(sort)
    return render(request, 'index.html', {'tenants': tenants})

def profile(request, tenant_id):
    """ Render full profile of tenant. """

    tenant = Tenant.objects.get(user__id=tenant_id)
    return render(request, 'profile.html', {'tenant': tenant})
