from StringIO import StringIO
from minixsv import pyxsval as xsv
import xml.etree.ElementTree as ET
from google.appengine.ext import db
from Models import *
import datetime
import logging

def get_tree_and_validate(data, schema):
    """
    validate an xml string against a schema string and return an ETree representation if it is valid
    data is the xml data to validate and build a tree from
    schema is the schema to validate against
    returns 0 if the xml is invalid, and an ETree if it is
    """
    try:
        xsv.parseAndValidateXmlInputString(data, schema, xmlIfClass=xsv.XMLIF_ELEMENTTREE)
        return ET.parse(StringIO(data))
    except xsv.XsvalError as e:
        logging.debug("XML NOT VALID. Trace: \n" + str(e))
        return 0

#http://stackoverflow.com/questions/7684333/converting-xml-to-dictionary-using-elementtree
def etree_to_dict(t):
    """recursively converts an ETree into a dict"""
    if not t.getchildren():
        # checks for shorthand empty XML tag
        if t.text is None:
            d = {t.tag: []}
        else:
            d = {t.tag: t.text}
    else:
        if t.attrib:
            assert type(t.attrib) == dict
            d = {t.tag : map(etree_to_dict, t.getchildren()), "id" : t.attrib['id']}
        else:
            d = {t.tag : map(etree_to_dict, t.getchildren())}
    return d


def store_references(references):
    assert type(references) == dict
    for object1, refs in references.items():

        assert type(refs) == dict
        for k, v in refs.items():
            # https://developers.google.com/appengine/docs/python/datastore/gqlqueryclass
            try:
                if k == 'crisis-refs':
                    object2 = Crisis.gql("WHERE us_id = :objname", objname = v).get()
                if k == 'organization-refs':
                    object2 = Organization.gql("WHERE us_id = :objname", objname = v).get()
                if k == 'person-refs':
                    object2 = Person.gql("WHERE us_id = :objname", objname = v).get()
            except Exception as e:
                logging.error("Exception getting reference into datastore. %s", e)

            try:
                # TODO: should the xml still validate if an error is thrown?
                # CrisisOrganization
                if (type(object1) == Crisis) and (type(object2) == Organization):
                    CrisisOrganization(crisis=object1, organization=object2).put()
                # CrisisPerson
                elif (type(object1) == Crisis) and (type(object2) == Person):
                    CrisisPerson(crisis=object1, person=object2).put()
                # OrganizationPerson
                elif (type(object1) == Organization) and (type(object2) == Person):
                    OrganizationPerson(organization=object1, person=object2).put()
            except Exception as e:
                logging.error("Exception putting reference into datastore. %s", e)



def store_special_classes(result_dict, assoc_obj):
    """ creates relational/child objects like videos, social, images, maps, etc from dict data
    """
    assert type(result_dict) == dict

    videos          = result_dict.get('videos')
    if videos:
        for video in videos:
            builder                 = {'video_type': video.items()[0][0],
                                       'video_id': video.items()[0][1],
                                       'assoc_object': assoc_obj}
            Video(**builder).put()
    social          = result_dict.get('social')
    if social:
        for media in social:
            builder                 = {'social_type': media.items()[0][0],
                                       'social_id': media.items()[0][1],
                                       'assoc_object': assoc_obj}
            Social(**builder).put()
    images          = result_dict.get('images')
    if images:
        for image in images:
            builder                 = {'source': image.get('source'),
                                       'description': image.get('description'),
                                       'assoc_object': assoc_obj}
            Image(**builder).put()
    maps            = result_dict.get('maps')
    if maps:
        for map in maps:
            builder                 = {'source': map.get('source'),
                                       'description': map.get('description'),
                                       'assoc_object': assoc_obj}
            Map(**builder).put()
    citations       = result_dict.get('citations')
    if citations:
        for citation in citations:
            builder                 = {'source': citation.get('source'),
                                       'description': citation.get('description'),
                                       'assoc_object': assoc_obj}
            Citation(**builder).put()
    external_links  = result_dict.get('external_links')
    if external_links:
        for link in external_links:
            builder                 = {'source': link.get('source'),
                                       'description': link.get('description'),
                                       'assoc_object': assoc_obj}
            ExternalLink(**builder).put()

def str_from_tree(etree):
    """
    Get the string representation of an ElementTree object
    etree is the desired root of the ElementTree
    returns a string representation using ElementTree.tos   tring()
    """
    return ET.tostring(etree)

# The handling of links is really gross. They're all individual dictionaries wrapped in lists
# We re-package them as a list of dictionaries with keys {source, description} so we can extract them in WC2.py

