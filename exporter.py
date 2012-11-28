from xml.etree.ElementTree import Element
from google.appengine.ext import db

def buildTree():
  """
  builds the tree of all objects in the datastore conforming to WC2.xsd
  return root element which is the root of the tree or '<world-crises>'
  """
  root = Element('world-crises')

  crises = Element('crises')
  crises_objects = db.GqlQuery("SELECT * FROM Crisis")

  # Build XML for crises
  for crisis_object in crises_objects:
    crisis = addCrisis(crisis_object)
    crises.append(crisis)
  root.append(crises)

  # Build XML for Organizations
  organizations = Element('organizations')
  organizations_objects = db.GqlQuery("SELECT * FROM Organization")
  for organization_object in organizations_objects:
    organization = addOrganization(organization_object)
    organizations.append(organization)
  root.append(organizations)

  # Build XML for people
  people = Element('people')
  people_objects = db.GqlQuery("SELECT * FROM Person")
  for person_object in people_objects:
    person = addPerson(person_object)
    people.append(person)
  root.append(people)

  return root

def addCrisis(crisis):
  """
    build xml crisis element based on WC2.xsd (hard coded, meaning changes to xsd will not reflect here)
    crisis is a Crisis object from the GAE datastore
    return crisis xml element
    """

  ele = Element('crisis')
  ele.attrib['id'] = str(crisis.us_id)
  
  name = Element('name')
  assert type(crisis.us_name) == str or type(crisis.us_name) == unicode
  name.text = crisis.us_name
  ele.append(name)

  # Alternate Names is stored as a list in datastore
  # Export as: <alternate-names>...</alternate-names>
  if crisis.us_alternateNames:
    assert type(crisis.us_alternateNames) == str or type(crisis.us_alternateNames) == unicode
    altName = Element('alternate-names')
    altName.text = crisis.us_alternateNames
    ele.append(altName)

  kind = Element('kind')
  assert type(crisis.us_type) == str or type(crisis.us_type) == unicode
  kind.text = crisis.us_type
  ele.append(kind)

  description = Element('description')
  description.text = crisis.us_description
  ele.append(description)

  # Location has nested XML groups: city, state, country, latitude, longitude
  # Export as: <location><>.....</></location>
  location = Element('location')
  if crisis.us_city:
    assert type(crisis.us_city) == str or type(crisis.us_city) == unicode
    city = Element('city')
    city.text = crisis.us_city
    location.append(city)

  if crisis.us_state:
    assert type(crisis.us_state) == str or type(crisis.us_state) == unicode
    state = Element('state')
    state.text = crisis.us_state
    location.append(state)

  assert type(crisis.us_country) == str or type(crisis.us_country) == unicode
  country = Element('country')
  country.text = crisis.us_country
  location.append(country)

  if crisis.us_latitude:
    assert type(crisis.us_latitude) == str or type(crisis.us_latitude) == unicode
    latitude = Element('latitude')
    latitude.text = crisis.us_latitude
    location.append(latitude)

  if crisis.us_longitude:
    assert type(crisis.us_longitude) == str or type(crisis.us_longitude) == unicode
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
      assert type(image.description) == str or type(image.description) == unicode
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
      assert type(map.description) == str or type(map.description) == unicode
      des_ele = Element('description')
      des_ele.text = map.description
      map_ele.append(des_ele)
    maps_main.append(map_ele)
  ele.append(maps_main)

  # Video is another entity in GAE
  # Export as: <videos><..>..</..></videos>
  video_main = Element('videos')
  for video in crisis.videos:
    assert type(video.video_type) == str or type(video.video_type) == unicode
    assert type(video.video_id) == str or type(video.video_id) == unicode
    video_ele = Element(video.video_type)
    video_ele.text = video.video_id
    video_main.append(video_ele)
  ele.append(video_main)

  # Social is another entity in GAE
  # Export as: <social><..>..</..></social>
  social_main = Element('social')
  for social in crisis.social:
    assert type(social.social_type) == str or type(social.social_type) == unicode
    assert type(social.social_id) == str or type(social.social_id) == unicode
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
      assert type(citation.description) == str or type(citation.description) == unicode
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
    assert type(link.description) == str or type(link.description) == unicode
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
  # Export as: <human-impact><deaths>...</deaths><injured>...</injured></human-impact>
  human_impact = Element('human-impact')
  if crisis.us_humanDeaths:
    humImp_Ele = Element('deaths')
    assert type(crisis.us_humanDeaths) == long or type(crisis.us_humanDeaths) == int
    humImp_Ele.text = str(crisis.us_humanDeaths)
    human_impact.append(humImp_Ele)
  if crisis.us_humanMissing:
    humImp_Ele = Element('missing')
    assert type(crisis.us_humanMissing) == long or type(crisis.us_humanMissing) == int
    humImp_Ele.text = str(crisis.us_humanMissing)
    human_impact.append(humImp_Ele)
  if crisis.us_humanInjured:
    humImp_Ele = Element('injured')
    assert type(crisis.us_humanInjured) == long or type(crisis.us_humanInjured) == int
    humImp_Ele.text = str(crisis.us_humanInjured)
    human_impact.append(humImp_Ele)
  if crisis.us_humanDisplaced:
    humImp_Ele = Element('displaced')
    assert type(crisis.us_humanDisplaced) == long or type(crisis.us_humanDisplaced) == int
    humImp_Ele.text = str(crisis.us_humanDisplaced)
    human_impact.append(humImp_Ele)

  ele.append(human_impact)

  # economic impact is stored as a list in GAE
  # Export as: <economic-impact>...</economic-impact>
  if crisis.us_economicImpact:
    econ_impact = Element('economic-impact')
    assert type(crisis.us_economicImpact) == long or type(crisis.us_economicImpact) == int
    econ_impact.text = str(crisis.us_economicImpact)
    ele.append(econ_impact)


  # resources needed is stored as a list in GAE
  # Export as: <resources-needed><resource>...</resource></resources-needed>
  resources = Element('resources-needed')
  for resource in crisis.us_resourcesNeeded:
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
  
  org_refs = []
  for org in crisis.organizations:
    org_refs.append(str(org.organization.us_id))
  if len(org_refs) > 0:
    org_refs_ele = Element('organization-refs')
    org_refs_ele.text = " ".join(org_refs)
    ele.append(org_refs_ele)

  p_refs = []
  for p in crisis.people:
    p_refs.append(str(p.person.us_id))
  if len(p_refs) > 0:
    p_refs_ele = Element('person-refs')
    p_refs_ele.text = " ".join(p_refs)
    ele.append(p_refs_ele)

  return ele

