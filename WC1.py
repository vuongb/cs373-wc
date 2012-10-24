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
from StringIO import StringIO
import webapp2
from google.appengine.ext import db
from minixsv import pyxsval as xsv
import xml.etree.ElementTree as ET
from importer import process_crisis, process_organization, process_person
import logging
import exporter
from Models import Image, Video, Map, Social, ExternalLink, Citation



def application_key(application_name = None):
    return db.Key.from_path('Crises Center', application_name or 'default_application')

def get_tree_and_validate(data, schema):
    try:
        xsv.parseAndValidateXmlInputString(data, schema, xmlIfClass=xsv.XMLIF_ELEMENTTREE)
        return ET.parse(StringIO(data))
    except xsv.XsvalError as e:
        print("XML did not validate\n"+str(e))
        return 0
    except Exception as e:
        logging.info('bad file\n' + str(e))
        return 0

#http://stackoverflow.com/questions/7684333/converting-xml-to-dictionary-using-elementtree
def etree_to_dict(t):
    if t.getchildren() == []:
        d = {t.tag: t.text}
    else:
        d = {t.tag : map(etree_to_dict, t.getchildren())}
    return d


def store_special_classes(result_dict, assoc_obj):
    # this is nuts. If you have questions, debug.
    videos          = result_dict.get('videos')
    if videos:
        for video in videos:
            builder                 = {}
            builder['video_type']   = video.items()[0][0]
            builder['video_id']     = video.items()[0][1]
            builder['assoc_object'] = assoc_obj
            Video(**builder).put()
    social          = result_dict.get('social')
    if social:
        for media in social:
            builder                 = {}
            builder['social_type']  = media.items()[0][0]
            builder['social_id']    = media.items()[0][1]
            builder['assoc_object'] = assoc_obj
            Social(**builder).put()
    images          = result_dict.get('images')
    if images:
        for image in images:
            builder                 = {}
            builder['source']       = image.get('source')
            builder['description']  = image.get('description')
            builder['assoc_object'] = assoc_obj
            Image(**builder).put()
    maps            = result_dict.get('maps')
    if maps:
        for map in maps:
            builder                 = {}
            builder['source']       = map.get('source')
            builder['description']  = map.get('description')
            builder['assoc_object'] = assoc_obj
            Map(**builder).put()
    citations       = result_dict.get('citations')
    if citations:
        for citation in citations:
            builder                 = {}
            builder['source']       = citation.get('source')
            builder['description']  = citation.get('description')
            builder['assoc_object'] = assoc_obj
            Citation(**builder).put()
    external_links  = result_dict.get('external_links')
    if external_links:
        for link in external_links:
            builder                 = {}
            builder['source']       = link.get('source')
            builder['description']  = link.get('description')
            builder['assoc_object'] = assoc_obj
            ExternalLink(**builder).put()


class ImportHandler(webapp2.RequestHandler):
    def post(self):
        password = self.request.get('pass')
        if password == 'hunter2':

            self.response.out.write('Authorized.')
            upload_request = self.request.get('uploaded_file')

            if upload_request != '':

                SCHEMA  ='unicornSteroids.xsd'

                tree = get_tree_and_validate(upload_request, open(SCHEMA, 'r').read())
                if tree == 0:
                    self.response.out.write('The file you uploaded is not valid. Please try again')
                else:
                    self.response.out.write('Your file has validated')

                root    = tree.getroot()
                # iterate over types
                for i in root.iter():
                    if i.tag == 'crises':
                        # iterate through all crises
                        d = etree_to_dict(i)
                        for c in d.get('crises'):
                            if type(c) != str:
                                result_dict     = process_crisis(c)
                                crisis          = result_dict.get('crisis')
                                crisis.put()
                                store_special_classes(result_dict, crisis)
                    elif i.tag == 'organizations':
                        # iterate through all organizations
                        d = etree_to_dict(i)
                        logging.info(d)
                        for o in d.get('organizations'):
                            if type(o) != str:
                                result_dict     = process_organization(o)
                                organization    = result_dict.get('organization')
                                organization.put()
                                store_special_classes(result_dict, organization)
                    elif i.tag == 'people':
                        # iterate through all person
                        d = etree_to_dict(i)
                        for p in d.get('people'):
                            if type(p) != str:
                                result_dict     = process_person(p)
                                person          = result_dict.get('person')
                                person.put()
                                store_special_classes(result_dict, person)

        else:
            self.response.out.write("""<h1>Please enter a password</h1>
<form method="post" enctype="multipart/form-data" action="/import">
<input type="file" name="uploaded_file"/>
<input type="password" name="pass"/>
<input type="submit" value="login"/>
</form>""")

    def get(self):
        self.post()


class ExportHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "text/xml; charset=utf-8"
        root = exporter.buildTree()
        logging.info("root: %s", root)
        output = ET.tostring(root)
        self.response.out.write(unicode(output,"UTF-8"))


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

    def get_externalLink(self):
        return db.GqlQuery("SELECT * "
                           "FROM ExternalLink "
                           "WHERE ANCESTOR IS :1 "
                           "ORDER BY description DESC",
                            application_key(self.application_name))

    def get_citation(self):
        return db.GqlQuery("SELECT * "
                           "FROM Citation "
                           "WHERE ANCESTOR IS :1 "
                           "ORDER BY description DESC",
                            application_key(self.application_name))

    def get_map(self):
        return db.GqlQuery("SELECT * "
                           "FROM Map "
                           "WHERE ANCESTOR IS :1 "
                           "ORDER BY description DESC",
                            application_key(self.application_name))

    def get_image(self):
        return db.GqlQuery("SELECT * "
                           "FROM Image "
                           "WHERE ANCESTOR IS :1 "
                           "ORDER BY description DESC",
                            application_key(self.application_name))

    def get_social(self):
        return db.GqlQuery("SELECT * "
                           "FROM Social "
                           "WHERE ANCESTOR IS :1 "
                           "ORDER BY social_id DESC",
                            application_key(self.application_name))

    def get_video(self):
        return db.GqlQuery("SELECT * "
                           "FROM Video "
                           "WHERE ANCESTOR IS :1 "
                           "ORDER BY video_id DESC",
                            application_key(self.application_name))



    def to_ul(self, col):
        return "<ul>" + "\n".join(["<li>" + str(item) + "</li>" for item in col]) + "</ul>"


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/import', ImportHandler),
    ('/export', ExportHandler)
], debug=True)
