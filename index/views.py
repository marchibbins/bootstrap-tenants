from django.contrib.auth.models import User
from django.shortcuts import render
from django.db.models import Q

from index.models import Tenant, Industry, Location

def list(request):
    """ Renders sortable list of Users. """

    user_fields = ['first_name', 'last_name', 'email']
    sort = request.GET.get('sort', 'last_name')
    reverse = (sort[0:1] == '-')
    if sort.split('-').pop() in user_fields:
        sort = 'user__'+sort.split('-').pop()
        if reverse == True:
            sort = '-'+sort

    industries = Industry.objects.all()
    locations = Location.objects.all()

    industry_id = request.GET.get('industry', '-1')
    location_id = request.GET.get('location', '-1')
    search_term = request.GET.get('search', '')

    tenants = Tenant.objects.all()
    if industry_id != '-1':
        tenants = tenants.filter(industries__id__contains=industry_id)
    if location_id != '-1':
        tenants = tenants.filter(location_id=location_id)
    if search_term != '':
        tenants = tenants.filter(
                        Q(user__first_name__icontains=search_term)|
                        Q(user__last_name__icontains=search_term)|
                        Q(company__icontains=search_term)
                )

    tenants = tenants.order_by(sort)

    # import pdb; pdb.set_trace()

    return render(request, 'index.html', {
        'tenants': tenants,
        'industries': industries,
        'locations': locations,
    })

def profile(request, tenant_id):
    """ Render full profile of tenant. """

    tenant = Tenant.objects.get(user__id=tenant_id)
    return render(request, 'profile.html', {'tenant': tenant})
