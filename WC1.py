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
import xml.etree.ElementTree as ET
from importer import importer
import logging
import exporter
from Models import Image, Video, Map, Social, ExternalLink, Citation

class ImportHandler(webapp2.RequestHandler):
    

    def post(self):
        self.response.out.write("<html><body>")
        password = self.request.get('pass')
        if password == 'hunter2':
            self.response.out.write('<h2>Access Granted</h2>')
            upload_request = self.request.get('uploaded_file') #upload request contains the raw data from the file
            if upload_request != '':
                # We only want to reach this section if the user actually attempted to upload a file
		importer(upload_request)
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
