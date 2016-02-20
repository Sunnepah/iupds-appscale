from google.appengine.api import users

from django.core import serializers
from django.http import HttpResponse
from .models import Profile
from django.shortcuts import render


def index(request):
    user = users.get_current_user()
    if user:
        greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                    (user.nickname(), users.create_logout_url('/')))
        # users.CreateLoginURL(dest_url=None, _auth_domain=None, federated_identity=None)
        # users.IsCurrentUserAdmin()
        # users.User(email=None, _auth_domain=None, _user_id=None,
        # federated_identity=None, federated_provider=None, _strict_mode=True)
        # users.is_current_user_admin()[source]
        # data = serializers.serialize("json", user)
        # return HttpResponse('Welcome!')#greeting)
        context = {'user': user, 'greeting': greeting}
        return render(request, 'layout.html', context)
    else:
        users.create_login_url('/')


def getprofile(request):
    profile = Profile.objects.all()
    data = serializers.serialize("json", profile)
    # user = users.User("Albert.Johnson@example.com")
    # user = users.get_current_user()
    return HttpResponse(data)
