from xml.etree.ElementTree import Element
from Models import *
from google.appengine.ext import db

def mergeSubObjects(la, lb):
  coll = []
  seen = set()

  for i in lb:
    if i.tag in ('image','video','social','external-link'):
      coll.append(i)
      seen.add((i.tag, i.find('link').text.strip()))
    elif i.tag in ('resource','way-to-help'):
      coll.append(i)
      seen.add((i.tag, i.text.strip()))
    else:
      coll.append(i)
      seen.add(i.tag)

  for i in la:
    if i.tag in ('image','video','social','external-link'):
      if (i.tag, i.find('link').text.strip()) not in seen:
        coll.append(i)
    elif i.tag in ('resource','way-to-help'):
      if (i.tag, i.text.strip()) not in seen:
        coll.append(i)
    else:
      if i.tag not in seen:
        coll.append(i)
  return coll

def mergeObjects(a, b):
  coll = []
  seen = set()
  for i in a:
    found = False
    for j in b:
      if i.attrib['id'] == j.attrib['id']:
        found = True
        seen.add(i.attrib['id'])
        sub = mergeSubObjects(list(i), list(j))
        for o in [x for x in i]:
          i.remove(o)
        for o in sub:
          i.append(o)
        coll.append(i)
    if not found:
      coll.append(i)
  for i in b:
    if i.attrib['id'] not in seen:
      coll.append(i)
  return coll

def merge(tree, other):
  '''
  constructs merged tree
  arguments are trees to merge
  returns the merged tree
  '''
  root = Element('world-crises')
  crises = Element('crises')
  orgs = Element('organizations')
  people = Element('people')
  for i in mergeObjects(tree.find('crises').findall('crisis'), other.find('crises').findall('crisis')):
    crises.append(i)
  for i in mergeObjects(tree.find('organizations').findall('organization'), other.find('organizations').findall('organization')):
    orgs.append(i)
  for i in mergeObjects(tree.find('people').findall('person'), other.find('people').findall('person')):
    people.append(i)

  root.append(crises)
  root.append(orgs)
  root.append(people)

  return root

def buildTree():
  """
  builds the tree of all objects in the datastore conforming to WC1.xsd
  return root element which is the root of the tree or '<world-crises>'
  """
  root = Element('world-crises')

  crises = Element('crises')
  crises_objects = db.GqlQuery("SELECT * FROM Crisis")
  
  for crisis_object in crises_objects:
    crisis = addCrisis(crisis_object)
    crises.append(crisis)
  root.append(crises)

  organizations = Element('organizations')
  organizations_objects = db.GqlQuery("SELECT * FROM Organization")
  for organization_object in organizations_objects:
    organization = addOrganization(organization_object)
    organizations.append(organization)
  root.append(organizations)

  people = Element('people')
  people_objects = db.GqlQuery("SELECT * FROM Person")
  for person_object in people_objects:
    person = addPerson(person_object)
    people.append(person)
  root.append(people)

  return root

