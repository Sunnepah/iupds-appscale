from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /iupdsmanager/
    url(r'^$', views.index, name='index'),
    url(r'^profiles/$', views.profile, name='profile'),
]