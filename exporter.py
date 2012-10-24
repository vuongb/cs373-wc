from xml.etree.ElementTree import Element
from Models import *
from google.appengine.ext import db

def buildTree():
  """
  builds the tree of all objects in the datastore conforming to WC1.xsd
  return root element which is the root of the tree or '<world-crises>'
  """
  root = Element('world-crises')

  crises = Element('crises')
  crises_objects = db.GqlQuery("SELECT * FROM Crisis")

  idNum = 1
  # Build XML for crises
  for crisis_object in crises_objects:
    crisis = addCrisis(crisis_object, idNum)
    idNum += 1
    crises.append(crisis)
  root.append(crises)

  # Build XML for Organizations
  organizations = Element('organizations')
  organizations_objects = db.GqlQuery("SELECT * FROM Organization")
  for organization_object in organizations_objects:
    organization = addOrganization(organization_object, idNum)
    idNum += 1
    organizations.append(organization)
  root.append(organizations)

  # Build XML for people
  people = Element('people')
  people_objects = db.GqlQuery("SELECT * FROM Person")
  for person_object in people_objects:
    person = addPerson(person_object, idNum)
    idNum += 1
    people.append(person)
  root.append(people)

  return root

def addCrisis(crisis, idNum):
  """
    build xml crisis element based on WC1.xsd (hard coded, meaning changes to xsd will not reflect here)
    crisis is a Crisis object from the GAE datastore
    return crisis xml element
    """

  ele = Element('crisis')
  ele.attrib['id'] = 'c' + str(idNum)
  
  name = Element('name')
  name.text = crisis.us_name
  ele.append(name)

  # Alternate Names is stored as a list in datastore
  # Export as: <alternate-names><alternate-name>.....</alternate-name></alternate-names>
  if crisis.us_alternateNames:
    altName = Element('alternate-names')
    for name in crisis.us_alternateNames:
      altName_Ele = Element('alternate-name')
      altName_Ele.text = name
      altName.append(altName_Ele)
    ele.append(altName)

  kind = Element('kind')
  kind.text = crisis.us_type
  ele.append(kind)

  description = Element('description')
  description.text = crisis.us_description
  ele.append(description)

  # Location has nested XML groups: city, state, country, latitude, longitude
  # Export as: <location><>.....</></location>
  location = Element('location')
  if crisis.us_city:
    city = Element('city')
    city.text = crisis.us_city
    location.append(city)

  if crisis.us_state:
    state = Element('state')
    state.text = crisis.us_state
    location.append(state)

  country = Element('country')
  country.text = crisis.us_country
  location.append(country)

  if crisis.us_latitude:
    latitude = Element('latitude')
    latitude.text = crisis.us_latitude
    location.append(latitude)

  if crisis.us_longitude:
    longitude = Element('longitude')
    longitude.text = crisis.us_longitude
    location.append(longitude)
    
  ele.append(location)

  # Images is another entity in GAE
  # Export as: <images><image><source>...</source><description>...</description></image></images>
  image_main = Element('images')
  for image in crisis.images:
    image_ele = Element('image')
    link = Element('source')
    link.text = image.source
    image_ele.append(link)
    if image.description:
      des_ele = Element('description')
      des_ele.text = image.description
      image_ele.append(des_ele)
    image_main.append(image_ele)
  ele.append(image_main)

  # Maps is another entity in GAE
  # Export as: <maps><map><source>...</source><description>...</description></map></maps>
  maps_main = Element('maps')
  for map in crisis.maps:
    map_ele = Element('map')
    link = Element('source')
    link.text = map.source
    map_ele.append(link)
    if map.description:
      des_ele = Element('description')
      des_ele.text = map.description
      map_ele.append(des_ele)
    maps_main.append(map_ele)
  ele.append(maps_main)

  # Video is another entity in GAE
  # Export as: <videos><..>..</..></videos>
  video_main = Element('videos')
  for video in crisis.videos:
    video_ele = Element(video.video_type)
    video_ele.text = video.video_id
    video_main.append(video_ele)
  ele.append(video_main)

  # Social is another entity in GAE
  # Export as: <social><..>..</..></social>
  social_main = Element('social')
  for social in crisis.social:
    social_ele = Element(social.social_type)
    social_ele.text = social.social_id
    social_main.append(social_ele)
  ele.append(social_main)

  # Citations is another entity in GAE
  # Export as: <citations><citation><source>...</source><description>...</description></citation></citations>
  citations_main = Element('citations')
  for citation in crisis.maps:
    citation_ele = Element('citation')
    link = Element('source')
    link.text = citation.source
    citation_ele.append(link)
    if citation.description:
      des_ele = Element('description')
      des_ele.text = citation.description
      citation_ele.append(des_ele)
    citations_main.append(citation_ele)
  ele.append(citations_main)

  # External-Links is another entity in GAE
  # Export as: <external-links><external-link><source>...</source><description>...</description></external-link></external-links>
  extLink_main = Element('external-links')
  for link in crisis.external_links:
    link_ele = Element('external-link')
    source_Elem = Element('source')
    source_Elem.text = link.source
    link_ele.append(source_Elem)
    descrip_Elem = Element('description')
    descrip_Elem.text = link.description
    link_ele.append(descrip_Elem)
    extLink_main.append(link_ele)
  ele.append(extLink_main)

  date = Element('start-date')
  tempDate = str(crisis.us_startDate)
  date.text = tempDate.replace(' ', 'T')
  ele.append(date)

  date = Element('end-date')
  tempDate = str(crisis.us_startDate)
  date.text = tempDate.replace(' ', 'T')
  ele.append(date)

  # human impact is stored as a list in GAE
  # Export as: <human-impact><statistic>...</statistic></human-impact>
  human_impact = Element('human-impact')
  for h_impact in crisis.us_humanImpact:
    stat = Element('statistic')
    stat.text = h_impact
    human_impact.append(stat)
  ele.append(human_impact)

  # economic impact is stored as a list in GAE
  # Export as: <economic-impact><statistic>...</statistic></economic-impact>
  economic_impact = Element('economic-impact')
  for e_impact in crisis.us_economicImpact:
    econImpact_Ele = Element('statistic')
    econImpact_Ele.text = e_impact
    economic_impact.append(econImpact_Ele)
  ele.append(economic_impact)

  # resources needed is stored as a list in GAE
  # Export as: <resources-needed><resource>...</resource></resources-needed>
  resources = Element('resources-needed')
  for resource in crisis.us_resoucesNeeded:
    resource_ele = Element('resource')
    resource_ele.text = resource
    resources.append(resource_ele)
  ele.append(resources)


  # ways to help is stored as a list in GAE
  # Export as: <ways-to-help><way>...</way></ways-to-help>
  ways = Element('ways-to-help')
  for way in crisis.us_waysToHelp:
    way_ele = Element('way')
    way_ele.text = way
    ways.append(way_ele)
  ele.append(ways)

