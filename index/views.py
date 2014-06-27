from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404


def user_list(request):
    users = get_user_model().objects.all()
    output = ', '.join([u.get_full_name() for u in users])
    return HttpResponse(output)


def user_detail(request, user_id):
    """
    Render full profile of User, throw 404 if ID not found.
    """
    user = get_object_or_404(get_user_model(), pk=user_id)
    return render(request, 'profile.html', {'user': user})
