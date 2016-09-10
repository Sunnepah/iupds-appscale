from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from iupdsmanager.views import index, profile, create_contact, get_contact_details, create_graphs, \
    drop_graphs, create_graph_user, new_user

urlpatterns = [
    # ex: /iupdsmanager/
    url(r'^$', index, name='index'),
    url(r'^api/v1/user/profile/$', profile, name='profile'),
    url(r'^api/v1/user/contact/$', create_contact, name='create_contact'),
    url(r'^api/v1/user/contact/details$', get_contact_details, name='contact_details'),
    url(r'^api/v1/user/new/$', csrf_exempt(new_user), name='new_user'),
    url(r'^api/v1/user/graph/$', create_graph_user, name='create_graph_user'),
    url(r'^api/v1/user/graph/create/$', create_graphs, name='create_graphs'),
    url(r'^api/v1/user/graph/drop/$', drop_graphs, name='drop_graphs')
]
