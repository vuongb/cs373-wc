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

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

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
    name            = db.StringProperty(required=True)
    alternameNames  = db.StringListProperty()
    kind            = db.StringProperty(required=True)
    citations       = db.StringListProperty()
    externalLinks   = db.StringListProperty()
    history         = db.TextProperty()

    # Location
    city            = db.StringProperty()
    state           = db.StringProperty()
    country         = db.StringProperty(required=True)

    # Media
    images          = db.StringListProperty()
    video           = db.StringListProperty()
    social          = db.StringListProperty()

    # Contact Info
    address         = db.StringProperty()
    email           = db.StringProperty()
    phone           = db.StringProperty()

class People(db.Model):
    # Base Data
    name            = db.StringProperty(required=True)
    alternameNames  = db.StringListProperty()
    kind            = db.StringProperty(required=True)
    citations       = db.StringListProperty()
    externalLinks   = db.StringListProperty()

    # Location
    city            = db.StringProperty()
    state           = db.StringProperty()
    country         = db.StringProperty(required=True)

    # Media
    images          = db.StringListProperty()
    video           = db.StringListProperty()
    social          = db.StringListProperty()

class Crisis(db.Model):
    # Base Data
    name            = db.StringProperty(required=True)
    alternameNames  = db.StringListProperty()
    kind            = db.StringProperty(required=True)
    citations       = db.StringListProperty()
    startDate       = db.DateProperty()
    endDate         = db.DateProperty()
    economicImpact  = db.IntegerProperty(required=True)
    resoucesNeeded  = db.StringListProperty()
    waysToHelp      = db.StringListProperty()

    # Location
    city            = db.StringProperty()
    state           = db.StringProperty()
    country         = db.StringProperty(required=True)

    # Media
    images          = db.StringListProperty()
    video           = db.StringListProperty()
    social          = db.StringListProperty()

    # External Links
    link            = db.StringProperty()
    description     = db.TextProperty()

    # Human Impact
    deaths          = db.IntegerProperty()
    missing         = db.IntegerProperty()
    injured         = db.IntegerProperty()
    displaced       = db.IntegerProperty()


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
    
    
