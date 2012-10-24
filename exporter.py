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
  ele.attrib['id'] = str(idNum)
  
  name = Element('name')
  name.text = crisis.us_name
  ele.append(name)

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

  # Location has nested groups. Cause problems?
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

  date = Element('startDate')
  date.text = str(crisis.us_startDate)
  ele.append(date)

  date = Element('endDate')
  date.text = str(crisis.us_endDate)
  ele.append(date)

  human_impact = Element('human-impact')
  for h_impact in crisis.us_humanImpact:
    stat = Element('statistic')
    stat.text = h_impact
    human_impact.append(stat)
  ele.append(human_impact)
  
  economic_impact = Element('economic-impact')
  for e_impact in crisis.us_economicImpact:
    econImpact_Ele = Element('statistic')
    econImpact_Ele.text = e_impact
    economic_impact.append(econImpact_Ele)
  ele.append(economic_impact)

  resources = Element('resources-needed')
  for resource in crisis.us_resoucesNeeded:
    resource_ele = Element('resource')
    resource_ele.text = resource
    resources.append(resource_ele)
  ele.append(resources)

  ways = Element('ways-to-help')
  for way in crisis.us_waysToHelp:
    way_ele = Element('way')
    way_ele.text = way
    ways.append(way_ele)
  ele.append(ways)

##  for image in crisis.images:
##    image_ele = Element('image')
##    link = Element('link')
##    link.text = image.link
##    image_ele.append(link)
##    if image.description:
##      des_ele = Element('description')
##      des_ele.text = image.description
##      image_ele.append(des_ele)
##    ele.append(image_ele)
##
##  for video in crisis.videos:
##    video_ele = Element('video')
##    video_ele.attrib['video-type'] = video.video_type
##    link = Element('link')
##    link.text = video.link
##    video_ele.append(link)
##    if video.title:
##      name_ele = Element('title')
##      name_ele.text = video.title
##      video_ele.append(name_ele)
##    if video.description:
##      des_ele = Element('description')
##      des_ele.text = video.description
##      video_ele.append(des_ele)
##    else:
##      video_ele.append(Element('description'))
##    ele.append(video_ele)
##
##  for social in crisis.social_networks:
##    social_ele = Element('social')
##    social_ele.attrib['social-type'] = social.social_type
##    link = Element('link')
##    link.text = social.link
##    social_ele.append(link)
##    if social.title:
##      name_ele = Element('title')
##      name_ele.text = social.title
##      social_ele.append(name_ele)
##    ele.append(social_ele)
##
##  for link in crisis.external_links:
##    link_ele = Element('external-link')
##    url = Element('link')
##    url.text = link.link
##    link_ele.append(url)
##    if link.title:
##      name_ele = Element('title')
##      name_ele.text = link.title
##      link_ele.append(name_ele)
##    ele.append(link_ele)
##
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
  ele.attrib['id'] = str(idNum)

  name = Element('name')
  name.text = organization.us_name
  ele.append(name)

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

  # Location has nested groups. Cause problems?
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

  # Text property cause problems?
  if organization.us_address or organization.us_email or organization.us_phone:
    contactInfo = Element('contact-info')
  
  if organization.us_address:
    address = Element('address')
    address.text = organization.us_address
    contactInfo.append(address)

  if organization.us_email:
    email = Element('email')
    email.text = organization.us_email
    contactInfo.append(email)

  if organization.us_phone:
    phone = Element('phone')
    phone.text = organization.us_phone
    contactInfo.append(phone)

  if contactInfo:
    ele.append(contactInfo)

##  for image in organization.images:
##    image_ele = Element('image')
##    link = Element('link')
##    link.text = image.link
##    image_ele.append(link)
##    if image.description:
##      des_ele = Element('description')
##      des_ele.text = image.description
##      image_ele.append(des_ele)
##    ele.append(image_ele)
##
##  for video in organization.videos:
##    video_ele = Element('video')
##    video_ele.attrib['video-type'] = video.video_type
##    link = Element('link')
##    link.text = video.link
##    video_ele.append(link)
##    if video.title:
##      name_ele = Element('title')
##      name_ele.text = video.title
##      video_ele.append(name_ele)
##    if video.description:
##      des_ele = Element('description')
##      des_ele.text = video.description
##      video_ele.append(des_ele)
##    ele.append(video_ele)
##
##  for social in organization.social_networks:
##    social_ele = Element('social')
##    social_ele.attrib['social-type'] = social.social_type
##    link = Element('link')
##    link.text = social.link
##    social_ele.append(link)
##    if social.title:
##      name_ele = Element('title')
##      name_ele.text = social.title
##      social_ele.append(name_ele)
##    ele.append(social_ele)
##
##  for link in organization.external_links:
##    link_ele = Element('external-link')
##    url = Element('link')
##    url.text = link.link
##    link_ele.append(url)
##    if link.title:
##      name_ele = Element('title')
##      name_ele.text = link.title
##      link_ele.append(name_ele)
##    ele.append(link_ele)
##
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
<<<<<<< HEAD
#  ele.attrib['id'] = person.key().name()
=======
  ele.attrib['id'] = str(idNum)
>>>>>>> Export works for all but strange objects

  name = Element('name')
  name.text = person.us_name
  ele.append(name)

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

  # Location has nested groups. Cause problems?
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

##  for image in person.images:
##    image_ele = Element('image')
##    link = Element('link')
##    link.text = image.link
##    image_ele.append(link)
##    if image.description:
##      des_ele = Element('description')
##      des_ele.text = image.description
##      image_ele.append(des_ele)
##    ele.append(image_ele)
##
##  for video in person.videos:
##    video_ele = Element('video')
##    video_ele.attrib['video-type'] = video.video_type
##    link = Element('link')
##    link.text = video.link
##    video_ele.append(link)
##    if video.title:
##      name_ele = Element('title')
##      name_ele.text = video.title
##      video_ele.append(name_ele)
##    if video.description:
##      des_ele = Element('description')
##      des_ele.text = video.description
##      video_ele.append(des_ele)
##    ele.append(video_ele)
##
##  for social in person.social_networks:
##    social_ele = Element('social')
##    social_ele.attrib['social-type'] = social.social_type
##    link = Element('link')
##    link.text = social.link
##    social_ele.append(link)
##    if social.title:
##      name_ele = Element('title')
##      name_ele.text = social.title
##      social_ele.append(name_ele)
##    ele.append(social_ele)
##
##  for link in person.external_links:
##    link_ele = Element('external-link')
##    url = Element('link')
##    url.text = link.link
##    link_ele.append(url)
##    if link.title:
##      name_ele = Element('title')
##      name_ele.text = link.title
##      link_ele.append(name_ele)
##    ele.append(link_ele)
##
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
