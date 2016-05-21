# coding=utf-8
import simplejson
import json
import logging
import urllib2

from google.appengine.api import users
from google.appengine.api import urlfetch

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from iupds import settings
from iupdsmanager.views import is_logged_in, get_user_email, get_profile
from iupdsmanager.models import Application, Profile, AccessToken, Grant
# ouath2
from iupdsmanager.authorization_code import AuthorizationCodeGrantPds
from iupdsmanager.views import ServiceUnavailable, get_object, get_user_id

log = logging.getLogger('oauth2_provider')
logging.basicConfig(level=logging.DEBUG)
# log = logging.getLogger(__name__)


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def application_list(request):
    try:
        """
        Get all Connected to the current User.
        """
        if request.method == 'GET':
            if is_logged_in():

                user_profile = Profile.objects.filter(email=get_user_email())
                apps = Grant.objects.filter(user=user_profile).values_list('application__pk', flat=True)
                applications = Application.objects.filter(pk__in=apps).values()

                return Response({'user_applications': applications})
            else:
                users.create_login_url('/')
        else:
            return Response({'status': False, 'message': 'Method not allowed'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)

    except Application.DoesNotExist or Profile.DoesNotExist:
        return Response({'status': False, 'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@renderer_classes((JSONRenderer,))
def revoke_application(request, pk):
    try:
        """
        Get all Connected to the current User.
        """
        if request.method == 'DELETE':
            if is_logged_in():

                # delete /tyk/oauth/refresh/{key}?api_id={api_id}
                headers = {'Content-Type': 'application/x-www-form-urlencoded',
                           'x-tyk-authorization': settings.TYK_AUTHORIZATION_NODE_SECRET, 'cache-control': "no-cache"}

                application = Application.objects.get(pk=pk)
                tokens = AccessToken.objects.filter(application=application, user=get_profile()).values()
                print tokens

                pds_auth = AuthorizationCodeGrantPds()

                # make DELETE
                for token in tokens:
                    print 'tokens'
                    print token['token']
                    pds_auth.revoke_token(token['token'], 'access_token', request)
                    r = urlfetch.fetch(url=settings.TYK_DELETE_ACCESS_TOKEN + "/" +
                                       token['token'] + "?api_id=" + settings.PDS_API_ID,
                                       method=urlfetch.DELETE, headers=headers)

                    if r.status_code == 200:
                        response = simplejson.loads(r.content)
                        print "Delete token from tyk"
                        print response

                        print "Deleting Grants"
                        Grant.objects.filter(application=application, user=get_profile()).delete()

                        return Response()
                    else:
                        response = simplejson.loads(r.content)
                        print "unable to delete token from tyk"
                        print response
            else:
                users.create_login_url('/')
        else:
            return Response({'status': False, 'message': 'Method not allowed'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)

    except Application.DoesNotExist or Profile.DoesNotExist or AccessToken.DoesNotExist:
        return Response({'status': False, 'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


def oauth_login(request):
    try:
        if request.method == 'GET':
            client_id = str(request.GET['client_id'])

            app = Application.objects.get(client_id=client_id)
            redirect_uri = str(app.redirect_uris)

            post_login_redirect_url = settings.APPSCALE_APP_URL + "/oauth/login/?client_id=" + client_id + \
                                      "&redirect_uri=" + redirect_uri + "&state=random_state_string&response_type=code"

            if is_logged_in():
                application = {'name': str(app.name), 'scopes_descriptions': settings.SCOPES,
                               'scope': " ".join(settings.SCOPES), 'redirect_uri': redirect_uri, 'client_id': client_id}

                return render(request, "oauth2_provider/authorize.html", application)
            else:
                return redirect(users.create_login_url(post_login_redirect_url))
        elif request.method == 'POST':
            if 'allow' in request.POST and request.POST.get('allow') == 'Authorize':

                payload = 'response_type=code&client_id='+str(request.POST.get('client_id')).strip()+'&redirect_uri='+str(request.POST.get('redirect_uri')).strip()+'&state='+str(request.POST.get('state')).strip()+'&scope='+str(request.POST.get('scope')).strip()+'&key_rules={"allowance":1000,"rate":1000,"per":60,"expires":'+str(settings.ACCESS_TOKEN_EXPIRE_SECONDS)+',"quota_max":-1,"quota_renews":1406121006,"quota_remaining":0,"quota_renewal_rate":60,"access_rights":{"'+settings.PDS_API_ID+'":{"api_name":"'+settings.PDS_API_NAME+'","api_id":"'+settings.PDS_API_ID+'","versions":["Default"],"allowed_urls":[{"url":"/api/v1/users/'+str(get_user_id()).strip()+'/emails/(.*)","methods":["GET"]},{"url":"/api/v1/users/'+str(get_user_id()).strip()+'/telephones/(.*)","methods":["GET"]},{"url":"/api/v1/users/'+str(get_user_id()).strip()+'/addresses/(.*)","methods":["GET"]},{"url":"/api/v1/users/'+str(get_user_id()).strip()+'/persons/(.*)","methods":["GET"]}]}},"org_id":"'+settings.TYK_API_ORG_ID+'","oauth_client_id":"'+str(request.POST.get('client_id')).strip()+'","hmac_enabled":false,"hmac_string":"","apply_policy_id":"'+settings.TYK_API_POLICY_ID+'"}'

                headers = {'Content-Type': 'application/x-www-form-urlencoded',
                           'x-tyk-authorization': settings.TYK_AUTHORIZATION_NODE_SECRET, 'cache-control': "no-cache"}

                # make POST
                r = urlfetch.fetch(url=settings.TYK_OAUTH_AUTHORIZE_ENDPOINT, payload=payload, method=urlfetch.POST,
                                   headers=headers)

                if r.status_code == 200:
                    response = simplejson.loads(r.content)

                    # save
                    grant = AuthorizationCodeGrantPds()

                    user_profile = Profile.objects.get(email=get_user_email())

                    client_id = str(request.GET.get('client_id'))
                    application = Application.objects.get(client_id=client_id)

                    request_ = {'client_id': request.POST.get('client_id'),
                                'redirect_uri': request.POST.get('redirect_uri'),
                                'response_type': request.POST.get('response_type', "code"),
                                'state': request.POST.get('state', None), 'client': application, 'user': user_profile,
                                'scopes': request.POST.get('scope')}

                    code = {'code': response['code']}
                    grant.save_authorization_client_code(get_object(request_), code)

                    return redirect(response['redirect_to']+"&user_id="+str(user_profile.id))
                else:
                    response = {'message': r.content, 'status_code': r.status_code}
                    print "Error " + str(r.content) + " - " + str(r.status_code)
                    return render(request, "oauth2_provider/authorize_error.html", response)
            else:
                log.debug("Redirecting " + request.POST.get('redirect_uri') + "?error=access_denied")
                print "Redirecting " + request.POST.get('redirect_uri') + "?error=access_denied"
                return redirect(request.POST.get('redirect_uri') + "?error=access_denied")
        else:
            return redirect(request.POST.get('redirect_uri') + "?error=method_not_allowed")
    except ServiceUnavailable or TypeError:
        return redirect(request.POST.get('redirect_uri') + "?error=internal_server_error")
    except Application.DoesNotExist:
        return redirect(request.GET.get('redirect_uri') + "?error=Application with the client_id does not exist!")


def oauth_tyk_notify(request):
    print "oauth_tyk_notify"
    try:
        if request.method == 'POST':
            received_json_data = json.loads(request.body)

            refresh_token = received_json_data['refresh_token']
            auth_code = received_json_data['auth_code']
            new_oauth_token = received_json_data['new_oauth_token']
            old_refresh_token = received_json_data['old_refresh_token']
            notification_type = received_json_data['notification_type']

            grant = Grant.objects.get(code=auth_code)

            print "Saving access_token"

            token = {
                'access_token': new_oauth_token,
                'scope': grant.scope,
                'refresh_token': refresh_token,
                'auth_code': auth_code,
                'old_refresh_token': old_refresh_token,
                'notification_type': notification_type,
                'new_oauth_token': new_oauth_token
            }

            request_ = {
                'client': grant.application,
                'user': grant.user,
                'refresh_token': "",
                'grant_type': 'authorization_code'
            }

            pds_auth = AuthorizationCodeGrantPds()
            pds_auth.save_bearer_token(token, get_object(request_))

            return HttpResponse(status=200)
    except Grant.DoesNotExist or Profile.DoesNotExist or Application.DoesNotExist:
        print "exception"
        return HttpResponse(status=404)


def oauth_create_client(request):
    try:
        if request.method == 'POST':
            received_data = json.loads(request.body)

            pds_api_id = str(settings.PDS_API_ID)
            token_callback_ = received_data['redirect_uri']

            payload = "{\"api_id\":\"%s\",\"redirect_uri\":\"%s\"}" % (pds_api_id, token_callback_)

            headers = {
                'content-type': "application/json",
                'cache-control': "no-cache",
                'X-Tyk-Authorization': settings.TYK_AUTHORIZATION_NODE_SECRET,
            }

            print "Sending client creation request"
            req = urllib2.Request(settings.TYK_CREATE_CLIENT_ENDPOINT, data=payload, headers=headers)
            response = urllib2.urlopen(req)

            if response.getcode() == 200:
                response_data = simplejson.loads(response.read())
                client = Application(
                                client_id=response_data['client_id'],
                                client_secret=response_data['secret'],
                                redirect_uris=response_data['redirect_uri'],
                                authorization_grant_type='authorization-code',
                                client_type='public',
                                name=received_data['client_name']
                            )

                client.save()
                print "Client saved, returning!"

                return JsonResponse({
                    'client_id':response_data['client_id'],
                    'client_secret':response_data['secret'],
                    'redirect_uri':response_data['redirect_uri']})
            else:
                print response.read()
                return HttpResponse(response.read(), status=404)
    except Exception as e:
        print e.message
        return HttpResponse(status=404)