##  org_refs = []
##  for org in crisis.organizations:
##    org_refs.append(org.organization.key().name())
##  org_refs_ele = Element('organization-refs')
##  org_refs_ele.text = " ".join(org_refs)
##  ele.append(org_refs_ele)
##
##  p_refs = []
##  for p in crisis.people:
##    p_refs.append(p.person.key().name())
##  p_refs_ele = Element('person-refs')
##  p_refs_ele.text = " ".join(p_refs)
##  ele.append(p_refs_ele)

  return ele

def addOrganization(organization, idNum):

  """
    build xml organization element based on WC1.xsd (hard coded, meaning changes to xsd will not reflect here)
    organization is an Organization object from the GAE datastore
    return organization xml element
    """
  
  ele = Element('organization')
  #ele.attrib['id'] = organization.us_name
  ele.attrib['id'] = 'o' + str(idNum)

  name = Element('name')
  name.text = organization.us_name
  ele.append(name)

  # Alternate Names is stored as a list in datastore
  # Export as: <alternate-names><alternate-name>.....</alternate-name></alternate-names>
  if organization.us_alternateNames:
    altName = Element('alternate-names')
    for name in organization.us_alternateNames:
      altName_Ele = Element('alternate-name')
      altName_Ele.text = name
      altName.append(altName_Ele)
    ele.append(altName)

  kind = Element('kind')
  kind.text = organization.us_type
  ele.append(kind)

  description = Element('description')
  description.text = organization.us_description
  ele.append(description)

  # Location has nested XML groups: city, state, country, latitude, longitude
  # Export as: <location><>.....</></location>
  location = Element('location')
  if organization.us_city:
    city = Element('city')
    city.text = organization.us_city
    location.append(city)

  if organization.us_state:
    state = Element('state')
    state.text = organization.us_state
    location.append(state)

  country = Element('country')
  country.text = organization.us_country
  location.append(country)

  if organization.us_latitude:
    latitude = Element('latitude')
    latitude.text = organization.us_latitude
    location.append(latitude)

  if organization.us_longitude:
    longitude = Element('longitude')
    longitude.text = organization.us_longitude
    location.append(longitude)
    
  ele.append(location)

  # Images is another entity in GAE
  # Export as: <images><image><source>...</source><description>...</description></image></images>    
  image_main = Element('images')
  for image in organization.images:
    image_ele = Element('image')
    link = Element('source')
    link.text = image.source
    image_ele.append(link)
    if image.description:
      des_ele = Element('description')
      des_ele.text = image.description
      image_ele.append(des_ele)
    image_main.append(image_ele)
  ele.append(image_main)

  # Maps is another entity in GAE
  # Export as: <maps><map><source>...</source><description>...</description></map></maps>
  maps_main = Element('maps')
  for map in organization.maps:
    map_ele = Element('map')
    link = Element('source')
    link.text = map.source
    map_ele.append(link)
    if map.description:
      des_ele = Element('description')
      des_ele.text = map.description
      map_ele.append(des_ele)
    maps_main.append(map_ele)
  ele.append(maps_main)

  # Video is another entity in GAE
  # Export as: <videos><..>..</..></videos>
  video_main = Element('videos')
  for video in organization.videos:
    video_ele = Element(video.video_type)
    video_ele.text = video.video_id
    video_main.append(video_ele)
  ele.append(video_main)

  # Social is another entity in GAE
  # Export as: <social><..>..</..></social>
  social_main = Element('social')
  for social in organization.social:
    social_ele = Element(social.social_type)
    social_ele.text = social.social_id
    social_main.append(social_ele)
  ele.append(social_main)

  # Citations is another entity in GAE
  # Export as: <citations><citation><source>...</source><description>...</description></citation></citations>
  citations_main = Element('citations')
  for citation in organization.maps:
    citation_ele = Element('citation')
    link = Element('source')
    link.text = citation.source
    citation_ele.append(link)
    if citation.description:
      des_ele = Element('description')
      des_ele.text = citation.description
      citation_ele.append(des_ele)
    citations_main.append(citation_ele)
  ele.append(citations_main)
  
  # External-Links is another entity in GAE
  # Export as: <external-links><external-link><source>...</source><description>...</description></external-link></external-links>
  extLink_main = Element('external-links')
  for link in organization.external_links:
    link_ele = Element('external-link')
    source_Elem = Element('source')
    source_Elem.text = link.source
    link_ele.append(source_Elem)
    descrip_Elem = Element('description')
    descrip_Elem.text = link.description
    link_ele.append(descrip_Elem)
    extLink_main.append(link_ele)
  ele.append(extLink_main)

  if organization.us_address:
    address = Element('address')
    address.text = organization.us_address
    ele.append(address)

  if organization.us_email:
    email = Element('email')
    email.text = organization.us_email
    ele.append(email)

  if organization.us_phone:
    phone = Element('phone')
    phone.text = organization.us_phone
    ele.append(phone)

