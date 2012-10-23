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
from Models import *


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