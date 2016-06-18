# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf.urls import include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from iupdsmanager.views import index, profile, create_user, logout,\
    create_contact, contact_details, my_contacts, create_graphs,\
    drop_graphs, create_graph_user, new_user

from pdsoauth.views import application_list, revoke_application, oauth_login, oauth_tyk_notify, oauth_create_client

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'^admin/', admin.site.urls),
    url(r'^iupdsmanager/', include('iupdsmanager.urls')),
    url(r'^api/v1/profile/$', profile, name='profile'),
    url(r'^api/v1/contact/$', create_contact, name='create_contact'),
    url(r'^api/v1/contact/details$', contact_details, name='contact_details'),
    url(r'^api/v1/mycontacts/$', my_contacts, name='my_contacts'),
    url(r'^api/v1/create_user/$', create_user, name='create_user'),
    url(r'^api/v1/user/new/$', csrf_exempt(new_user), name='new_user'),
    url(r'^api/v1/graph/user/$', create_graph_user, name='create_graph_user'),
    url(r'^api/v1/drop_graphs/$', drop_graphs, name='drop_graphs'),
    url(r'^api/v1/create_graphs/$', create_graphs, name='create_graphs'),
    url(r'^api/v1/auth/logout/$', logout, name='logout'),
    url(r'^o/', include('iupdsmanager.urls', namespace='oauth2_provider')),
    url(r'^oauth/login/$', oauth_login, name='oauth_login'),
    url(r'^oauth/tyk/notify/$', csrf_exempt(oauth_tyk_notify), name='oauth_tyk_notify'),
    url(r'^oauth/clients/create/$', csrf_exempt(oauth_create_client), name='oauth_create_client_notify'),
    url(r'^api/v1/users/applications/$', application_list, name='user-applications'),
    url(r'^api/v1/users/applications/(?P<pk>[0-9])/$', revoke_application, name='revoke-applications')
]
