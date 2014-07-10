from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from index.views import MessageFormView, MessageSentView, LoginView, LogoutView, UserDetailView, UserListView, UserUpdateView
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

    url(r'^profile/edit$',
        login_required(UserUpdateView.as_view()),
        name='user_update'),

    # Messages
    url(r'^message$',
        login_required(MessageFormView.as_view()),
        name='message_form'),

    url(r'^message/(?P<user>\d+)$',
        login_required(MessageFormView.as_view()),
        name='message_form'),

    url(r'^message/sent$',
        login_required(MessageSentView.as_view()),
        name='message_sent'),

    # Avatar
    url(r'^avatar/add$', 'avatar.views.add', name='avatar_add'),
    url(r'^avatar/change$', 'avatar.views.change', name='avatar_change'),
    url(r'^avatar/delete$', 'avatar.views.delete', name='avatar_delete'),

    # Auth
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),

    url(r'^recover/(?P<signature>.+)$',
        RecoverDone.as_view(template_name='auth/reset_sent.html'),
        name='password_reset_sent'),

    url(r'^recover$',
        Recover.as_view(template_name='auth/recovery_form.html' ,
                        email_template_name='auth/recovery_email.txt',
                        email_subject_template_name='auth/recovery_email_subject.txt'),
        name='password_reset_recover'),

    url(r'^reset/done$',
        ResetDone.as_view(template_name='auth/recovery_done.html'),
        name='password_reset_done'),

    url(r'^reset/(?P<token>[\w:-]+)$',
        Reset.as_view(template_name='auth/reset.html'),
        name='password_reset_reset'),

    url(r'^reset/(?P<token>[\w:-]+)/new$',
        Reset.as_view(template_name='auth/new.html'),
        name='password_reset_new'),

    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # Error previews
    url(r'^403', 'index.views.error403', name='error_403'),
    url(r'^404', 'index.views.error404', name='error_404'),
    url(r'^500', 'index.views.error500', name='error_500'),
)

# Allow Django to serve media files in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Explicit setup for debug_toolbar: http://django-debug-toolbar.readthedocs.org/en/latest/installation.html#explicit-setup
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )

# Error handlers
handler403 = 'index.views.error403'
handler404 = 'index.views.error404'
handler500 = 'index.views.error500'
