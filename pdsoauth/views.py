# coding=utf-8
from google.appengine.api import users

from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from google.appengine.api import urlfetch
from iupds import settings
import simplejson

from iupdsmanager.views import is_logged_in, get_user_email
from iupdsmanager.models import Application, Profile, AccessToken


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
                applications = Application.objects.get(user=user_profile).values()

                print applications

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
                token = AccessToken.objects.get(application=application)

                # make DELETE
                r = urlfetch.fetch(url=settings.TYK_DELETE_ACCESS_TOKEN + "/" +
                                   token['token'] + "?api_id=" + settings.PDS_API_ID,
                                   method=urlfetch.DELETE, headers=headers)

                if r.status_code == 200:
                    response = simplejson.loads(r.content)
                    print "Delete token from tyk"
                    print response

                    token.delete()
                    application.delete()

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

# @api_view(['GET', 'POST'])
# def snippet_list(request):
#     """
#     List all snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# url=settings.TYK_INVALIDATE_REFRESH_TOKEN + "/"
#  + settings.TOKEN_DELETE + "?api_id=" + settings.PDS_API_ID,
# api_id={api_id}
