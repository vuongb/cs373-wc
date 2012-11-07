from google.appengine.ext import db
import urllib
import json

# One to Many Relationships
class ExternalLink(db.Model):
    source = db.LinkProperty(required=True)
    description = db.StringProperty(required=True)
    assoc_object = db.ReferenceProperty(None, collection_name='external_links', required=True)

class Citation(db.Model):
    source = db.LinkProperty(required=True)
    description = db.StringProperty(required=True)
    assoc_object = db.ReferenceProperty(None, collection_name='citations', required=True)

class Map(db.Model):
    source = db.LinkProperty(required=True)
    description = db.StringProperty(required=True)
    assoc_object = db.ReferenceProperty(None, collection_name='maps', required=True)

class Image(db.Model):
    source = db.LinkProperty(required=True)
    description = db.StringProperty(required=True)
    assoc_object = db.ReferenceProperty(None, collection_name='images', required=True)

class Social(db.Model):
    social_id = db.StringProperty(required=True)
    social_type = db.StringProperty(choices=('facebook', 'twitter', 'youtube'), required=True)
    assoc_object = db.ReferenceProperty(None, collection_name='social', required=True)

    def get_twitter_feed(self):
        if self.social_type != 'twitter':
            return False
        elif self.social_id[0] == "@":
            url = "https://api.twitter.com/1/statuses/user_timeline.json?include_entities=false&include_rts=false&screen_name=%s&count=5" % self.social_id[1:]
        elif self.social_id[0] == "#":
            url = "http://search.twitter.com/search.json?q=%s&rpp=5&include_entities=false&result_type=mixed" % self.social_id[1:]
        else:
            return False
        return json.loads(urllib.urlopen(url).read())

class Video(db.Model):
    video_id = db.StringProperty(required=True)
    video_type = db.StringProperty(choices=('youtube', 'vimeo'), required=True)
    assoc_object = db.ReferenceProperty(None, collection_name='videos', required=True)

class Crisis(db.Model):
    #todo removed required properties for name, type, description, economicimpact, humanimpact, resourcesneeded, waystohelp
    # Base Data
    us_name            = db.StringProperty(required=True)
    us_alternateNames  = db.StringProperty()
    us_type            = db.StringProperty(required=True)
    us_description     = db.TextProperty(required=True)

    # Location
    us_city            = db.StringProperty()
    us_state           = db.StringProperty()
    us_country         = db.StringProperty()
    us_latitude        = db.StringProperty()
    us_longitude       = db.StringProperty()

    # Other Data
    us_startDate       = db.DateTimeProperty()
    us_endDate         = db.DateTimeProperty()
    us_economicImpact  = db.IntegerProperty(required=True)
    us_humanDeaths     = db.IntegerProperty()
    us_humanMissing    = db.IntegerProperty()
    us_humanInjured    = db.IntegerProperty()
    us_humanDisplaced  = db.IntegerProperty()

    us_resoucesNeeded  = db.StringListProperty(required=True)
    us_waysToHelp      = db.StringListProperty(required=True)

    def getUrl(self):
        return "/c/" + str(self.key().id())

    def getLocation(self):
        location = []
        if self.us_city :
          location.append(str(self.us_city))
        if self.us_state :
          location.append(str(self.us_state))
        location.append(str(self.us_country))
        return ", ".join(location)

class Organization(db.Model):
    # Base Data
    us_name            = db.StringProperty(required=True)
    us_alternateNames  = db.StringProperty()
    us_type            = db.StringProperty(required=True)
    us_description     = db.TextProperty(required=True)

    # Location
    us_city            = db.StringProperty()
    us_state           = db.StringProperty()
    us_country         = db.StringProperty()
    us_latitude        = db.StringProperty()
    us_longitude       = db.StringProperty()

    # Contact Info
    us_address         = db.TextProperty()
    us_email           = db.StringProperty()
    us_phone           = db.StringProperty()

    def getUrl(self):
        return "/o/" + str(self.key().id())

    def getLocation(self):
        location = []
        if self.us_city :
          location.append(str(self.us_city))
        if self.us_state :
          location.append(str(self.us_state))
        location.append(str(self.us_country))
        return ", ".join(location)

class Person(db.Model):
    # Base Data
    us_name            = db.StringProperty(required=True)
    us_alternateNames  = db.StringProperty()
    us_type            = db.StringProperty(required=True)
    us_description     = db.TextProperty(required=True)

    # Location
    us_city            = db.StringProperty()
    us_state           = db.StringProperty()
    us_country         = db.StringProperty()
    us_latitude        = db.StringProperty()
    us_longitude       = db.StringProperty()

    def getUrl(self):
        return "/p/" + str(self.key().id())

    def getLocation(self):
        location = []
        if self.us_city :
          location.append(str(self.us_city))
        if self.us_state :
          location.append(str(self.us_state))
        location.append(str(self.us_country))
        return ", ".join(location)

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