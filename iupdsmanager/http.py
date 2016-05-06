from django.http import HttpResponseRedirect

from iupds import settings


class HttpResponseUriRedirect(HttpResponseRedirect):
    def __init__(self, redirect_to, *args, **kwargs):
        self.allowed_schemes = settings.ALLOWED_REDIRECT_URI_SCHEMES
        super(HttpResponseUriRedirect, self).__init__(redirect_to, *args, **kwargs)