def addCrisis(crisis):
  """
    build xml crisis element based on WC1.xsd (hard coded, meaning changes to xsd will not reflect here)
    crisis is a Crisis object from the GAE datastore
    return crisis xml element
    """
  ele = Element('crisis')
  ele.attrib['id'] = crisis.key().name()

  name = Element('name')
  name.text = crisis.name
  ele.append(name)

  kind = Element('kind')
  kind.text = crisis.kind_
  ele.append(kind)

  if crisis.description:
    description = Element('description')
    description.text = crisis.description
    ele.append(description)

  if crisis.city:
    city = Element('city')
    city.text = crisis.city
    ele.append(city)

  if crisis.state:
    state = Element('state')
    state.text = crisis.state
    ele.append(state)

  country = Element('country')
  country.text = crisis.country
  ele.append(country)

  date = Element('date')
  date.text = str(crisis.date)
  ele.append(date)

  human_impact = Element('human-impact')
  if crisis.deaths:
    deaths = Element('deaths')
    deaths.text = str(crisis.deaths)
    human_impact.append(deaths)
  if crisis.missing:
    missing = Element('missing')
    missing.text = str(crisis.missing)
    human_impact.append(missing)
  if crisis.injured:
    injured = Element('injured')
    injured.text = str(crisis.injured)
    human_impact.append(injured)
  if crisis.displaced:
    displaced = Element('displaced')
    displaced.text = str(crisis.displaced)
    human_impact.append(displaced)
  ele.append(human_impact)

  economic_impact = Element('economic-impact')
  economic_impact.text = str(crisis.economic_impact)
  ele.append(economic_impact)

  for resource in crisis.resources:
    resource_ele = Element('resource')
    resource_ele.text = resource
    ele.append(resource_ele)

  for way in crisis.ways_to_help:
    way_ele = Element('way-to-help')
    way_ele.text = way
    ele.append(way_ele)

  for image in crisis.images:
    image_ele = Element('image')
    link = Element('link')
    link.text = image.link
    image_ele.append(link)
    if image.description:
      des_ele = Element('description')
      des_ele.text = image.description
      image_ele.append(des_ele)
    ele.append(image_ele)

  for video in crisis.videos:
    video_ele = Element('video')
    video_ele.attrib['video-type'] = video.video_type
    link = Element('link')
    link.text = video.link
    video_ele.append(link)
    if video.title:
      name_ele = Element('title')
      name_ele.text = video.title
      video_ele.append(name_ele)
    if video.description:
      des_ele = Element('description')
      des_ele.text = video.description
      video_ele.append(des_ele)
    else:
      video_ele.append(Element('description'))
    ele.append(video_ele)

  for social in crisis.social_networks:
    social_ele = Element('social')
    social_ele.attrib['social-type'] = social.social_type
    link = Element('link')
    link.text = social.link
    social_ele.append(link)
    if social.title:
      name_ele = Element('title')
      name_ele.text = social.title
      social_ele.append(name_ele)
    ele.append(social_ele)

  for link in crisis.external_links:
    link_ele = Element('external-link')
    url = Element('link')
    url.text = link.link
    link_ele.append(url)
    if link.title:
      name_ele = Element('title')
      name_ele.text = link.title
      link_ele.append(name_ele)
    ele.append(link_ele)

  org_refs = []
  for org in crisis.organizations:
    org_refs.append(org.organization.key().name())
  org_refs_ele = Element('organization-refs')
  org_refs_ele.text = " ".join(org_refs)
  ele.append(org_refs_ele)

  p_refs = []
  for p in crisis.people:
    p_refs.append(p.person.key().name())
  p_refs_ele = Element('person-refs')
  p_refs_ele.text = " ".join(p_refs)
  ele.append(p_refs_ele)

  return ele