##  c_refs = []
##  for c in organization.crises:
##    c_refs.append(c.crisis.key().name())
##  c_refs_ele = Element('crisis-refs')
##  c_refs_ele.text = " ".join(c_refs)
##  ele.append(c_refs_ele)
##
##  p_refs = []
##  for p in organization.people:
##    p_refs.append(p.person.key().name())
##  p_refs_ele = Element('person-refs')
##  p_refs_ele.text = " ".join(p_refs)
##  ele.append(p_refs_ele)

  return ele
  
def addPerson(person, idNum):
  """
    build xml person element based on WC1.xsd (hard coded, meaning changes to xsd will not reflect here)
    person is a Person object from the GAE datastore
    return person xml element
    """
  
  ele = Element('person')
#  ele.attrib['id'] = person.key().name()
  ele.attrib['id'] = 'p' + str(idNum)

  name = Element('name')
  name.text = person.us_name
  ele.append(name)

  # Alternate Names is stored as a list in datastore
  # Export as: <alternate-names><alternate-name>.....</alternate-name></alternate-names>
  if person.us_alternateNames:
    altName = Element('alternate-names')
    for name in person.us_alternateNames:
      altName_Ele = Element('alternate-name')
      altName_Ele.text = name
      altName.append(altName_Ele)
    ele.append(altName)

  kind = Element('kind')
  kind.text = person.us_type
  ele.append(kind)

  description = Element('description')
  description.text = person.us_description
  ele.append(description)

  # Location has nested XML groups: city, state, country, latitude, longitude
  # Export as: <location><>.....</></location>
  location = Element('location')
  if person.us_city:
    city = Element('city')
    city.text = person.us_city
    location.append(city)

  if person.us_state:
    state = Element('state')
    state.text = person.us_state
    location.append(state)

  country = Element('country')
  country.text = person.us_country
  location.append(country)

  if person.us_latitude:
    latitude = Element('latitude')
    latitude.text = person.us_latitude
    location.append(latitude)

  if person.us_longitude:
    longitude = Element('longitude')
    longitude.text = person.us_longitude
    location.append(longitude)
    
  ele.append(location)

  # Images is another entity in GAE
  # Export as: <images><image><source>...</source><description>...</description></image></images>
  image_main = Element('images')
  for image in person.images:
    image_ele = Element('image')
    link = Element('source')
    link.text = image.source
    image_ele.append(link)
    if image.description:
      des_ele = Element('description')
      des_ele.text = image.description
      image_ele.append(des_ele)
    image_main.append(image_ele)
  ele.append(image_main)

  # Maps is another entity in GAE
  # Export as: <maps><map><source>...</source><description>...</description></map></maps>
  maps_main = Element('maps')
  for map in person.maps:
    map_ele = Element('map')
    link = Element('source')
    link.text = map.source
    map_ele.append(link)
    if map.description:
      des_ele = Element('description')
      des_ele.text = map.description
      map_ele.append(des_ele)
    maps_main.append(map_ele)
  ele.append(maps_main)

  # Video is another entity in GAE
  # Export as: <videos><..>..</..></videos>
  video_main = Element('videos')
  for video in person.videos:
    video_ele = Element(video.video_type)
    video_ele.text = video.video_id
    video_main.append(video_ele)
  ele.append(video_main)

  # Social is another entity in GAE
  # Export as: <social><..>..</..></social>
  social_main = Element('social')
  for social in person.social:
    social_ele = Element(social.social_type)
    social_ele.text = social.social_id
    social_main.append(social_ele)
  ele.append(social_main)

  # Citations is another entity in GAE
  # Export as: <citations><citation><source>...</source><description>...</description></citation></citations>
  citations_main = Element('citations')
  for citation in person.maps:
    citation_ele = Element('citation')
    link = Element('source')
    link.text = citation.source
    citation_ele.append(link)
    if citation.description:
      des_ele = Element('description')
      des_ele.text = citation.description
      citation_ele.append(des_ele)
    citations_main.append(citation_ele)
  ele.append(citations_main)

  # External-Links is another entity in GAE
  # Export as: <external-links><external-link><source>...</source><description>...</description></external-link></external-links>
  extLink_main = Element('external-links')
  for link in person.external_links:
    link_ele = Element('external-link')
    source_Elem = Element('source')
    source_Elem.text = link.source
    link_ele.append(source_Elem)
    descrip_Elem = Element('description')
    descrip_Elem.text = link.description
    link_ele.append(descrip_Elem)
    extLink_main.append(link_ele)
  ele.append(extLink_main)

##  c_refs = []
##  for c in person.crises:
##    c_refs.append(c.crisis.key().name())
##  c_refs_ele = Element('crisis-refs')
##  c_refs_ele.text = " ".join(c_refs)
##  ele.append(c_refs_ele)
##
##  org_refs = []
##  for org in person.organizations:
##    org_refs.append(org.organization.key().name())
##  org_refs_ele = Element('organization-refs')
##  org_refs_ele.text = " ".join(org_refs)
##  ele.append(org_refs_ele)

  return ele
