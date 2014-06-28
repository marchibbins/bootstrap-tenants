from django.conf.urls import patterns, include, url
from django.contrib import admin
from index.views import UserDetailView, UserListView


admin.autodiscover()

urlpatterns = patterns('',
    # Index
    url(r'^$', UserListView.as_view(), name='user_list'),
    url(r'^profile/(?P<pk>\d+)$', UserDetailView.as_view(), name='user_detail'),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
)
