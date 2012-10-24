from google.appengine.ext import db

# One to Many Relationships
class ExternalLink(db.Model):
    source = db.LinkProperty(required=True)
    description = db.LinkProperty(required=True)
    assoc_object = db.ReferenceProperty(None, collection_name='external_links', required=True)

class Citation(db.Model):
    source = db.LinkProperty(required=True)
    description = db.LinkProperty(required=True)
    assoc_object = db.ReferenceProperty(None, collection_name='citations', required=True)

class Map(db.Model):
    source = db.LinkProperty(required=True)
    description = db.LinkProperty(required=True)
    assoc_object = db.ReferenceProperty(None, collection_name='maps', required=True)

class Image(db.Model):
    source = db.LinkProperty(required=True)
    description = db.LinkProperty(required=True)
    assoc_object = db.ReferenceProperty(None, collection_name='images', required=True)

class Social(db.Model):
    social_id = db.StringProperty(required=True)
    social_type = db.StringProperty(choices=('facebook', 'twitter', 'youtube'), required=True)
    assoc_object = db.ReferenceProperty(None, collection_name='social', required=True)

class Video(db.Model):
    social_id = db.StringProperty(required=True)
    social_type = db.StringProperty(choices=('youtube', 'vimeo'), required=True)
    assoc_object = db.ReferenceProperty(None, collection_name='videos', required=True)

class Organization(db.Model):
    # Base Data
    us_name            = db.StringProperty(required=True)
    us_alternateNames  = db.StringListProperty()
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

class Person(db.Model):
    # Base Data
    us_name            = db.StringProperty(required=True)
    us_alternateNames  = db.StringListProperty()
    us_type            = db.StringProperty(required=True)
    us_description     = db.TextProperty(required=True)

    # Location
    us_city            = db.StringProperty()
    us_state           = db.StringProperty()
    us_country         = db.StringProperty()
    us_latitude        = db.StringProperty()
    us_longitude       = db.StringProperty()

class Crisis(db.Model):
    #todo removed required properties for name, type, description, economicimpact, humanimpact, resourcesneeded, waystohelp
    # Base Data
    us_name            = db.StringProperty(required=True)
    us_alternateNames  = db.StringListProperty()
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
    us_economicImpact  = db.StringListProperty(required=True)
    us_humanImpact     = db.StringListProperty(required=True)
    us_resoucesNeeded  = db.StringListProperty(required=True)
    us_waysToHelp      = db.StringListProperty(required=True)


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