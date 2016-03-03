from google.appengine.api import users

from django.core import serializers
from django.http import HttpResponse
from .models import Profile
from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# APPSCALE RELATED IMPORT
# import cgi
# from appscalehelper.appscale_user_client import AppscaleUserClient

# uaserver = AppscaleUserClient()


@api_view(['GET'])
def profile(request):
    if request.method == 'GET':
        user = users.get_current_user()
        if user:
            # users.User(email='test@example.com',_user_id='185804764220139124118')
            data = {"email": user.email(),
                    "nickname": user.nickname(),
                    "user_id": user.user_id(),
                    "is_current_user_admin": users.is_current_user_admin()}

            return Response({"user": data}, status=status.HTTP_200_OK)
        else:
            users.create_login_url('/')
    else:
        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def logout(request):
    if request.method == 'POST':
        user = users.get_current_user()
        if user:
            logout_url = users.create_logout_url("/", _auth_domain=None)
            return Response({'logout_url': logout_url}, status=status.HTTP_200_OK)
        else:
            users.create_login_url('/')
    else:
        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        return Response(status=status.HTTP_200_OK)
        # # user_gae = uaserver.get_user_data(request.data['email'])
        # errors = uaserver.parse_new_user_post(request.data['email'], request.data['password'],
        #                                       request.data['password_confirmation'])
    #
    # if errors['email'] or errors['password'] or errors['password_confirmation']:
        #     return False
        # else:
        #     if uaserver.does_user_exist(request.data['email']):
        #         return Response({
        #             'status': 'Conflict',
        #             'message': 'Account could not be created becasue user already exist.'
        #         }, status=status.HTTP_409_CONFLICT)
        #     else:
        #         result = uaserver.create_user(cgi.escape(request.data['email']),
        #                                       cgi.escape(request.data['password']))
        #         if result:
        #             return Response({'response': result}, status=status.HTTP_200_OK)
        #         else:
        #             return Response({'response': result}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


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
    user_profile = Profile.objects.all()
    data = serializers.serialize("json", user_profile)
    return HttpResponse(data)

# Sample Non-model Endpoint
# class ShareView(views.APIView):
#     permission_classes = []
#
#     def post(self, request, *args, **kwargs):
#         email = request.DATA.get('email', None)
#         url = request.DATA.get('url', None)
#         if email and url:
#             share_url(email, url)
#             return Response({"success": True})
#         else:
#             return Response({"success": False})


@api_view(['GET'])
def get_user_data(request):
    if request.method == 'GET':
        user = users.get_current_user()
        if user:
            # users.User(email='test@example.com',_user_id='185804764220139124118')
            data = {"email": user.email(),
                    "nickname": user.nickname(),
                    "user_id": user.user_id(),
                    "is_current_user_admin": users.is_current_user_admin()}

            return Response({"user": data}, status=status.HTTP_200_OK)
        else:
            users.create_login_url('/')
    else:
        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
