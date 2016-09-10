# coding=utf-8

from google.appengine.api import users
from google.appengine.api.users import UserNotFoundError
import json
import cgi
import logging
from random import randint

from .models import Profile, Contact
from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from iupds import settings
from graph import Graph
from user_data import UserData

SPARQL_ENDPOINT = settings.SPARQL_ENDPOINT
SPARQL_AUTH_ENDPOINT = settings.SPARQL_AUTH_ENDPOINT
GRAPH_USER_PERMISSION_ENDPOINT = settings.GRAPH_USER_PERMISSION_ENDPOINT
NEW_SQL_USER_ENDPOINT = settings.NEW_SQL_USER_ENDPOINT

graph = Graph(SPARQL_AUTH_ENDPOINT, "", "", GRAPH_USER_PERMISSION_ENDPOINT, NEW_SQL_USER_ENDPOINT, settings.GRAPH_ROOT)
user_data = UserData()

log = logging.getLogger('oauth2_provider')
logging.basicConfig(level=logging.DEBUG)
# log = logging.getLogger(__name__)


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'


@api_view(['GET'])
def profile(request):
    if request.method == 'GET':
        if is_logged_in():
            user = user_data.get_user_data()

            total_contact_graph = graph.get_total_user_graph(user_data.get_user_id())

            return Response({"user": user, "contact_graph": total_contact_graph}, status=status.HTTP_200_OK)
        else:
            users.create_login_url('/')
    else:
        return Response({'status': False, 'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def index(request):
    user = users.get_current_user()
    if user:
        greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' % (user.nickname(), users.create_logout_url('/')))

        context = {'user': user, 'greeting': greeting}
        return render(request, 'layout.html', context)
    else:
        users.create_login_url('/')


@api_view(['POST'])
def create_contact(request):
    try:
        if is_logged_in():
            user_profile = user_data.get_profile()
            phone_contact = Contact.build_phone_contact(request.data, user_profile)
            phone_contact.save()

            email_contact = Contact.build_email_contact(request.data, user_profile)
            email_contact.save()

            address = Contact.build_address(request.data, user_profile)
            address.save()

            rdf = graph.insert_contact_rdf(user_data.get_user_id(), user_profile, request.data)
            if rdf:
                return Response({'rdf': rdf}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'Can not save data', 'message': 'Error saving to personal store'},
                                status=status.HTTP_304_NOT_MODIFIED)
        else:
            return Response({'status': 'Unauthorized', 'message': 'User not logged in'},
                            status=status.HTTP_401_UNAUTHORIZED)
    except UserNotFoundError:
        return None


@api_view(['GET'])
def get_contact_details(request):
    try:
        if is_logged_in():
            email = graph.query_graph(graph.get_graph_uri(user_data.get_user_id(), graph.EMAILS_GRAPH))
            telephone = graph.query_graph(graph.get_graph_uri(user_data.get_user_id(), graph.TELEPHONES_GRAPH))
            address = graph.query_graph(graph.get_graph_uri(user_data.get_user_id(), graph.ADDRESSES_GRAPH))
            person = graph.query_graph(graph.get_graph_uri(user_data.get_user_id(), graph.PERSONS_GRAPH))

            return Response({'email': email, 'telephone': telephone, 'address': address, 'person': person},
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Unauthorized', 'message': 'User not logged in'},
                            status=status.HTTP_401_UNAUTHORIZED)
    except UserNotFoundError:
        return Response({'response': 'No content'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def create_graphs(request):
    if request.method == 'POST':
        try:

            return Response({'status': 'Graphs created!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'Server error', 'message': 'Not successful'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'status': 'Bad request', 'message': 'Graph creation was not successful'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['DELETE'])
def drop_graphs(request):
    if request.method == 'DELETE':
        try:
            graph.drop_graph(graph.get_graph_uri(user_data.get_user_id(), graph.PERSONS_GRAPH))
            graph.drop_graph(graph.get_graph_uri(user_data.get_user_id(), graph.EMAILS_GRAPH))
            graph.drop_graph(graph.get_graph_uri(user_data.get_user_id(), graph.TELEPHONES_GRAPH))
            graph.drop_graph(graph.get_graph_uri(user_data.get_user_id(), graph.TELEPHONES_GRAPH))

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'Server error', 'message': 'Not successful'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'status': 'Bad request', 'message': 'Not successful'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def create_graph_user(request):
    try:
        username = user_data.get_user_id()
        if graph.create_sql_graph_user(username):
            graph.create_user_graphs(username)

            return Response({'status': 'User created!'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'status': 'Server error', 'message': 'Not successful'}, status=status.HTTP_404_NOT_FOUND)


# When new user is created via AppScale Signup,
# this endpoint is called to create sql user, setup the user graphs and profiles
def new_user(request):
    print "Create New User"
    try:
        if request.method == 'POST':
            received_json_data = json.loads(request.body)

            email = cgi.escape(received_json_data['email'])

            print "Creating User"
            id = randint(100, 999)  # randint is inclusive at both ends
            new_profile = Profile(uid=id, email=email, username=email, appscale_user_id=id, user_id_old=id)
            new_profile.save()
            print "New User created!"

            print "Creating SQl User"
            if graph.create_sql_graph_user(new_profile.id):
                print "Creating User graphs"
                graph.create_user_graphs()

            return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=404)


def is_logged_in():
    try:
        if users.get_current_user() is not None:
            return True
        else:
            return False
    except:
        return False


class Struct(object):
    def __init__(self, adict):
        """Convert a dictionary to a class

        @param :adict Dictionary
        """
        self.__dict__.update(adict)
        for k, v in adict.items():
            if isinstance(v, dict):
                self.__dict__[k] = Struct(v)


def get_object(adict):
    """Convert a dictionary to a class

    @param :a dict Dictionary
    @return :class:Struct
    """
    return Struct(adict)