def addOrganization(organization):

  """
    build xml organization element based on WC2.xsd (hard coded, meaning changes to xsd will not reflect here)
    organization is an Organization object from the GAE datastore
    return organization xml element
    """
  
  ele = Element('organization')
  ele.attrib['id'] = str(organization.us_id)

  name = Element('name')
  assert type(organization.us_name) == str or type(organization.us_name) == unicode
  name.text = organization.us_name
  ele.append(name)

  # Alternate Names is stored as a list in datastore
  # Export as: <alternate-names>...</alternate-names>
  if organization.us_alternateNames:
    altName = Element('alternate-names')
    assert type(organization.us_alternateNames) == str or type(organization.us_alternateNames) == unicode
    altName.text = organization.us_alternateNames
    ele.append(altName)

  kind = Element('kind')
  assert type(organization.us_type) == str or type(organization.us_type) == unicode
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
    assert type(organization.us_city) == str or type(organization.us_city) == unicode
    city.text = organization.us_city
    location.append(city)

  if organization.us_state:
    state = Element('state')
    assert type(organization.us_state) == str or type(organization.us_state) == unicode
    state.text = organization.us_state
    location.append(state)

  assert type(organization.us_country) == str or type(organization.us_country) == unicode
  country = Element('country')
  country.text = organization.us_country
  location.append(country)

  if organization.us_latitude:
    latitude = Element('latitude')
    assert type(organization.us_latitude) == str or type(organization.us_latitude) == unicode
    latitude.text = organization.us_latitude
    location.append(latitude)

  if organization.us_longitude:
    longitude = Element('longitude')
    assert type(organization.us_longitude) == str or type(organization.us_longitude) == unicode
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
      assert type(image.description) == str or type(image.description) == unicode
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
      assert type(map.description) == str or type(map.description) == unicode
      des_ele = Element('description')
      des_ele.text = map.description
      map_ele.append(des_ele)
    maps_main.append(map_ele)
  ele.append(maps_main)

  # Video is another entity in GAE
  # Export as: <videos><..>..</..></videos>
  video_main = Element('videos')
  for video in organization.videos:
    assert type(video.video_type) == str or type(video.video_type) == unicode
    assert type(video.video_id) == str or type(video.video_id) == unicode
    video_ele = Element(video.video_type)
    video_ele.text = video.video_id
    video_main.append(video_ele)
  ele.append(video_main)

  # Social is another entity in GAE
  # Export as: <social><..>..</..></social>
  social_main = Element('social')
  for social in organization.social:
    assert type(social.social_type) == str or type(social.social_type) == unicode
    assert type(social.social_id) == str or type(social.social_id) == unicode
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
      assert type(citation.description) == str or type(citation.description) == unicode
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
    assert type(link.description) == str or type(link.description) == unicode
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
    assert type(organization.us_email) == str or type(organization.us_email) == unicode
    email.text = organization.us_email
    ele.append(email)

  if organization.us_phone:
    phone = Element('phone')
    assert type(organization.us_phone) == str or type(organization.us_phone) == unicode
    phone.text = organization.us_phone
    ele.append(phone)

  c_refs = []
  for c in organization.crises:
    c_refs.append(str(c.crisis.us_id))
  if len(c_refs) > 0:
    c_refs_ele = Element('crisis-refs')
    c_refs_ele.text = " ".join(c_refs)
    ele.append(c_refs_ele)

  p_refs = []
  for p in organization.people:
    p_refs.append('p' + str(p.person.us_id))
  if len(p_refs) > 0:
    p_refs_ele = Element('person-refs')
    p_refs_ele.text = " ".join(p_refs)
    ele.append(p_refs_ele)

    
  return ele
  
