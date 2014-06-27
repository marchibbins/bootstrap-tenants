from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Index
    url(r'^$', 'index.views.user_list', name='user_list'),
    url(r'^profile/(?P<user_id>[0-9]+)$', 'index.views.user_detail', name='user_detail'),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
)
