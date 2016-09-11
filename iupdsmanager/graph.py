# -*- coding: utf-8 -*-
import urllib
import urllib2

import re

from sparqlwrapper.SPARQLWrapper import SPARQLWrapper, JSON

from iupdsmanager.models import Contact


class Graph:

    def __init__(self, sparql_auth_endpoint, user_id, password, user_permission_endpoint, new_sql_user_endpoint,
                 graph_root="https://mypds.me/users"):
        """
        Class
        """
        self.NEW_SQL_USER_ENDPOINT = new_sql_user_endpoint
        self.GRAPH_USER_PERMISSION_ENDPOINT = user_permission_endpoint
        self.SPARQL_AUTH_ENDPOINT = sparql_auth_endpoint
        self.GRAPH_USER_ID = user_id
        self.GRAPH_USER_PW = password
        self.GRAPH_ROOT = graph_root

        self.sparql = SPARQLWrapper(self.SPARQL_AUTH_ENDPOINT)
        self.sparql.setCredentials(self.GRAPH_USER_ID, self.GRAPH_USER_PW)

        self.PERSONS_GRAPH = "persons"
        self.EMAILS_GRAPH = "emails"
        self.ADDRESSES_GRAPH = "addresses"
        self.TELEPHONES_GRAPH = "telephones"

    def insert_graph(self, rdf_triples, graph):
        try:
            query = """ INSERT IN GRAPH <""" + graph + """> { """ + rdf_triples + """ }"""

            self.sparql.setQuery(query)
            self.sparql.setReturnFormat(JSON)

            return self.sparql.query().convert()
        except Exception as e:
            return list()

    def drop_graph(self, graph):
        try:
            self.clear_graph(graph)

            self.sparql.setQuery(""" DROP GRAPH <""" + graph + """>""")
            self.sparql.setReturnFormat(JSON)

            return self.sparql.query().convert()
        except Exception as e:
            return list()

    def clear_graph(self, graph):
        try:
            self.sparql.setQuery(""" CLEAR GRAPH <""" + graph + """>""")
            self.sparql.setReturnFormat(JSON)

            return self.sparql.query().convert()
        except Exception as e:
            return list()

    def query_graph(self, graph):
        try:
            query = "SELECT * WHERE { GRAPH <" + graph + "> { ?s ?p ?o . } }"

            self.sparql.setQuery(query)
            self.sparql.setReturnFormat(JSON)
            results = self.sparql.query().convert()

            return results['results']['bindings']
        except Exception as e:
            return list()

    def get_bindings(self, graph):
        try:
            query = "SELECT * WHERE { GRAPH <" + graph + "> { ?s ?p ?o . } }"

            self.sparql.setQuery(query)
            results = self.sparql.query()

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

    def create_sql_graph_user(self, username):
        data = {'username': username}

        data = urllib.urlencode(data)
        req = urllib2.Request(self.NEW_SQL_USER_ENDPOINT, data)
        response = urllib2.urlopen(req)

        if response.getcode() == 200:
            return True
        else:
            return False

    def create_graph(self, graph):
        try:
            if self.set_user_permission_on_graph(graph, self.GRAPH_USER_ID):

                self.sparql.setQuery(""" CREATE GRAPH <""" + graph + """>""")
                self.sparql.setReturnFormat(JSON)

                return self.sparql.query().convert()

            return False
        except Exception as e:
            return list()

    def set_user_permission_on_graph(self, graph, username):
        data = {'username': username, 'graph': graph}

        data = urllib.urlencode(data)
        req = urllib2.Request(self.GRAPH_USER_PERMISSION_ENDPOINT, data)
        response = urllib2.urlopen(req)

        if response.getcode() == 200:
            return True

        return False

    def get_graph_uri(self, user_id, graph_name):
        return self.GRAPH_ROOT + "/" + user_id + "/" + graph_name

    def get_total_user_graph(self, user_id, graph=None):

        if graph is not None:
            return self.get_user_graph_count(graph)

        total = self.get_user_graph_count(self.get_graph_uri(user_id, self.PERSONS_GRAPH))
        total += self.get_user_graph_count(self.get_graph_uri(user_id, self.EMAILS_GRAPH))
        total += self.get_user_graph_count(self.get_graph_uri(user_id, self.ADDRESSES_GRAPH))
        total += self.get_user_graph_count(self.get_graph_uri(user_id, self.TELEPHONES_GRAPH))

        return total

    def get_user_graph_count(self, graph):
        return len(self.query_graph(graph))

    @staticmethod
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

    def insert_contact_rdf(self, user_id, user_profile, data,):
        try:
            user_account_identifier = self.get_graph_uri(user_id, self.PERSONS_GRAPH)

            # Person Graph
            persons_rdf = self.generate_persons_rdf(user_profile, user_account_identifier)
            person_graph_uri = self.get_graph_uri(user_id, self.PERSONS_GRAPH)
            self.clear_graph(person_graph_uri)
            self.insert_graph(persons_rdf, person_graph_uri)

            # Telephones Graph
            telephone_graph_uri = self.get_graph_uri(user_id, self.TELEPHONES_GRAPH)
            telephones_rdf = self.generate_telephone_rdf(user_account_identifier, telephone_graph_uri, data)
            self.clear_graph(telephone_graph_uri)
            self.insert_graph(telephones_rdf, telephone_graph_uri)

            # ===== Emails Graph =========
            """ TODO Slugify Email """
            email = data['email']
            formatted_email = re.sub('[^0-9a-zA-Z]+', '-', str(email).lower())

            email_graph_uri = self.get_graph_uri(user_id, self.EMAILS_GRAPH)

            emails_rdf = self.generate_email_rdf(user_account_identifier, email_graph_uri, email, formatted_email)
            self.clear_graph(email_graph_uri)
            self.insert_graph(emails_rdf, email_graph_uri)

            # ========= Addresses =========
            addresses_graph_uri = self.get_graph_uri(user_id, self.ADDRESSES_GRAPH)
            addresses_rdf = self.generate_addresses_rdf(user_account_identifier, addresses_graph_uri, data)
            self.clear_graph(addresses_graph_uri)
            self.insert_graph(addresses_rdf, addresses_graph_uri)

            return True
        except Exception as e:
            return False

    def generate_addresses_rdf(self, user_account_identifier, addresses_graph_uri, data):

        street_address = data['street1'] + "," + data['street2']
        locality = data['city']
        postal_code = data['post_code']
        country = data['country']

        formatted_mustamae = re.sub('[^0-9a-zA-Z]+', '-', str(street_address).lower())
        user_address = addresses_graph_uri + "/" + formatted_mustamae

        addresses_rdf = ""
        addresses_rdf += self.create_triple(user_account_identifier, "http://www.w3.org/2006/vcard/ns#hasAddress",
                                            user_address)
        addresses_rdf += self.create_triple(user_address, "http://www.w3.org/2006/vcard/ns#street-address",
                                            street_address, "no-type")
        addresses_rdf += self.create_triple(user_address, "http://www.w3.org/2006/vcard/ns#locality", locality,
                                            "no-type")
        addresses_rdf += self.create_triple(user_address, "http://www.w3.org/2006/vcard/ns#postal-code",
                                            postal_code, "no-type")
        addresses_rdf += self.create_triple(user_address, "http://www.w3.org/2006/vcard/ns#country-name", country,
                                            "no-type")
        addresses_rdf += self.create_triple(user_address, "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                                            "http://www.w3.org/2006/vcard/ns#Home")

        return addresses_rdf

    def generate_email_rdf(self, user_account_identifier, email_graph_uri, email, formatted_email):
        emails_rdf = ""
        emails_rdf += self.create_triple(user_account_identifier, "http://www.w3.org/2006/vcard/ns#hasEmail",
                                         email_graph_uri + "/" + formatted_email)
        emails_rdf += self.create_triple(email_graph_uri + "/" + formatted_email,
                                         "http://www.w3.org/2006/vcard/ns#hasValue", "mailto:" + email)
        emails_rdf += self.create_triple(email_graph_uri + "/" + formatted_email,
                                         "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                                         "http://www.w3.org/2006/vcard/ns#Work")

        return emails_rdf

    def generate_telephone_rdf(self, user_account_identifier, telephone_graph_uri, data):
        telephone = str(data['telephone']).replace("+", "00")
        telephone_standard = data['telephone']

        telephones_rdf = ""
        telephones_rdf += self.create_triple(user_account_identifier,
                                             "http://www.w3.org/2006/vcard/ns#hasTelephone",
                                             telephone_graph_uri + "/" + telephone)
        telephones_rdf += self.create_triple(telephone_graph_uri + "/" + telephone,
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
            telephones_rdf += self.create_triple(telephone_graph_uri + "/" + telephone,
                                                 "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                                                 "http://www.w3.org/2006/vcard/ns#" + telephone_type)

        return telephones_rdf

    def generate_persons_rdf(self, user_profile, user_account_identifier):
        persons_rdf = ""

        persons_rdf += self.create_triple(user_account_identifier,
                                          "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                                          "http://www.w3.org/2006/vcard/ns#Individual")
        persons_rdf += self.create_triple(user_account_identifier, "http://www.w3.org/2006/vcard/ns#fn",
                                          user_profile.full_name, "no-type")
        persons_rdf += self.create_triple(user_account_identifier, "http://www.w3.org/2006/vcard/ns#nickname",
                                          user_profile.nickname)

        return persons_rdf

    def create_user_graphs(self, username):
        self.clear_graph(self.get_graph_uri(username, self.PERSONS_GRAPH))
