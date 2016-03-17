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
from tastypie.api import Api
from jobs.api import JobResource

# from polls.views import index as pollIndex
from iupdsmanager.views import index, profile, create_user, logout, create_contact, contact_details, my_contacts
# from iupds.views import IndexView

from rest_framework_nested import routers

from authentication.views import AccountViewSet, LoginView
from posts.views import AccountPostsViewSet, PostViewSet

# account rest_framework API
router = routers.SimpleRouter()
router.register(r'accounts', AccountViewSet)

router.register(r'posts', PostViewSet)
accounts_router = routers.NestedSimpleRouter(
    router, r'accounts', lookup='account'
)
accounts_router.register(r'posts', AccountPostsViewSet)

# JOB tastypie API
v1_api = Api(api_name='v1')
v1_api.register(JobResource())


urlpatterns = [
    url(r'^$', index),
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^iupdsmanager/', include('iupdsmanager.urls')),
    url(r'^api/', include(v1_api.urls)),
    # url(r'^job/', include('jobs.urls')),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/', include(accounts_router.urls)),
    # url('^.*$', IndexView.as_view(), name='index'),
    url(r'^api/v1/auth/login/$', LoginView.as_view(), name='login'),
    # url(r'^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),
    url(r'^api/v1/profile/$', profile, name='profile'),
    url(r'^api/v1/contact/$', create_contact, name='create_contact'),
    url(r'^api/v1/contact/details$', contact_details, name='contact_details'),
    url(r'^api/v1/mycontacts/$', my_contacts, name='mycontacts'),
    url(r'^api/v1/create_user/$', create_user, name='create_user'),
    url(r'^api/v1/auth/logout/$', logout, name='logout')
]
