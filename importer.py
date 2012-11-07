from StringIO import StringIO
from minixsv import pyxsval as xsv
import xml.etree.ElementTree as ET
from google.appengine.ext import db
from Models import *
import datetime
import logging

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
    assert type(result_dict) == dict

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

def str_from_tree(etree):
    """
    Get the string representation of an ElementTree object
    etree is the desired root of the ElementTree
    returns a string representation using ElementTree.tos   tring()
    """
    return ET.tostring(etree)

# The handling of links is really gross. They're all individual dictionaries wrapped in lists
# We re-package them as a list of dictionaries with keys {source, description} so we can extract them in WC1.py

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
    '''
    Processes common data for Organization, Person, and Crisis. Modifies a mutable dictionary passed as an argument
    '''
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
    '''
    Processes special data such as videos, social media, etc. for Organization, Person, and Crisis
    '''
    assert type(result_dict) == dict

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
        except Exception:
            logging.warn("Empty tag found for images")
    elif key == 'maps':
        try:
            result_dict['maps']              = parse_links(xml_value, "map")
        except Exception:
            logging.warn("Empty tag found for maps")
    elif key == 'citations':
        try:
            result_dict['citations']         = parse_links(xml_value, "citation")
        except Exception:
            logging.warn("Empty tag found for citations")
    elif key == 'external-links':
        try:
            result_dict['external_links']    = parse_links(xml_value, "external-link")
        except Exception:
            logging.warn("Empty tag found for external_links")


def process_crisis(crisis):
    '''
    Parses crisis xml data into a dictionary to eventually end up in a model.
    '''

    result = {}
    logging.info(str(crisis))
    c = {}
    assert type(crisis) == dict
    # iterates through list of dictionaries
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
            else:
                process_special_data(k, v, result)

    crisis_instance     = Crisis(**c)
    result['crisis']    = crisis_instance
    #   {crisis_instance: crisis_instance, external_links: [{source, description}], citations: [()]}
    return result


def process_organization(organization):
    '''
    Parses organization xml data into a dictionary to eventually end up in a model.
    '''

    result = {}
    logging.info(organization)
    o = {}
    # iterates through list of dictionaries
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
            else:
                process_special_data(k, v, result)

    org_instance            = Organization(**o)
    result['organization']  = org_instance
    return result


def process_person(person):
    '''
    Parses person xml data into a dictionary to eventually end up in a model.
    '''

    result = {}
    p = {}
    # iterates through list of dictionaries
    for attribute_dictionary in person['person']:
        # iterates through attribute dictionary
        for k,v in attribute_dictionary.items():
            if proccess_common_data(k, v, p):
                pass
            else:
                process_special_data(k, v, result)

    person_instance     = Person(**p)
    result['person']    = person_instance
    return result