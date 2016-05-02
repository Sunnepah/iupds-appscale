# coding=utf-8
from google.appengine.api import users
from google.appengine.api.users import UserNotFoundError
import urllib
import urllib2
from google.appengine.api import urlfetch

import simplejson
import json

from .models import Profile, Contact, Address, Application, Grant, AccessToken, RefreshToken
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from iupds import settings

from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes,parser_classes
from rest_framework.response import Response

from sparqlwrapper.SPARQLWrapper import SPARQLWrapper, JSON, XML, N3, RDF, TURTLE, SPARQLWrapper2, SPARQLExceptions
# from rdflib import Graph
import re

from rest_framework.exceptions import APIException
import logging

from django.forms.models import modelform_factory
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView

# ouath2
from oauthlib.oauth2 import BearerToken
from iupdsmanager.authorization_code import AuthorizationCodeGrantPds

# APPSCALE RELATED IMPORT
# import cgi
# from appscalehelper.appscale_user_client import AppscaleUserClient

# uaserver = AppscaleUserClient()

SPARQL_ENDPOINT = settings.SPARQL_ENDPOINT
SPARQL_AUTH_ENDPOINT = settings.SPARQL_AUTH_ENDPOINT

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
            user = get_user_data()

            total_contact_graph = get_total_user_graph()

            return Response({"user": user, "contact_graph": total_contact_graph}, status=status.HTTP_200_OK)
        else:
            users.create_login_url('/')
    else:
        return Response({'status': False, 'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def logout(request):
    if is_logged_in():
        logout_url = users.create_logout_url("/", _auth_domain=None)
        return Response({'logout_url': logout_url}, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'Bad request', 'message': 'The user is not logged in'}, status=status.HTTP_410_GONE)


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
        return Response({'status': 'Bad request', 'message': 'Account could not be created with received data.'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


def index(request):
    user = users.get_current_user()
    if user:
        greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' % (user.nickname(), users.create_logout_url('/')))
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


def get_profile():
    try:
        user = get_user_data()
        user_profile = Profile.objects.get(email=user['email'])
        return user_profile
    except:
        return False


@api_view(['POST'])
def create_contact(request):
    try:
        if is_logged_in():
            user_profile = get_profile()
            phone_contact = _build_phone_contact(request.data, user_profile)
            phone_contact.save()

            email_contact = _build_email_contact(request.data, user_profile)
            email_contact.save()

            # skype_contact = _build_skype_contact(request.data, user_profile)
            # skype_contact.save()

            address = _build_address(request.data, user_profile)
            address.save()

            rdf = generate_contact_rdf(request.data)
            if rdf:
                return Response({'rdf': rdf}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'Can not save data', 'message': 'Error saving to personal store'},
                                status=status.HTTP_304_NOT_MODIFIED)

                # user = get_user_data()

        # return Response({"response": request.data['email']}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Unauthorized', 'message': 'User not logged in'},
                            status=status.HTTP_401_UNAUTHORIZED)
    except UserNotFoundError:
        return None


@api_view(['GET'])
def contact_details(request):
    try:
        if is_logged_in():
            email = query_graph(get_email_graph_uri())
            telephone = query_graph(get_telephone_graph_uri())
            address = query_graph(get_address_graph_uri())
            person = query_graph(get_person_graph_uri())

            return Response({'email': email, 'telephone': telephone, 'address': address, 'person': person},
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Unauthorized', 'message': 'User not logged in'},
                            status=status.HTTP_401_UNAUTHORIZED)
    except UserNotFoundError:
        return Response({'response': 'No content'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def my_contacts(request):
    try:
        if is_logged_in():
            email = query_graph(get_email_graph_uri())
            print email
            telephone = query_graph(get_telephone_graph_uri())
            print telephone
            address = query_graph(get_address_graph_uri())
            print address
            person = query_graph(get_person_graph_uri())
            print person

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
            create_graph(get_person_graph_uri())
            create_graph(get_email_graph_uri())
            create_graph(get_telephone_graph_uri())
            create_graph(get_address_graph_uri())

            return Response({'status': 'Graphs created!'}, status=status.HTTP_200_OK)
        except Exception as e:
            print e
            return Response({'status': 'Server error', 'message': 'Not successful'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'status': 'Bad request', 'message': 'Graph creation was not successful'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['DELETE'])
def drop_graphs(request):
    if request.method == 'DELETE':
        try:
            drop_graph(get_person_graph_uri())
            drop_graph(get_email_graph_uri())
            drop_graph(get_telephone_graph_uri())
            drop_graph(get_address_graph_uri())

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print e
            return Response({'status': 'Server error', 'message': 'Not successful'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'status': 'Bad request', 'message': 'Not successful'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def create_graph_user(request):
    try:
        username = get_user_id()
        create_sql_graph_user(username)

        return Response({'status': 'User created!'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        print e
        return Response({'status': 'Server error', 'message': 'Not successful'}, status=status.HTTP_404_NOT_FOUND)


def is_logged_in():
    try:
        user = users.get_current_user()
        if user is not None:
            return True
        else:
            return False
    except:
        return False


def get_user_data():
    try:
        user = users.get_current_user()
        if user:
            # users.User(email='test@example.com',_user_id='185804764220139124118')
            data = {"email": user.email(), "nickname": user.nickname(), "user_id": user.user_id(),
                    "is_current_user_admin": users.is_current_user_admin()}
            return data
        else:
            users.create_login_url('/')
    except UserNotFoundError:
        return None


def _build_email_contact(data, user_profile):
    return Contact(contact=data["email"], contact_section=Contact.EMAIL, profile_id=user_profile.id)


def _build_phone_contact(data, user_profile):
    if data["telephone_type"] == Contact.HOME:
        _type = Contact.HOME
    elif data["telephone_type"] == Contact.MOBILE:
        _type = Contact.MOBILE
    elif data["telephone_type"] == Contact.OFFICE:
        _type = Contact.OFFICE
    elif data["telephone_type"] == Contact.VOICE:
        _type = Contact.VOICE
    else:
        _type = ""

    return Contact(contact=data["telephone"], contact_type=_type, contact_section=Contact.PHONE,
                   profile_id=user_profile.id)


def _build_skype_contact(data, user_profile):
    return Contact(contact=data["skype"], contact_section=Contact.SKYPE, profile_id=user_profile.id)


def _build_address(data, user_profile):
    if data["street1"] is not None and data["street2"] is not None:
        street = data["street1"] + ", " + data["street2"]
    else:
        street = data["street1"]
    return Address(street=street, city=data["city"], post_code=data["post_code"], profile_id=user_profile.id,
                   primary=True, country=data["country"])


def generate_contact_rdf(data):
    try:
        rdf_persons = ""
        rdf_emails = ""
        rdf_telephones = ""
        rdf_addresses = ""

        nickname = get_profile().username
        full_name = get_profile().full_name
        street_address = data['street1'] + "," + data['street2']
        locality = data['city']
        postal_code = data['post_code']
        country = data['country']
        email = data['email']

        # uid = get_profile().uid
        user_account_identifier = get_person_graph_uri()  # + str(uid)

        rdf_persons += create_triple(user_account_identifier, "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                                     "http://www.w3.org/2006/vcard/ns#Individual")
        rdf_persons += create_triple(user_account_identifier, "http://www.w3.org/2006/vcard/ns#fn", full_name,
                                     "no-type")
        rdf_persons += create_triple(user_account_identifier, "http://www.w3.org/2006/vcard/ns#nickname", nickname)

        print clear_graph(get_person_graph_uri())
        print insert_graph(rdf_persons, get_person_graph_uri())

        # Telephones
        telephone = str(data['telephone']).replace("+", "00")
        telephone_standard = data['telephone']

        rdf_telephones += create_triple(user_account_identifier, "http://www.w3.org/2006/vcard/ns#hasTelephone",
                                        get_telephone_graph_uri() + "/" + telephone)
        rdf_telephones += create_triple(get_telephone_graph_uri() + "/" + telephone,
                                        "http://www.w3.org/2006/vcard/ns#hasValue", "tel:" + telephone_standard)

        if data["telephone_type"] == Contact.HOME:
            telephone_type = "Home"
        elif data["telephone_type"] == Contact.MOBILE:
            telephone_type = "Mobile"
        elif data["telephone_type"] == Contact.OFFICE:
            telephone_type = "Office"
        elif data["telephone_type"] == Contact.VOICE:
            telephone_type = "Voice"
        else:
            telephone_type = ""

        if telephone_type is not None:
            rdf_telephones += create_triple(get_telephone_graph_uri() + "/" + telephone,
                                            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                                            "http://www.w3.org/2006/vcard/ns#" + telephone_type)

        clear_graph(get_telephone_graph_uri())
        insert_graph(rdf_telephones, get_telephone_graph_uri())

        # Emails
        """ TODO Slugify Email """
        formatted_email = re.sub('[^0-9a-zA-Z]+', '-', str(email).lower())
        rdf_emails += create_triple(user_account_identifier, "http://www.w3.org/2006/vcard/ns#hasEmail",
                                    get_email_graph_uri() + "/" + formatted_email)
        rdf_emails += create_triple(get_email_graph_uri() + "/" + formatted_email,
                                    "http://www.w3.org/2006/vcard/ns#hasValue", "mailto:" + email)
        rdf_emails += create_triple(get_email_graph_uri() + "/" + formatted_email,
                                    "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                                    "http://www.w3.org/2006/vcard/ns#Work")

        clear_graph(get_email_graph_uri())
        insert_graph(rdf_emails, get_email_graph_uri())

        # Addresses
        formatted_mustamae = re.sub('[^0-9a-zA-Z]+', '-', str(street_address).lower())
        user_address = get_address_graph_uri() + "/" + formatted_mustamae
        rdf_addresses += create_triple(user_account_identifier, "http://www.w3.org/2006/vcard/ns#hasAddress",
                                       user_address)
        rdf_addresses += create_triple(user_address, "http://www.w3.org/2006/vcard/ns#street-address", street_address,
                                       "no-type")

        rdf_addresses += create_triple(user_address, "http://www.w3.org/2006/vcard/ns#locality", locality, "no-type")
        rdf_addresses += create_triple(user_address, "http://www.w3.org/2006/vcard/ns#postal-code", postal_code,
                                       "no-type")

        rdf_addresses += create_triple(user_address, "http://www.w3.org/2006/vcard/ns#country-name", country, "no-type")
        rdf_addresses += create_triple(user_address, "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                                       "http://www.w3.org/2006/vcard/ns#Home")

        clear_graph(get_address_graph_uri())
        insert_graph(rdf_addresses, get_address_graph_uri())

        return True
    except Exception as e:
        print e
        return False


def create_triple(subject, predicate, object_, type_=""):
    if object_ is None:
        return ""
    else:
        triple = "<" + subject + "> " + "<" + predicate + "> "

        if 'no-type' in type_:
            triple += "\"" + object_ + "\" .\n"
        elif '@et' in type_:
            triple += "\"" + object_ + "\"" + type_ + " .\n"
        elif type_ is None:
            triple += "\"" + object_ + "\"^^<" + type_ + "> .\n"
        else:
            triple += "<" + object_ + "> .\n"

        return triple


def create_graph(graph):
    try:
        sparql = SPARQLWrapper(SPARQL_AUTH_ENDPOINT)
        sparql.setCredentials(get_user_id(), settings.GRAPH_USER_PW)

        sparql.setQuery(""" CREATE GRAPH <""" + graph + """>""")

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print results

        return results
    except Exception as e:
        print e.message
        return list()


def get_user_id():
    user = get_user_data()
    # create virtuoso user
    # nickname_ = slugify(unicode(user['nickname']))
    user_id = str(user['user_id'])
    return user_id


def insert_graph(rdf_triples, graph):
    try:
        sparql = SPARQLWrapper(SPARQL_AUTH_ENDPOINT)
        sparql.setCredentials(get_user_id(), settings.GRAPH_USER_PW)

        query = """ INSERT IN GRAPH <""" + graph + """> { """ + rdf_triples + """ }"""
        print query
        sparql.setQuery(query)

        sparql.setReturnFormat(JSON)
        return sparql.query().convert()
    except Exception as e:
        print e.message
        return list()


def drop_graph(graph):
    try:
        clear_graph(graph)

        sparql = SPARQLWrapper(SPARQL_AUTH_ENDPOINT)
        sparql.setCredentials(get_user_id(), settings.GRAPH_USER_PW)

        sparql.setQuery(""" DROP GRAPH <""" + graph + """>""")

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        print results

        return results
    except Exception as e:
        print e.message
        return list()


def clear_graph(graph):
    try:
        sparql = SPARQLWrapper(SPARQL_AUTH_ENDPOINT)
        sparql.setCredentials(get_user_id(), settings.GRAPH_USER_PW)

        sparql.setQuery(""" CLEAR GRAPH <""" + graph + """>""")

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        return results
    except Exception as e:
        print e.message
        return list()


def query_graph(graph):
    try:
        sparql = SPARQLWrapper(SPARQL_AUTH_ENDPOINT)
        sparql.setCredentials(get_user_id(), settings.GRAPH_USER_PW)

        query = "SELECT * WHERE { GRAPH <" + graph + "> { ?s ?p ?o . } }"

        sparql.setQuery(query)

        # JSON example
        # print '\n\n*** JSON Example'
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        # res = json.dumps(results, separators=(',', ':'))
        return results['results']['bindings']
    except Exception as e:
        print e.message
        return list()


def get_bindings(graph):
    try:
        sparql = SPARQLWrapper(SPARQL_AUTH_ENDPOINT)
        sparql.setCredentials(get_user_id(), settings.GRAPH_USER_PW)
        query = "SELECT * WHERE { GRAPH <" + graph + "> { ?s ?p ?o . } }"

        sparql.setQuery(query)

        results = sparql.query()
        print results.convert()
        print "Bindings:"
        rdf = ""
        for b in results.bindings:
            for v in results.variables:
                try:
                    val = b[v]
                    if val.lang:
                        str_triples = "%s: %s@%s" % (v, val.value, val.lang)
                    elif val.datatype:
                        str_triples = "%s: %s^^%s" % (v, val.value, val.datatype)
                    else:
                        str_triples = "%s: %s" % (v, val.value)
                except KeyError:
                    # no binding to that one...
                    str_triples = "%s: <<None>>" % v
                # print str_triples.encode('utf-8')
                rdf += str_triples.encode('utf-8') + '\n'
                # print
        return rdf
    except:
        return False


def create_sql_graph_user(username, password='secret'):
    remote_command("DB.DBA.USER_CREATE('" + username + "', '" + password + "')")
    remote_command('GRANT SPARQL_SELECT TO "' + username + '"')
    remote_command('GRANT SPARQL_UPDATE TO "' + username + '"')
    remote_command('GRANT SPARQL_SPONGE TO "' + username + '"')

    username = get_user_id()
    # Set graph permissions on just created user
    set_user_permission_on_personal_graph(get_person_graph_uri(), username)
    set_user_permission_on_personal_graph(get_email_graph_uri(), username)
    set_user_permission_on_personal_graph(get_telephone_graph_uri(), username)
    set_user_permission_on_personal_graph(get_address_graph_uri(), username)


def set_user_permission_on_personal_graph(graph, username):
    remote_command("DB.DBA.RDF_DEFAULT_USER_PERMS_SET('" + username + "', 0)")
    # remote_command("DB.DBA.RDF_GRAPH_USER_PERMS_SET('" + graph + "','" + username + "', " + str(1) + ")")
    # remote_command("DB.DBA.RDF_GRAPH_USER_PERMS_SET('" + graph + "','" + username + "', " + str(2) + ")")
    remote_command("DB.DBA.RDF_GRAPH_USER_PERMS_SET('" + graph + "','" + username + "', " + str(3) + ")")
    # remote_command("DB.DBA.RDF_GRAPH_USER_PERMS_SET('" + graph + "','" + username + "', " + str(4) + ")")


def get_email_graph_uri():
    user = get_user_data()
    print settings.GRAPH_ROOT + '/' + str(user['user_id']) + '/emails'
    return settings.GRAPH_ROOT + '/' + str(user['user_id']) + '/emails'


def get_telephone_graph_uri():
    user = get_user_data()
    print settings.GRAPH_ROOT + '/' + str(user['user_id']) + '/telephones'
    return settings.GRAPH_ROOT + '/' + str(user['user_id']) + '/telephones'


def get_address_graph_uri():
    user = get_user_data()
    print settings.GRAPH_ROOT + '/' + str(user['user_id']) + '/addresses'
    return settings.GRAPH_ROOT + '/' + str(user['user_id']) + '/addresses'


def get_person_graph_uri():
    user = get_user_data()
    print settings.GRAPH_ROOT + '/' + str(user['user_id']) + '/persons'
    return settings.GRAPH_ROOT + '/' + str(user['user_id']) + '/persons'


def remote_command(command):
    values = {'cmd': command}

    data = urllib.urlencode(values)
    req = urllib2.Request(settings.REMOTE_COMMAND_HOST, data)
    response = urllib2.urlopen(req)
    print response.read()
    if response.getcode() == 200:
        return True
    else:
        return False


def get_total_user_graph():
    total_telephone_graph = len(query_graph(get_telephone_graph_uri()))
    total_email_graph = len(query_graph(get_email_graph_uri()))
    total_addresses_graph = len(query_graph(get_address_graph_uri()))
    total_persons_graph = len(query_graph(get_person_graph_uri()))
    total_contact_graph = total_telephone_graph + total_email_graph + total_addresses_graph + total_persons_graph

    return total_contact_graph


def oauth_authorize(request):
    try:
        if request.method == 'GET':
            client_id = str(request.GET['client_id'])
            # callback_url = str(request.GET['callback_url'])
            print client_id + " - "

            redirect_url = settings.APPSCALE_APP_URL + "/oauth/authorize/?state=random_state_string&client_id=" + client_id + "&response_type=code"

            if is_logged_in():
                # check
                app = Application.objects.get(client_id=client_id)
                application = {'name': getattr(app, 'name'), 'scopes_descriptions': settings.SCOPES,
                               'scope': " ".join(settings.SCOPES), 'redirect_uri': getattr(app, 'redirect_uris'),
                               'client_id': getattr(app, 'client_id')}

                return render(request, "oauth2_provider/authorize.html", application)
            else:
                return redirect(users.create_login_url(redirect_url))
        elif request.method == 'POST':
            client_id = str(request.GET['client_id'])
            if 'allow' in request.POST and request.POST.get('allow') == 'Authorize':
                token = BearerToken()
                grant = AuthorizationCodeGrantPds()

                userprofile = Profile.objects.get(appscale_user_id=get_user_id())
                request_ = {'client_id': request.POST.get('client_id'),
                            'redirect_uri': request.POST.get('redirect_uri'),
                            'response_type': request.POST.get('response_type', None),
                            'state': request.POST.get('state', None),
                            'client': Application.objects.get(client_id=client_id), 'user': userprofile,
                            'scopes': request.POST.get('scope')}

                uri = grant.create_authorization_response(get_object(request_), token)
                return redirect(uri[0]['Location'])
            else:
                client_id = str(request.GET['client_id'])
                application = Application.objects.get(client_id=client_id)

                log.debug("Redirecting " + application.redirect_uris + "?error=access_denied")
                return redirect(application.redirect_uris + "?error=access_denied")
        else:
            return Response({'status': False, 'message': 'Method not allowed'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except ServiceUnavailable:
        return Response({'status': False, 'message': 'Internal Server Error'}, status=status.HTTP_404_NOT_FOUND)


def oauth_login(request):
    try:
        if request.method == 'GET':
            client_id = str(request.GET['client_id'])
            redirect_uri = str(request.GET['redirect_uri'])
            # Get requesting Client, redirect with error if not found
            print "CLIENT_IT"
            print str(request.GET['client_id'])
            print str(request.GET['redirect_uri'])
            Application.objects.get(client_id=client_id)

            post_login_redirect_url = settings.APPSCALE_APP_URL + "/oauth/login/?client_id=" + client_id + "&response_type=code&redirect_uri=" + redirect_uri + "&state=random_state_string"

            if is_logged_in():
                application = {'name': "App", 'scopes_descriptions': settings.SCOPES,
                               'scope': " ".join(settings.SCOPES), 'redirect_uri': redirect_uri, 'client_id': client_id}

                return render(request, "oauth2_provider/authorize.html", application)
            else:
                return redirect(users.create_login_url(post_login_redirect_url))
        elif request.method == 'POST':
            if 'allow' in request.POST and request.POST.get('allow') == 'Authorize':

                payload = 'response_type=code&client_id='+str(request.POST.get('client_id')).strip()+'&redirect_uri='+str(request.POST.get('redirect_uri')).strip()+'&state='+str(request.POST.get('state')).strip()+'&scope='+str(request.POST.get('scope')).strip()+'&key_rules={"allowance":1000,"rate":1000,"per":60,"expires":'+str(settings.ACCESS_TOKEN_EXPIRE_SECONDS)+',"quota_max":-1,"quota_renews":1406121006,"quota_remaining":0,"quota_renewal_rate":60,"access_rights":{"'+settings.PDS_API_ID+'":{"api_name":"'+settings.PDS_API_NAME+'","api_id":"'+settings.PDS_API_ID+'","versions":["Default"],"allowed_urls":[{"url":"/api/v1/users/'+str(get_user_id()).strip()+'/emails/(.*)","methods":["GET"]},{"url":"/api/v1/users/'+str(get_user_id()).strip()+'/telephones/(.*)","methods":["GET"]},{"url":"/api/v1/users/'+str(get_user_id()).strip()+'/addresses/(.*)","methods":["GET"]},{"url":"/api/v1/users/'+str(get_user_id()).strip()+'/persons/(.*)","methods":["GET"]}]}},"org_id":"'+settings.TYK_API_ORG_ID+'","oauth_client_id":"'+str(request.POST.get('client_id')).strip()+'","hmac_enabled":false,"hmac_string":"","apply_policy_id":"'+settings.TYK_API_POLICY_ID+'"}'

                headers = {'Content-Type': 'application/x-www-form-urlencoded',
                           'x-tyk-authorization': settings.TYK_AUTHORIZATION_NODE_SECRET, 'cache-control': "no-cache"}

                print payload

                # make POST
                r = urlfetch.fetch(url=settings.TYK_OAUTH_AUTHORIZE_ENDPOINT, payload=payload, method=urlfetch.POST,
                                   headers=headers)

                if r.status_code == 200:
                    response = simplejson.loads(r.content)
                    print "serialized code"
                    print response['code']
                    print r.content

                    # save
                    grant = AuthorizationCodeGrantPds()

                    print "User ID"
                    print get_user_id()
                    user_profile = Profile.objects.get(appscale_user_id=get_user_id())

                    client_id = str(request.GET.get('client_id'))
                    application = Application.objects.get(client_id=client_id)

                    request_ = {'client_id': request.POST.get('client_id'),
                                'redirect_uri': request.POST.get('redirect_uri'),
                                'response_type': request.POST.get('response_type', "code"),
                                'state': request.POST.get('state', None), 'client': application, 'user': user_profile,
                                'scopes': request.POST.get('scope')}

                    code = {'code': response['code']}
                    grant.save_authorization_client_code(get_object(request_), code)

                    return redirect(response['redirect_to'])
                else:
                    response = {'message': r.content, 'status_code': r.status_code}
                    print "Error " + str(r.content) + " - " + str(r.status_code)
                    return render(request, "oauth2_provider/authorize_error.html", response)
            else:
                log.debug("Redirecting " + request.POST.get('redirect_uri') + "?error=access_denied")
                print "Redirecting " + request.POST.get('redirect_uri') + "?error=access_denied"
                return redirect(request.POST.get('redirect_uri') + "?error=access_denied")
        else:
            return Response({'status': False, 'message': 'Method not allowed'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except ServiceUnavailable:
        return Response({'status': False, 'message': 'Internal Server Error'}, status=status.HTTP_404_NOT_FOUND)
    except Application.DoesNotExist:
        return redirect(request.GET.get('redirect_uri') + "?error=Application with the client_id does not exist!")


def oauth_tyk_notify(request):
    print "oauth_tyk_notify"
    try:
        if request.method == 'POST':
            received_json_data = json.loads(request.body)
            print received_json_data
            refresh_token = received_json_data['refresh_token']
            auth_code = received_json_data['auth_code']
            new_oauth_token = received_json_data['new_oauth_token']
            old_refresh_token = received_json_data['old_refresh_token']
            notification_type = received_json_data['notification_type']

            grant = Grant.objects.get(code=auth_code)
            # application = Application.objects.get(pk=grant.application)
            # user_profile = Profile.objects.get(pk=grant.user)

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

            # {
            #     "access_token": "101f6bdb7f05f4dd5579e1ee5f1d46952",
            #     "expires_in": 3600,
            #     "refresh_token": "ODhiMGQ5M2EtYjAxOC00OTc4LTUzMTgtZjBhZTQ4ZTEzNWVh",
            #     "scope": "read",
            #     "token_type": "bearer"
            # }

            pds_auth = AuthorizationCodeGrantPds()
            pds_auth.save_bearer_token(token, get_object(request_))

            return HttpResponse(status=200)
    except Grant.DoesNotExist or Profile.DoesNotExist or Application.DoesNotExist:
        print "exception"
        return HttpResponse(status=404)


class ApplicationRegistration(CreateView):
    """
    View used to register a new Application for the request.user
    """
    template_name = "oauth2_provider/application_registration_form.html"

    def get_form_class(self):
        """
        Returns the form class for the application model
        """
        return modelform_factory(Application, fields=(
        'name', 'client_id', 'client_secret', 'client_type', 'authorization_grant_type', 'redirect_uris'))


class ApplicationOwnerIsUserMixin():
    """
    This mixin is used to provide an Application queryset filtered by the current request.user.
    """
    fields = '__all__'

    def get_queryset(self):
        print get_user_id()
        profile = Profile.objects.get(appscale_user_id=get_user_id())

        return Application.objects.filter(user_id=profile.id)


class ApplicationList(ApplicationOwnerIsUserMixin, ListView):
    """
    List view for all the applications owned by the request.user
    """
    context_object_name = 'applications'
    template_name = "oauth2_provider/application_list.html"


class ApplicationDetail(ApplicationOwnerIsUserMixin, DetailView):
    """
    Detail view for an application instance owned by the request.user
    """
    context_object_name = 'application'
    template_name = "oauth2_provider/application_detail.html"


class ApplicationUpdate(ApplicationOwnerIsUserMixin, UpdateView):
    """
    View used to update an application owned by the request.user
    """
    context_object_name = 'application'
    template_name = "oauth2_provider/application_form.html"


class ApplicationDelete(ApplicationOwnerIsUserMixin, DeleteView):
    """
    View used to delete an application owned by the request.user
    """
    context_object_name = 'application'
    success_url = reverse_lazy('oauth2_provider:list')
    template_name = "oauth2_provider/application_confirm_delete.html"


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
