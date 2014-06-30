from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from index.views import LoginView, LogoutView, UserDetailView, UserListView


admin.autodiscover()

urlpatterns = patterns('',
    # Index
    url(r'^$', login_required(UserListView.as_view()), name='user_list'),
    url(r'^profile/(?P<pk>\d+)$', login_required(UserDetailView.as_view()), name='user_detail'),

    # Auth
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
    url(r'^password/', include('password_reset.urls')),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
)
