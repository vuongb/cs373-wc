from google.appengine.ext import db
from Models import *
import datetime
import logging

# The handling of links is really gross. They're all individual dictionaries wrapped in lists
# We re-package them as a list of dictionaries with keys {source, description} so we can extract them in WC1.py

def parse_links(dict_value, type_as_string):
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

# {'crisis': [{'name': 'Breast Cancer'}, {'kind': 'Cancer'}, {'description': 'Breast cancer is a type of cancer originating from breast tissue, most commonly from the inner lining of milk ducts or the lobules that supply the ducts with milk.'}, {'location': [{'country': 'USA'}]}, {'images': [{'image': [{'source': 'http://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Mammo_breast_cancer.jpg/230px-Mammo_breast_cancer.jpg'}, {'description': 'Breast Cancer'}]}]}, {'maps': '\n\t\t\t'}, {'videos': [{'youtube': 'YNUBnX9JHQs'}]}, {'social': [{'twitter': '@BrstCancerNews'}]}, {'citations': [{'citation': [{'source': 'http://en.wikipedia.org/wiki/Breast_cancer'}, {'description': 'Wiki'}]}, {'citation': [{'source': 'http://www.ncbi.nlm.nih.gov/pubmed/17345557'}, {'description': 'Economic Impact'}]}, {'citation': [{'source': 'http://c-changetogether.org/Websites/cchange/images/Publications%20and%20Reports/Reports/Disparities%20Report.pdf'}, {'description': 'Societal Impact'}]}, {'citation': [{'source': 'http://www.cancer.gov/cancertopics/types/breast'}, {'description': 'Cancer.gov on breast cancer'}]}]}, {'external-links': [{'external-link': [{'source': 'http://www.nationalbreastcancer.org/breast-cancer-support'}, {'description': 'How to help 1'}]}, {'external-link': [{'source': 'http://www.bcsupport.org/'}, {'description': 'How to help 2'}]}, {'external-link': [{'source': 'http://www.huffingtonpost.com/hayley-rose-horzepa/breast-cancer-awareness_b_1990310.html'}, {'description': 'Awareness 1'}]}, {'external-link': [{'source': 'http://www.nationalpartnership.org'}, {'description': 'Awareness 2'}]}]}, {'start-date': '1776-07-04T00:00:00'}, {'end-date': '2012-10-22T00:00:00'}, {'human-impact': [{'statistic': '230,480 people per year'}]}, {'economic-impact': [{'statistic': '$60,000 per person'}]}, {'resources-needed': [{'resource': 'money'}, {'resource': 'donations'}, {'resource': 'research'}]}, {'ways-to-help': [{'way': 'donations'}, {'way': 'volunteering'}, {'way': 'fundraising'}, {'way': 'pink ribbons'}, {'way': 'support'}]}]}

# TODO: conversions of types?
# TODO: error handling as specified by project properties
def process_crisis(crisis):
    result = {}
    logging.info(str(crisis))
    c = {}
    # iterates through list of dictionaries
    for attribute_dictionary in crisis['crisis']:
        # iterates through attribute dictionary
        for k,v in attribute_dictionary.items():
            if k == 'name':
                c['us_name'] = str(v)
##            elif k == 'alternate-names':
##                #TODO: test this with xml containing alternate names
##                c['us_alternateNames'] = v
            elif k == 'alternate-names':
                altNames = []
                for name in v:
                    altNames.append(name['alternate-name'])
                c['us_alternateNames'] = altNames
            elif k == 'kind':
                c['us_type'] = str(v)
            elif k == 'description':
                c['us_description'] = db.Text(v)
            elif k == 'location':
                for value in v:
                    if 'city' in value:
                        c['us_city']        = str(value['city'])
                    if 'state' in value:
                        c['us_state']       = str(value['state'])
                    if 'country' in value:
                        c['us_country']     = str(value['country'])
                    if 'latitude' in value:
                        c['us_latitude']    = str(value['latitude'])
                    if 'longitude' in value:
                        c['us_longitude']   = str(value['longitude'])
            elif k == 'start-date':
                c['us_startDate'] = datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S')
            elif k == 'end-date':
                c['us_endDate'] = datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S')
            elif k == 'economic-impact':
                c['us_economicImpact'] = int(v)
            elif k == 'human-impact':
                for dict in v:
                    if "deaths" in dict:
                        c['us_humanDeaths']     = int(dict['deaths'])
                    if "missing" in dict:
                        c['us_humanMissing']    = int(dict['missing'])
                    if "injured" in dict:
                        c['us_humanInjured']    = int(dict['injured'])
                    if "displaced" in dict:
                        c['us_humanDisplaced']  = int(dict['displaced'])
            elif k == 'resources-needed':
                res = []
                for resource in v:
                    res.append(resource['resource'])
                c['us_resourcesNeeded'] = res
            elif k == 'ways-to-help':
                ways = []
                for way in v:
                    ways.append(way['way'])
                c['us_waysToHelp'] = ways

            # The following are associated classes (not properties of Crisis)
            elif k == 'videos':
                videos = []
                for video in v:
                    videos.append(video)
                result['videos']    = videos
            elif k == 'social':
                socials = []
                for social in v:
                    socials.append(social)
                result['social']    = socials
            elif k == 'images':
                try:
                    result['images']            = parse_links(v, "image")
                except Exception:
                    logging.warn("Empty tag found for images")
            elif k == 'maps':
                try:
                    result['maps']              = parse_links(v, "map")
                except Exception:
                    logging.warn("Empty tag found for maps")
            elif k == 'citations':
                try:
                    result['citations']         = parse_links(v, "citation")
                except Exception:
                    logging.warn("Empty tag found for citations")
            elif k == 'external-links':
                try:
                    result['external_links']    = parse_links(v, "external-link")
                except Exception:
                    logging.warn("Empty tag found for external_links")

    crisis_instance     = Crisis(**c)
    result['crisis']    =  crisis_instance
    #   {crisis_instance: crisis_instance, external_links: [{source, description}], citations: [()]}
    return result

