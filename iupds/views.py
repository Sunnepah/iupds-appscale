from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator

from google.appengine.api import users


class IndexView(TemplateView):
    template_name = 'layout.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):

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
            # context = {'user': user, 'greeting': greeting}
            # return render(request, 'layout.html', context)
            return super(IndexView, self).dispatch(greeting, *args, **kwargs)
        else:
            users.create_login_url('/')


