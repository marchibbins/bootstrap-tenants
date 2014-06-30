from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from index.views import LoginView, LogoutView, UserDetailView, UserListView
from password_reset.views import Recover, RecoverDone, Reset, ResetDone


admin.autodiscover()

urlpatterns = patterns('',
    # Index
    url(r'^$',
        login_required(UserListView.as_view()),
        name='user_list'),

    url(r'^profile/(?P<pk>\d+)$',
        login_required(UserDetailView.as_view()),
        name='user_detail'),

    # Auth
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),

    url(r'^recover/(?P<signature>.+)/$',
        RecoverDone.as_view(template_name='auth/reset_sent.html'),
        name='password_reset_sent'),

    url(r'^recover/$',
        Recover.as_view(template_name='auth/recovery_form.html' ,
                        email_template_name='auth/recovery_email.txt',
                        email_subject_template_name='auth/recovery_email_subject.txt'),
        name='password_reset_recover'),

    url(r'^reset/done/$',
        ResetDone.as_view(template_name='auth/recovery_done.html'),
        name='password_reset_done'),

    url(r'^reset/(?P<token>[\w:-]+)/$',
        Reset.as_view(template_name='auth/reset.html'),
        name='password_reset_reset'),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
)
