from django.conf.urls import patterns, include, url
from django.contrib import admin
from index.views import UserDetailView


admin.autodiscover()

urlpatterns = patterns('',
    # Index
    url(r'^$', 'index.views.user_list', name='user_list'),
    url(r'^profile/(?P<pk>\d+)$', UserDetailView.as_view(), name='user-detail'),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
)
