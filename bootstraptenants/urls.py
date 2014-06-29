from django.conf.urls import patterns, include, url
from django.contrib import admin
from index.views import LoginView, LogoutView, UserDetailView, UserListView


admin.autodiscover()

urlpatterns = patterns('',
    # Index
    url(r'^$', UserListView.as_view(), name='user_list'),
    url(r'^profile/(?P<pk>\d+)$', UserDetailView.as_view(), name='user_detail'),

    # Auth
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
)
