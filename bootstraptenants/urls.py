from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Index
    url(r'^$', 'index.views.list', name='index'),

    # Profile
    # url(r'^profile\/(?P<tenant_id>[0-9]+)/$', 'index.views.profile', name='profile'),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
)