def process_organization(organization):
    result = {}
    logging.info(organization)
    o = {}
    # iterates through list of dictionaries
    for attribute_dictionary in organization['organization']:
        # iterates through attribute dictionary
        for k,v in attribute_dictionary.items():
            if k == 'name':
                o['us_name'] = str(v)
            elif k == 'alternate-names':
                altNames = []
                for name in v:
                    altNames.append(name['alternate-name'])
                o['us_alternateNames'] = altNames
            elif k == 'kind':
                o['us_type'] = str(v)
            elif k == 'description':
                o['us_description'] = db.Text(v)
            elif k == 'location':
                for value in v:
                    if 'city' in value:
                        o['us_city'] = str(value['city'])
                    if 'state' in value:
                        o['us_state'] = str(value['state'])
                    if 'country' in value:
                        o['us_country'] = str(value['country'])
                    if 'latitude' in value:
                        o['us_latitude'] = str(value['latitude'])
                    if 'longitude' in value:
                        o['us_longitude'] = str(value['longitude'])
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

            # The following are associated classes (not properties of Organization)
            elif k == 'videos':
                videos = []
                for video in v:
                    videos.append(video)
                result['videos']    = videos
            elif k == 'social':
                socials = []
                for social in v:
                    socials.append(social)
                result['social']    = socials
            elif k == 'images':
                try:
                    result['images']            = parse_links(v, "image")
                except Exception:
                    logging.warn("Empty tag found for images")
            elif k == 'maps':
                try:
                    result['maps']              = parse_links(v, "map")
                except Exception:
                    logging.warn("Empty tag found for maps")
            elif k == 'citations':
                try:
                    result['citations']         = parse_links(v, "citation")
                except Exception:
                    logging.warn("Empty tag found for citations")
            elif k == 'external-links':
                try:
                    result['external_links']    = parse_links(v, "external-link")
                except Exception:
                    logging.warn("Empty tag found for external_links")

    org_instance            = Organization(**o)
    result['organization']  = org_instance
    return result

def process_person(person):
    result = {}
    p = {}
    # iterates through list of dictionaries
    for attribute_dictionary in person['person']:
        # iterates through attribute dictionary
        for k,v in attribute_dictionary.items():
            if k == 'name':
                p['us_name'] = str(v)
            if k == 'alternate-names':
                p['us_alternateNames'] = v
            elif k == 'kind':
                p['us_type'] = str(v)
            elif k == 'description':
                p['us_description'] = db.Text(v)
            elif k == 'location':
                for value in v:
                    if 'city' in value:
                        p['us_city'] = str(value['city'])
                    if 'state' in value:
                        p['us_state'] = str(value['state'])
                    if 'country' in value:
                        p['us_country'] = str(value['country'])
                    if 'latitude' in value:
                        p['us_latitude'] = str(value['latitude'])
                    if 'longitude' in value:
                        p['us_longitude'] = str(value['longitude'])

            # The following are associated classes (not properties of Person)
            elif k == 'videos':
                videos = []
                for video in v:
                    videos.append(video)
                result['videos']    = videos
            elif k == 'social':
                socials = []
                for social in v:
                    socials.append(social)
                result['social']    = socials
            elif k == 'images':
                try:
                    result['images']            = parse_links(v, "image")
                except Exception:
                    logging.warn("Empty tag found for images")
            elif k == 'maps':
                try:
                    result['maps']              = parse_links(v, "map")
                except Exception:
                    logging.warn("Empty tag found for maps")
            elif k == 'citations':
                try:
                    result['citations']         = parse_links(v, "citation")
                except Exception:
                    logging.warn("Empty tag found for citations")
            elif k == 'external-links':
                try:
                    result['external_links']    = parse_links(v, "external-link")
                except Exception:
                    logging.warn("Empty tag found for external_links")

    person_instance     = Person(**p)
    result['person']    = person_instance
    return result

#process(tree)
