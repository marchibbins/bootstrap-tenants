from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Index
    url(r'^$', 'index.views.list', name='index'),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
)
