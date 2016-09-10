from django.conf.urls import url

from django.views.decorators.csrf import csrf_exempt

from pdsoauth.views import logout, application_list, revoke_application, oauth_login, oauth_tyk_notify, \
    oauth_create_client

urlpatterns = [
    # ex: /pdsoauth/
    url(r'^oauth/login/$', oauth_login, name='oauth_login'),
    url(r'^oauth/tyk/notify/$', csrf_exempt(oauth_tyk_notify), name='oauth_tyk_notify'),
    url(r'^oauth/clients/create/$', csrf_exempt(oauth_create_client), name='oauth_create_client_notify'),
    url(r'^auth/logout/$', logout, name='logout'),

    url(r'^api/v1/user/applications/$', application_list, name='user-applications'),
    url(r'^api/v1/user/applications/(?P<pk>[0-9])/$', revoke_application, name='revoke-applications')
]
