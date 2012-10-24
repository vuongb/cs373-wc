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



def get_tree_and_validate(data, schema):
    """validate an xml string against a schema string and return an ETree representation if it is valid
    data is the xml data to validate and build a tree from
    schema is the schema to validate against
    returns 0 if the xml is invalid, and an ETree if it is
    """
    try:
        xsv.parseAndValidateXmlInputString(data, schema, xmlIfClass=xsv.XMLIF_ELEMENTTREE)
        return ET.parse(StringIO(data))
    except xsv.XsvalError as e:
        return 0

#http://stackoverflow.com/questions/7684333/converting-xml-to-dictionary-using-elementtree
def etree_to_dict(t):
    """recursively converts an ETree into a dict"""
    if t.getchildren() == []:
        d = {t.tag: t.text}
    else:
        d = {t.tag : map(etree_to_dict, t.getchildren())}
    return d


def store_special_classes(result_dict, assoc_obj):
    """ creates relational/child objects like videos, social, images, maps, etc from dict data
    """
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
    """ Handles the interaction between the client and the server for importing xml files into our datastore
    """
    SCHEMA  ='unicornSteroids.xsd' # the schema that all xml is validated against
    PASSWORD = 'hunter2' # the password required for upload and import functionality

    def post(self):
        self.response.out.write("<html><body>")
        password = self.request.get('pass')
        if password == 'hunter2':
            self.response.out.write('<h2>Access Granted</h2>')
            upload_request = self.request.get('uploaded_file') #upload request contains the raw data from the file

            if upload_request != '':
                # We only want to reach this section if the user actually attempted to upload a file

                tree = get_tree_and_validate(upload_request, open(self.SCHEMA, 'r').read())

                if tree == 0:
                    self.response.out.write('<p>The file you uploaded did not validate.<br />Please try again</p>')
                else:
                    self.response.out.write('<p>Your file has validated</p>')
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
        self.response.out.write("</body></html>")
    def get(self):
        # This section is reached when a user clicks on "Import" on the main page, but we want a post, not a get.
        self.post()


class ExportHandler(webapp2.RequestHandler):
    """ Renders the page for exporting objects from our datastore to XML
    """
    def get(self):
        self.response.headers['Content-Type'] = "text/xml; charset=utf-8"
        root = exporter.buildTree()
        logging.info("root: %s", root)
        output = ET.tostring(root)
        self.response.out.write(unicode(output,"UTF-8"))


app = webapp2.WSGIApplication([
#    ('/', MainHandler),
    ('/import', ImportHandler),
    ('/export', ExportHandler)
], debug=True)
