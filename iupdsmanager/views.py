# coding=utf-8
from google.appengine.api import users
from google.appengine.api.users import UserNotFoundError
from slugify import slugify

# from django.core import serializers
# from django.http import HttpResponse
from .models import Profile, Contact, Address
from django.shortcuts import render
from django.shortcuts import redirect
from iupds import settings

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from sparqlwrapper.SPARQLWrapper import SPARQLWrapper, JSON, XML, N3, RDF, TURTLE, SPARQLWrapper2, SPARQLExceptions
from rdflib import Graph
import re

import urllib
import urllib2
import json

# import pprint
# APPSCALE RELATED IMPORT
# import cgi
# from appscalehelper.appscale_user_client import AppscaleUserClient

# uaserver = AppscaleUserClient()

SPARQL_ENDPOINT = settings.SPARQL_ENDPOINT
SPARQL_AUTH_ENDPOINT = settings.SPARQL_AUTH_ENDPOINT


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
        return Response({
            'status': False,
            'message': 'Method not allowed'
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def logout(request):
    if is_logged_in():
        logout_url = users.create_logout_url("/", _auth_domain=None)
        return Response({'logout_url': logout_url}, status=status.HTTP_200_OK)
    else:
        return Response({
            'status': 'Bad request',
            'message': 'The user is not logged in'
        }, status=status.HTTP_410_GONE)


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
    user = get_user_data()
    user_profile = Profile.objects.get(email=user['email'])
    return user_profile


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
                return Response({
                    'status': 'Can not save data',
                    'message': 'Error saving to personal store'
                }, status=status.HTTP_304_NOT_MODIFIED)

            # user = get_user_data()

        # return Response({"response": request.data['email']}, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'User not logged in'
            }, status=status.HTTP_401_UNAUTHORIZED)
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
            return Response({
                'status': 'Unauthorized',
                'message': 'User not logged in'
            }, status=status.HTTP_401_UNAUTHORIZED)
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
            return Response({
                'status': 'Unauthorized',
                'message': 'User not logged in'
            }, status=status.HTTP_401_UNAUTHORIZED)
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

            return Response({
                'status': 'Graphs created!'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print e
            return Response({
                'status': 'Server error',
                'message': 'Not successful'
            }, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({
            'status': 'Bad request',
            'message': 'Graph creation was not successful'
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


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
            return Response({
                'status': 'Server error',
                'message': 'Not successful'
            }, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({
            'status': 'Bad request',
            'message': 'Not successful'
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def create_graph_user(request):
    try:
        username = get_user_id()
        create_sql_graph_user(username)

        return Response({
            'status': 'User created!'
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        print e
        return Response({
            'status': 'Server error',
            'message': 'Not successful'
        }, status=status.HTTP_404_NOT_FOUND)


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
                   primary=True,
                   country=data["country"])


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
        user_account_identifier = get_person_graph_uri()    # + str(uid)

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
        rdf_emails += create_triple(get_email_graph_uri() + "/" + formatted_email, "http://www.w3.org/2006/vcard/ns#hasValue",
                                    "mailto:" + email)
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


def test_rdf():
    g = Graph()
    g.parse("/Users/sunnepah/appscale/apps/ipds-gae-django-skeleton/contactrdf.nt", format="nt")
    return len(g)


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


@api_view(['GET'])
def oauth_authorize(request):
    if request.method == 'GET':
        client_id = request.query_params.get('client_id', None)
        callback_url = request.query_params.get('callback_url', None)

        redirect_url = "http://127.0.0.1:8000/o/token/?state=random_state_string&client_id=" + client_id + \
                       "&response_type=code&callback_url=" + callback_url

        if is_logged_in():
            return redirect(redirect_url)
        else:
            return redirect(users.create_login_url(redirect_url))
    else:
        return Response({
            'status': False,
            'message': 'Method not allowed'
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