def addPerson(person):
  """
    build xml person element based on WC2.xsd (hard coded, meaning changes to xsd will not reflect here)
    person is a Person object from the GAE datastore
    return person xml element
    """
  
  ele = Element('person')
  ele.attrib['id'] = str(person.us_id)

  name = Element('name')
  assert type(person.us_name) == str or type(person.us_name) == unicode
  name.text = person.us_name
  ele.append(name)

  # Alternate Names is stored as a list in datastore
  # Export as: <alternate-names>...</alternate-names>
  if person.us_alternateNames:
    altName = Element('alternate-names')
    assert type(person.us_alternateNames) == str or type(person.us_alternateNames) == unicode
    altName.text = person.us_alternateNames
    ele.append(altName)

  kind = Element('kind')
  assert type(person.us_type) == str or type(person.us_type) == unicode
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
    assert type(person.us_city) == str or type(person.us_city) == unicode
    city.text = person.us_city
    location.append(city)

  if person.us_state:
    state = Element('state')
    assert type(person.us_state) == str or type(person.us_state) == unicode
    state.text = person.us_state
    location.append(state)

  country = Element('country')
  assert type(person.us_country) == str or type(person.us_country) == unicode
  country.text = person.us_country
  location.append(country)

  if person.us_latitude:
    latitude = Element('latitude')
    assert type(person.us_latitude) == str or type(person.us_latitude) == unicode
    latitude.text = person.us_latitude
    location.append(latitude)

  if person.us_longitude:
    longitude = Element('longitude')
    assert type(person.us_longitude) == str or type(person.us_longitude) == unicode
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
      assert type(image.description) == str or type(image.description) == unicode
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
      assert type(map.description) == str or type(map.description) == unicode
      des_ele = Element('description')
      des_ele.text = map.description
      map_ele.append(des_ele)
    maps_main.append(map_ele)
  ele.append(maps_main)

  # Video is another entity in GAE
  # Export as: <videos><..>..</..></videos>
  video_main = Element('videos')
  for video in person.videos:
    assert type(video.video_type) == str or type(video.video_type) == unicode
    assert type(video.video_id) == str or type(video.video_id) == unicode
    video_ele = Element(video.video_type)
    video_ele.text = video.video_id
    video_main.append(video_ele)
  ele.append(video_main)

  # Social is another entity in GAE
  # Export as: <social><..>..</..></social>
  social_main = Element('social')
  for social in person.social:
    assert type(social.social_type) == str or type(social.social_type) == unicode
    assert type(social.social_id) == str or type(social.social_id) == unicode
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
      assert type(citation.description) == str or type(citation.description) == unicode
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
    assert type(link.description) == str or type(link.description) == unicode
    descrip_Elem.text = link.description
    link_ele.append(descrip_Elem)
    extLink_main.append(link_ele)
  ele.append(extLink_main)

  c_refs = []
  for c in person.crises:
    c_refs.append(str(c.crisis.us_id))
  if len(c_refs) > 0:
    c_refs_ele = Element('crisis-refs')
    c_refs_ele.text = " ".join(c_refs)
    ele.append(c_refs_ele)

  org_refs = []
  for org in person.organizations:
    org_refs.append(str(org.organization.us_id))
  if len(org_refs) > 0:
    org_refs_ele = Element('organization-refs')
    org_refs_ele.text = " ".join(org_refs)
    ele.append(org_refs_ele)
  return ele