def addOrganization(organization):
  """
    build xml organization element based on WC1.xsd (hard coded, meaning changes to xsd will not reflect here)
    organization is an Organization object from the GAE datastore
    return organization xml element
    """
  ele = Element('organization')
  ele.attrib['id'] = organization.key().name()

  name = Element('name')
  name.text = organization.name
  ele.append(name)

  kind = Element('kind')
  kind.text = organization.kind_
  ele.append(kind)

  if organization.description:
    description = Element('description')
    description.text = organization.description
    ele.append(description)

  if organization.city:
    city = Element('city')
    city.text = organization.city
    ele.append(city)

  if organization.state:
    state = Element('state')
    state.text = organization.state
    ele.append(state)

  country = Element('country')
  country.text = organization.country
  ele.append(country)

  if organization.history:
    history = Element('history')
    history.text = organization.history
    ele.append(history)

  if organization.address:
    address = Element('address')
    address.text = organization.address
    ele.append(address)

  if organization.email:
    email = Element('email')
    email.text = organization.email
    ele.append(email)

  if organization.phone:
    phone = Element('phone')
    phone.text = organization.phone
    ele.append(phone)

  for image in organization.images:
    image_ele = Element('image')
    link = Element('link')
    link.text = image.link
    image_ele.append(link)
    if image.description:
      des_ele = Element('description')
      des_ele.text = image.description
      image_ele.append(des_ele)
    ele.append(image_ele)

  for video in organization.videos:
    video_ele = Element('video')
    video_ele.attrib['video-type'] = video.video_type
    link = Element('link')
    link.text = video.link
    video_ele.append(link)
    if video.title:
      name_ele = Element('title')
      name_ele.text = video.title
      video_ele.append(name_ele)
    if video.description:
      des_ele = Element('description')
      des_ele.text = video.description
      video_ele.append(des_ele)
    ele.append(video_ele)

  for social in organization.social_networks:
    social_ele = Element('social')
    social_ele.attrib['social-type'] = social.social_type
    link = Element('link')
    link.text = social.link
    social_ele.append(link)
    if social.title:
      name_ele = Element('title')
      name_ele.text = social.title
      social_ele.append(name_ele)
    ele.append(social_ele)

  for link in organization.external_links:
    link_ele = Element('external-link')
    url = Element('link')
    url.text = link.link
    link_ele.append(url)
    if link.title:
      name_ele = Element('title')
      name_ele.text = link.title
      link_ele.append(name_ele)
    ele.append(link_ele)

  c_refs = []
  for c in organization.crises:
    c_refs.append(c.crisis.key().name())
  c_refs_ele = Element('crisis-refs')
  c_refs_ele.text = " ".join(c_refs)
  ele.append(c_refs_ele)

  p_refs = []
  for p in organization.people:
    p_refs.append(p.person.key().name())
  p_refs_ele = Element('person-refs')
  p_refs_ele.text = " ".join(p_refs)
  ele.append(p_refs_ele)

  return ele
  
def addPerson(person):
  """
    build xml person element based on WC1.xsd (hard coded, meaning changes to xsd will not reflect here)
    person is a Person object from the GAE datastore
    return person xml element
    """
  ele = Element('person')
  ele.attrib['id'] = person.key().name()

  name = Element('name')
  name.text = person.name
  ele.append(name)

  kind = Element('kind')
  kind.text = person.kind_
  ele.append(kind)

  if person.description:
    description = Element('description')
    description.text = person.description
    ele.append(description)

  if person.city:
    city = Element('city')
    city.text = person.city
    ele.append(city)

  if person.state:
    state = Element('state')
    state.text = person.state
    ele.append(state)

  country = Element('country')
  country.text = person.country
  ele.append(country)

  for image in person.images:
    image_ele = Element('image')
    link = Element('link')
    link.text = image.link
    image_ele.append(link)
    if image.description:
      des_ele = Element('description')
      des_ele.text = image.description
      image_ele.append(des_ele)
    ele.append(image_ele)

  for video in person.videos:
    video_ele = Element('video')
    video_ele.attrib['video-type'] = video.video_type
    link = Element('link')
    link.text = video.link
    video_ele.append(link)
    if video.title:
      name_ele = Element('title')
      name_ele.text = video.title
      video_ele.append(name_ele)
    if video.description:
      des_ele = Element('description')
      des_ele.text = video.description
      video_ele.append(des_ele)
    ele.append(video_ele)

  for social in person.social_networks:
    social_ele = Element('social')
    social_ele.attrib['social-type'] = social.social_type
    link = Element('link')
    link.text = social.link
    social_ele.append(link)
    if social.title:
      name_ele = Element('title')
      name_ele.text = social.title
      social_ele.append(name_ele)
    ele.append(social_ele)

  for link in person.external_links:
    link_ele = Element('external-link')
    url = Element('link')
    url.text = link.link
    link_ele.append(url)
    if link.title:
      name_ele = Element('title')
      name_ele.text = link.title
      link_ele.append(name_ele)
    ele.append(link_ele)

  c_refs = []
  for c in person.crises:
    c_refs.append(c.crisis.key().name())
  c_refs_ele = Element('crisis-refs')
  c_refs_ele.text = " ".join(c_refs)
  ele.append(c_refs_ele)

  org_refs = []
  for org in person.organizations:
    org_refs.append(org.organization.key().name())
  org_refs_ele = Element('organization-refs')
  org_refs_ele.text = " ".join(org_refs)
  ele.append(org_refs_ele)

  return ele
