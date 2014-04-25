from django.contrib.auth.models import User
from django.shortcuts import render

def index(request):
    users = User.objects.all()
    return render(request, 'index.html', {'users': users})