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
from google.appengine.ext import db


def application_key(application_name = None):
    return db.Key.from_path('Crises Center', application_name or 'default_application')

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(self.get_header())

        ##todo: not too sure about how or if this works
        ## see https://developers.google.com/appengine/docs/python/gettingstartedpython27/usingdatastore
        self.application_name = self.request.get('application_name')

        crises = self.get_crises()
        organizations = self.get_organizations()
        people = self.get_people()

        body = "Crises\n" + self.to_ul(crises) \
               + "\nOrganizations\n" + self.to_ul(organizations) \
               + "\nPeople\n" + self.to_ul(people)

        self.response.out.write(body)

        self.response.write(self.get_footer())

    def get_header(self):
        return "<html><body>"

    def get_footer(self):
        return "</body></html>"

    def get_crises(self):
        return db.GqlQuery("SELECT * "
                             "FROM Crisis "
                             "WHERE ANCESTOR IS :1 "
                             "ORDER BY us_name DESC",
                             application_key(self.application_name))

    def get_organizations(self):
        return db.GqlQuery("SELECT * "
                           "FROM Organization "
                           "WHERE ANCESTOR IS :1 "
                           "ORDER BY us_name DESC",
                            application_key(self.application_name))

    def get_people(self):
        return db.GqlQuery("SELECT * "
                           "FROM Person "
                           "WHERE ANCESTOR IS :1 "
                           "ORDER BY us_name DESC",
                            application_key(self.application_name))
    def to_ul(self, col):
        return "<ul>" + "\n".join(["<li>" + str(item) + "</li>" for item in col]) + "</ul>"


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)


# One to Many Relationships
class ExternalLink(db.Model):
    title = db.StringProperty(required=True)
    link = db.LinkProperty(required=True)
    # One(object) to many(links)
    # Specifying None for class allows us to use any object for the association
    assoc_object = db.ReferenceProperty(None, collection_name='external_links', required=True)

class Organization(db.Model):
    # Base Data
    us_name            = db.StringProperty(required=True)
    us_alternateNames  = db.StringListProperty()
    us_type            = db.StringProperty(required=True)
    us_citations       = db.StringListProperty()
    us_externalLinks   = db.StringListProperty()
    us_history         = db.TextProperty()

    # Location
    us_city            = db.StringProperty()
    us_state           = db.StringProperty()
    us_country         = db.StringProperty(required=True)

    # Media
    us_images          = db.StringListProperty()
    us_video           = db.StringListProperty()
    us_social          = db.StringListProperty()

    # Contact Info
    us_address         = db.StringProperty()
    us_email           = db.StringProperty()
    us_phone           = db.StringProperty()

class Person(db.Model):
    # Base Data
    us_name            = db.StringProperty(required=True)
    us_alternateNames  = db.StringListProperty()
    us_kind            = db.StringProperty(required=True)
    us_citations       = db.StringListProperty()
    us_externalLinks   = db.StringListProperty()

    # Location
    us_city            = db.StringProperty()
    us_state           = db.StringProperty()
    us_country         = db.StringProperty(required=True)

    # Media
    us_images          = db.StringListProperty()
    us_video           = db.StringListProperty()
    us_social          = db.StringListProperty()

class Crisis(db.Model):
    # Base Data
    us_name            = db.StringProperty(required=True)
    us_alternateNames  = db.StringListProperty()
    us_kind            = db.StringProperty(required=True)
    us_citations       = db.StringListProperty()
    us_startDate       = db.DateProperty()
    us_endDate         = db.DateProperty()
    us_economicImpact  = db.IntegerProperty(required=True)
    us_resoucesNeeded  = db.StringListProperty()
    us_waysToHelp      = db.StringListProperty()

    # Location
    us_city            = db.StringProperty()
    us_state           = db.StringProperty()
    us_country         = db.StringProperty(required=True)

    # Media
    us_images          = db.StringListProperty()
    us_video           = db.StringListProperty()
    us_social          = db.StringListProperty()

    # External Links
    us_link            = db.StringProperty()
    us_description     = db.TextProperty()

    # Human Impact
    us_deaths          = db.IntegerProperty()
    us_missing         = db.IntegerProperty()
    us_injured         = db.IntegerProperty()
    us_displaced       = db.IntegerProperty()


# Many to many relationships
class CrisisOrganization(db.Model):
    crisis = db.ReferenceProperty(Crisis, required=True, collection_name='organizations')
    organization = db.ReferenceProperty(Organization, required=True, collection_name='crises')

class CrisisPerson(db.Model):
    crisis = db.ReferenceProperty(Crisis, required=True, collection_name='people')
    person = db.ReferenceProperty(Person, required=True, collection_name='crises')

class OrganizationPerson(db.Model):
    organization = db.ReferenceProperty(Organization, required=True, collection_name='people')
    person = db.ReferenceProperty(Person, required=True, collection_name='organizations')
    
    
