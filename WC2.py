#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from importer import get_tree_and_validate, str_from_tree, put_objects
import logging
import exporter
from Models import Crisis, Organization, Person
from merge import distinct
from search import process_search_query
from google.appengine.ext import db
from google.appengine.ext.webapp import template
import os
import urllib
from urlparse import urlparse, parse_qs

class ImportHandler(webapp2.RequestHandler):
    """ Handles the interaction between the client and the server for importing xml files into our datastore """

    SCHEMA = 'WC2.xsd' # the schema that all xml is validated against
    PASSWORD = 'hunter2' # the password required for upload and import functionality

    def post(self):
        data = {
            'title': "Import",
            'import_active': "active"
        }
        password = self.request.get('pass')
        if password == 'hunter2':
            data['login'] = True
            upload_request = self.request.get('uploaded_file') #upload request contains the raw data from the file
            if upload_request != '':
                # We only want to reach this section if the user actually attempted to upload a file
                tree = get_tree_and_validate(upload_request, open(self.SCHEMA, 'r').read())
                if tree != 0:
                    data['valid'] = True
                    root = tree.getroot()
                    # If we successfully loaded xml data into the datastore
                    if put_objects(root):
                        data['success'] = True
            else:
                data['no_file'] = True
                data['login'] = False
        else:
            data['login_failure'] = True
        path = os.path.join(os.path.dirname(__file__), 'templates/import.phtml')
        self.response.out.write(template.render(path, data))

    def get(self):
        # This section is reached when a user clicks on "Import" on the main page, but we want a post, not a get.
        data = {
            'title': "Import",
            'import_active': "active"
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/import.phtml')
        self.response.out.write(template.render(path, data))


class ExportHandler(webapp2.RequestHandler):
    """ Renders the page for exporting objects from our datastore to XML """

    def get(self):
        self.response.headers['Content-Type'] = "text/xml; charset=utf-8"
        root = exporter.buildTree()
        logging.info("root: %s", root)
        output = str_from_tree(root)
        self.response.out.write(unicode(output, "UTF-8"))


class IndexPage(webapp2.RequestHandler):
    """ Renders the home page """

    def get(self):
        crises          = query_distinct("SELECT * FROM Crisis")
        organizations   = query_distinct("SELECT * FROM Organization")
        people          = query_distinct("SELECT * FROM Person")

        data = {
            'title'         : "Home",
            'crises'        : crises,
            'organizations' : organizations,
            'people'        : people,
            'home_active'   : "active"
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/index.phtml')
        self.response.out.write(template.render(path, data))

class CrisisPage(webapp2.RequestHandler):
    def get(self, id=None):
        if id is None:
            #Base Crisis Page
            path = os.path.join(os.path.dirname(__file__), 'templates/index.phtml')
            #Get list of crises and print links
            crises = query_distinct("SELECT * FROM Crisis")
            data = {
                'title': "Crises",
                'crises': crises
            }
        else:
            #Individual Crisis Page
            path = os.path.join(os.path.dirname(__file__), 'templates/crisis.phtml')
            crisis = Crisis.get_by_id(int(id))
            #Get individual crisis object from id
            data = {
                'object': crisis
            }
        data['crises_active'] = "active"
        self.response.out.write(template.render(path, data))


class OrganizationPage(webapp2.RequestHandler):
    def get(self, id=None):
        if id is None:
            #Base Organization Page
            path = os.path.join(os.path.dirname(__file__), 'templates/index.phtml')
            #Get list of organizations and print links
            organizations = query_distinct("SELECT * FROM Organization")
            data = {
                'title': "Organizations",
                'organizations': organizations
            }
        else:
            #Individual Organization Page
            path = os.path.join(os.path.dirname(__file__), 'templates/organization.phtml')
            organization = Organization.get_by_id(int(id))
            #Get individual organization object from id
            data = {
                'object': organization
            }
        data['organizations_active'] = "active"
        self.response.out.write(template.render(path, data))


class PersonPage(webapp2.RequestHandler):
    def get(self, id=None):
        if id is None:
            #Base Person Page
            path = os.path.join(os.path.dirname(__file__), 'templates/index.phtml')
            #Get list of crises and print links
            people = query_distinct("SELECT * FROM Person")
            data = {
                'title': "People",
                'people': people
            }
        else:
            #Individual Person Page
            path = os.path.join(os.path.dirname(__file__), 'templates/person.phtml')
            person = Person.get_by_id(int(id))
            #Get individual crisis object from id
            data = {
                'object': person
            }
        data['people_active'] = "active"
        self.response.out.write(template.render(path, data))

class SearchHandler(webapp2.RequestHandler):

    def post(self):
        """ Handles a search request and redirects to results """
        query = self.request.get('search_query')
        if query:
            self.redirect('/search?' + urllib.urlencode(
            #{'query': query}))
            {'query': query.encode('utf-8')}))
        else:
            self.redirect('/')

    def get(self):
        """ Parses query and redirects to Search Results page"""

        search_results  = {}
        data            = dict()
        valid           = True

        # Parse out the search query (if any)
        uri = urlparse(self.request.uri)
        if uri.query:
            query = parse_qs(uri.query)
            query = query['query'][0]
            query_results = process_search_query(query)

            if query_results == "invalid":
                valid = False
            else:
                # get the model associated with the search result
                for id, descriptions in query_results.items():
                    gql_results = db.GqlQuery("SELECT * FROM Crisis WHERE us_id =:1", id)
                    if gql_results.count() < 1:
                        gql_results = db.GqlQuery("SELECT * FROM Person WHERE us_id =:1", id)
                    if gql_results.count() < 1:
                        gql_results = db.GqlQuery("SELECT * FROM Organization WHERE us_id =:1", id)
                    assert gql_results

                    # built a list of type [ [result name, result url, [descriptions] ] ]
                    for object in gql_results:
                        object_properties = (object.getUrl(), descriptions)
                        if object.us_name not in search_results:
                            search_results[object.us_name] = object_properties

            data = {
                'title'         : "Search Results",
                'search_terms'  : query,
                'search_results': search_results,
                'valid'         : valid
            }
        path = os.path.join(os.path.dirname(__file__), 'templates/search.html')
        self.response.out.write(template.render(path, data))

def query_distinct(s):
    """
    performs a google query and filters non-unique results by us_name
    s is a str representation of a query to execute
    returns a list with us_name as key and the URL as value
    """
    query = db.GqlQuery(s)
    result = dict()
    for i in query:
        if i.us_name not in result:
            result[i.us_name] = i.getUrl()
    return result


app = webapp2.WSGIApplication([
    ('/', IndexPage),
    ('/c/?', CrisisPage),
    (r'/c/(.+)', CrisisPage),
    ('/o/?', OrganizationPage),
    (r'/o/(.+)', OrganizationPage),
    ('/p/?', PersonPage),
    (r'/p/(.+)', PersonPage),
    ('/import', ImportHandler),
    ('/export', ExportHandler),
    ('/search', SearchHandler)
], debug=True)