def parse_links(dict_value, type_as_string):
    assert type(type_as_string) == str

    logging.info("type: %s", type_as_string)
    links = []
    for link in dict_value:
        link_data               = {}
        link_source             = link[type_as_string][0]['source']
        link_description        = link[type_as_string][1]['description']
        link_data['source']     = link_source
        link_data['description']= link_description
        links.append(link_data)
    return links


def proccess_common_data(key, xml_value, result_dict):
    """
    Processes common data for Organization, Person, and Crisis. Modifies a mutable dictionary passed as an argument
    """
    assert type(result_dict) == dict

    value_inserted = True
    if key == 'name':
        result_dict['us_name'] = str(xml_value)
    elif key == 'alternate-names':
        result_dict['us_alternateNames'] = xml_value
    elif key == 'kind':
        result_dict['us_type'] = str(xml_value)
    elif key == 'description':
        result_dict['us_description'] = db.Text(xml_value)
    elif key == 'location':
        for value in xml_value:
            if 'city' in value:
                result_dict['us_city']        = str(value['city'])
            if 'state' in value:
                result_dict['us_state']       = str(value['state'])
            if 'country' in value:
                result_dict['us_country']     = str(value['country'])
            if 'latitude' in value:
                result_dict['us_latitude']    = str(value['latitude'])
            if 'longitude' in value:
                result_dict['us_longitude']   = str(value['longitude'])
    else:
        value_inserted = False
    return value_inserted


def process_special_data(key, xml_value, result_dict):
    """
    Processes special data such as videos, social media, etc. for Organization, Person, and Crisis
    """
    assert type(result_dict) == dict

    value_inserted = True
    if key == 'videos':
        videos = []
        for video in xml_value:
            videos.append(video)
        result_dict['videos']    = videos
    elif key == 'social':
        socials = []
        for social in xml_value:
            socials.append(social)
        result_dict['social']    = socials
    elif key == 'images':
        try:
            result_dict['images']            = parse_links(xml_value, "image")
        except KeyError:
            logging.warn("Empty tag found for images")
    elif key == 'maps':
        try:
            result_dict['maps']              = parse_links(xml_value, "map")
        except KeyError:
            logging.warn("Empty tag found for maps")
    elif key == 'citations':
        try:
            result_dict['citations']         = parse_links(xml_value, "citation")
        except KeyError:
            logging.warn("Empty tag found for citations")
    elif key == 'external-links':
        try:
            result_dict['external_links']    = parse_links(xml_value, "external-link")
        except KeyError:
            logging.warn("Empty tag found for external_links")
    else:
        value_inserted = False
    return value_inserted


def process_references(xml_key, xml_value, references_dict):
    """
    Processes references to other objects. Modifies a mutable dictionary passed as an argument
    """
    assert type(references_dict) == dict

    value_inserted = True
    if xml_key == 'crisis-refs' :
        references_dict['crisis-refs']          = xml_value
    if xml_key == 'person-refs' :
        references_dict['person-refs']          = xml_value
    if xml_key == 'organization-refs' :
        references_dict['organization-refs']    = xml_value
    else:
        value_inserted = False
    return value_inserted


def process_crisis(crisis):
    """
    Parses crisis xml data into a dictionary to eventually end up in a model.
    """
    assert type(crisis) == dict

    logging.info(str(crisis))
    references  = {}
    result      = {}
    c           = {}

    # id is handled a bit differently in the XML
    assert crisis['id']
    c['us_id']  = crisis['id']

    # iterates through list of dictionaries (elements of XML object)
    for attribute_dictionary in crisis['crisis']:
        assert type(attribute_dictionary) == dict
        # iterates through attribute dictionary
        for k,v in attribute_dictionary.items():
            if proccess_common_data(k, v, c):
                pass
            elif k == 'start-date':
                c['us_startDate'] = datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S')
            elif k == 'end-date':
                c['us_endDate'] = datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S')
            elif k == 'economic-impact':
                c['us_economicImpact'] = int(v)
            elif k == 'human-impact':
                assert type(v) == list
                for impact_dict in v:
                    if "deaths" in impact_dict:
                        c['us_humanDeaths']     = int(impact_dict['deaths'])
                    if "missing" in impact_dict:
                        c['us_humanMissing']    = int(impact_dict['missing'])
                    if "injured" in impact_dict:
                        c['us_humanInjured']    = int(impact_dict['injured'])
                    if "displaced" in impact_dict:
                        c['us_humanDisplaced']  = int(impact_dict['displaced'])
            elif k == 'resources-needed':
                res = []
                assert type(v) == list
                for resource in v:
                    res.append(resource['resource'])
                c['us_resourcesNeeded'] = res
            elif k == 'ways-to-help':
                ways = []
                for way in v:
                    ways.append(way['way'])
                c['us_waysToHelp'] = ways
            elif process_special_data(k, v, result):
                pass
            else:
                process_references(k, v, references)

    crisis_instance     = Crisis(**c)
    result['crisis']    = crisis_instance
    result['references']= references
    return result


