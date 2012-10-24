#dynamic html serving
#
#def application_key(application_name = None):
#    return db.Key.from_path('Crises Center', application_name or 'default_application')
#
#class MainHandler(webapp2.RequestHandler):
#    def get(self):
#        self.response.write(self.get_header())
#
#        ##todo: not too sure about how or if this works
#        ## see https://developers.google.com/appengine/docs/python/gettingstartedpython27/usingdatastore
#        self.application_name = self.request.get('application_name')
#
#        crises = self.get_crises()
#        organizations = self.get_organizations()
#        people = self.get_people()
#
#        body = "Crises\n" + self.to_ul(crises)\
#               + "\nOrganizations\n" + self.to_ul(organizations)\
#               + "\nPeople\n" + self.to_ul(people)
#
#        self.response.out.write(body)
#
#        self.response.write(self.get_footer())
#
#    def get_header(self):
#        return "<html><body>"
#
#    def get_footer(self):
#        return "</body></html>"
#
#    def get_crises(self):
#        return db.GqlQuery("SELECT * "
#                           "FROM Crisis "
#                           "WHERE ANCESTOR IS :1 "
#                           "ORDER BY us_name DESC",
#            application_key(self.application_name))
#
#    def get_organizations(self):
#        return db.GqlQuery("SELECT * "
#                           "FROM Organization "
#                           "WHERE ANCESTOR IS :1 "
#                           "ORDER BY us_name DESC",
#            application_key(self.application_name))
#
#    def get_people(self):
#        return db.GqlQuery("SELECT * "
#                           "FROM Person "
#                           "WHERE ANCESTOR IS :1 "
#                           "ORDER BY us_name DESC",
#            application_key(self.application_name))
#
#    def get_externalLink(self):
#        return db.GqlQuery("SELECT * "
#                           "FROM ExternalLink "
#                           "WHERE ANCESTOR IS :1 "
#                           "ORDER BY description DESC",
#            application_key(self.application_name))
#
#    def get_citation(self):
#        return db.GqlQuery("SELECT * "
#                           "FROM Citation "
#                           "WHERE ANCESTOR IS :1 "
#                           "ORDER BY description DESC",
#            application_key(self.application_name))
#
#    def get_map(self):
#        return db.GqlQuery("SELECT * "
#                           "FROM Map "
#                           "WHERE ANCESTOR IS :1 "
#                           "ORDER BY description DESC",
#            application_key(self.application_name))
#
#    def get_image(self):
#        return db.GqlQuery("SELECT * "
#                           "FROM Image "
#                           "WHERE ANCESTOR IS :1 "
#                           "ORDER BY description DESC",
#            application_key(self.application_name))
#
#    def get_social(self):
#        return db.GqlQuery("SELECT * "
#                           "FROM Social "
#                           "WHERE ANCESTOR IS :1 "
#                           "ORDER BY social_id DESC",
#            application_key(self.application_name))
#
#    def get_video(self):
#        return db.GqlQuery("SELECT * "
#                           "FROM Video "
#                           "WHERE ANCESTOR IS :1 "
#                           "ORDER BY video_id DESC",
#            application_key(self.application_name))
#
#
#
#    def to_ul(self, col):
#        return "<ul>" + "\n".join(["<li>" + str(item) + "</li>" for item in col]) + "</ul>"