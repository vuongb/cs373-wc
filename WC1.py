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
from minixsv import pyxsval as xsv
import xml.etree.ElementTree as ET
from importer import process_crisis, process_organization, process_person
from Models import *
import logging


def application_key(application_name = None):
    return db.Key.from_path('Crises Center', application_name or 'default_application')

def get_tree_and_validate(data, schema):
    try:
        wrapper = xsv.parseAndValidateXmlInput(data, schema, xmlIfClass=xsv.XMLIF_ELEMENTTREE)
        return ET.parse(data)
    except xsv.XsvalError as e:
        print("XML did not validate\n"+str(e))

#http://stackoverflow.com/questions/7684333/converting-xml-to-dictionary-using-elementtree
def etree_to_dict(t):
    if t.getchildren() == []:
        d = {t.tag: t.text}
    else:
        d = {t.tag : map(etree_to_dict, t.getchildren())}
    return d

class ImportHandler(webapp2.RequestHandler):
    def get(self):
        SCHEMA  ='cassie-schema-statistics.xsd'
        tree    = get_tree_and_validate('xml_instances/organization-doctors_without_borders.xml', SCHEMA)
        root    = tree.getroot()
        # iterate over types
        for i in root.iter():
            if i.tag == 'crises':
                # iterate through all crises
                d = etree_to_dict(i)
                for c in d.get('crises'):
                    if type(c) != str:
                        crisis_instance = process_crisis(c)
                        crisis_instance.put()
            elif i.tag == 'organizations':
                # iterate through all organizations
                d = etree_to_dict(i)
                logging.info(d)
                for o in d.get('organizations'):
                    if type(o) != str:
                        organization_instance = process_organization(o)
                        organization_instance.put()
            elif i.tag == 'people':
                # iterate through all people
                d = etree_to_dict(i)
                for p in d.get('people'):
                    if type(p) != str:
                        people_instance = process_people(p)
                        people_instance.put()


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
    ('/', MainHandler),
    ('/import', ImportHandler)
], debug=True)