def process_organization(organization):
    """
    Parses organization xml data into a dictionary to eventually end up in a model.
    """
    assert type(organization) == dict

    logging.info(str(organization))
    references  = {}
    result      = {}
    o           = {}

    # id is handled a bit differently in the XML
    assert organization['id']
    o['us_id']  = organization['id']

    # iterates through list of dictionaries (elements of XML object)
    for attribute_dictionary in organization['organization']:
        # iterates through attribute dictionary
        for k,v in attribute_dictionary.items():
            if proccess_common_data(k, v, o):
                pass
            elif k == 'contact-info':
                for value in v:
                    if 'address' in value:
                        o['us_address'] = str(value['address'])
                    if 'email' in value:
                        o['us_email'] = str(value['email'])
                    if 'phone' in value:
                        o['us_phone'] = str(value['phone'])
            elif k == 'address':
                o['us_address'] = str(v)
            elif k == 'email':
                o['us_email'] = str(v)
            elif k == 'phone':
                o['us_phone'] = str(v)
            elif process_special_data(k, v, result):
                pass
            else:
                process_references(k, v, references)

    org_instance            = Organization(**o)
    result['organization']  = org_instance
    result['references']= references
    return result


def process_person(person):
    """
    Parses person xml data into a dictionary to eventually end up in a model.
    """
    assert type(person) == dict

    logging.info(str(person))
    references  = {}
    result      = {}
    p           = {}

    # id is handled a bit differently in the XML
    assert person['id']
    p['us_id']  = person['id']

    # iterates through list of dictionaries (elements of XML object)
    for attribute_dictionary in person['person']:
        # iterates through attribute dictionary
        for k,v in attribute_dictionary.items():
            if proccess_common_data(k, v, p):
                pass
            elif process_special_data(k, v, result):
                pass
            else:
                process_references(k, v, references)

    person_instance     = Person(**p)
    result['person']    = person_instance
    result['references']= references
    return result

def put_objects(root):
    """
    processes and inserts objects from the tree into the data store
    root is the root of an ElementTree
    return True if successful, otherwise False
    """
    # iterate over types
    try:
        references = {}
        # iterate over types
        for i in root.iter():
            if i.tag == 'crises':
                # iterate through all crises
                d = etree_to_dict(i)
                for c in d.get('crises'):
                    if type(c) != str:  # TODO: what is this? Can we remove it?
                        result_dict     = process_crisis(c)

                        # get the crisis dictionary from result dict and put it in the datastore
                        crisis          = result_dict.get('crisis')
                        crisis.put()

                        # TODO: clean up by returning a 'media' dict which we send to store_special_classes
                        store_special_classes(result_dict, crisis)

                        # Get the references for this object and store them for later (after obj processing)
                        references_dict     = result_dict.get('references')
                        if references_dict:
                            references[crisis]  = references_dict
            elif i.tag == 'organizations':
                # iterate through all organizations
                d = etree_to_dict(i)
                logging.info(d)
                for o in d.get('organizations'):
                    if type(o) != str:
                        result_dict     = process_organization(o)

                        # get the organization dictionary from result dict and put it in the datastore
                        organization    = result_dict.get('organization')
                        organization.put()

                        # TODO: clean up by returning a 'media' dict which we send to store_special_classes
                        store_special_classes(result_dict, organization)

                        # Get the references for this object and store them for later (after obj processing)
                        references_dict             = result_dict.get('references')
                        if references_dict:
                            references[organization]    = references_dict
            elif i.tag == 'people':
                # iterate through all person
                d = etree_to_dict(i)
                for p in d.get('people'):
                    if type(p) != str:
                        result_dict     = process_person(p)

                        # get the person dictionary from result dict and put it in the datastore
                        person          = result_dict.get('person')
                        person.put()

                        # TODO: clean up by returning a 'media' dict which we send to store_special_classes
                        store_special_classes(result_dict, person)

                        # Get the references for this object and store them for later (after obj processing)
                        references_dict     = result_dict.get('references')
                        if references_dict:
                            references[person]  = references_dict
        store_references(references)
        return True
    except BaseException as e:
        print(e)
        return False
