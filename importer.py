from google.appengine.ext import db
from Models import *
import datetime
import logging

#def process(tree):
#    '''
#    go through elementtree and create objects from elements
#    '''
#    root = tree.getroot()
#    for i in root.iter():
#        if i.tag == 'crises':
#
#            process_crises(i)
#        elif i.tag == 'organizations':
#            process_organizations(i)
#        elif i.tag == 'people':
#            process_people(i)

#def process_crises(element):
#    # Iterates through all crises
#    dict = etree_to_dict(element)
#    # for all crises
#    for crisis in dict.get('crises'):
#        print crisis
#        c = Crisis
#        # iterates through list of dictionaries
#        for attribute_dictionary in crisis['crisis']:
#            # iterates through attribute dictionary
#            print "attribute dictionary: " + str(attribute_dictionary)
#            for k,v in attribute_dictionary.items():
#                print "k: " + str(k)
#                print "v: " + str(v)
#                # set attributes of crisis class and prepend 'us_' to field names
#                setattr(c, "us_" + str(k), v)
#        print crisis
#    print
#    print
#    print
#    print Crisis


# {'crisis': [{'name': 'Breast Cancer'}, {'kind': 'Cancer'}, {'description': 'Breast cancer is a type of cancer originating from breast tissue, most commonly from the inner lining of milk ducts or the lobules that supply the ducts with milk.'}, {'location': [{'country': 'USA'}]}, {'images': [{'image': [{'source': 'http://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Mammo_breast_cancer.jpg/230px-Mammo_breast_cancer.jpg'}, {'description': 'Breast Cancer'}]}]}, {'maps': '\n\t\t\t'}, {'videos': [{'youtube': 'YNUBnX9JHQs'}]}, {'social': [{'twitter': '@BrstCancerNews'}]}, {'citations': [{'citation': [{'source': 'http://en.wikipedia.org/wiki/Breast_cancer'}, {'description': 'Wiki'}]}, {'citation': [{'source': 'http://www.ncbi.nlm.nih.gov/pubmed/17345557'}, {'description': 'Economic Impact'}]}, {'citation': [{'source': 'http://c-changetogether.org/Websites/cchange/images/Publications%20and%20Reports/Reports/Disparities%20Report.pdf'}, {'description': 'Societal Impact'}]}, {'citation': [{'source': 'http://www.cancer.gov/cancertopics/types/breast'}, {'description': 'Cancer.gov on breast cancer'}]}]}, {'external-links': [{'external-link': [{'source': 'http://www.nationalbreastcancer.org/breast-cancer-support'}, {'description': 'How to help 1'}]}, {'external-link': [{'source': 'http://www.bcsupport.org/'}, {'description': 'How to help 2'}]}, {'external-link': [{'source': 'http://www.huffingtonpost.com/hayley-rose-horzepa/breast-cancer-awareness_b_1990310.html'}, {'description': 'Awareness 1'}]}, {'external-link': [{'source': 'http://www.nationalpartnership.org'}, {'description': 'Awareness 2'}]}]}, {'start-date': '1776-07-04T00:00:00'}, {'end-date': '2012-10-22T00:00:00'}, {'human-impact': [{'statistic': '230,480 people per year'}]}, {'economic-impact': [{'statistic': '$60,000 per person'}]}, {'resources-needed': [{'resource': 'money'}, {'resource': 'donations'}, {'resource': 'research'}]}, {'ways-to-help': [{'way': 'donations'}, {'way': 'volunteering'}, {'way': 'fundraising'}, {'way': 'pink ribbons'}, {'way': 'support'}]}]}

# TODO: conversions of types?
# TODO: error handling as specified by project properties
def process_crisis(crisis):
    result = {}
    print crisis
    c = {}
    # iterates through list of dictionaries
    for attribute_dictionary in crisis['crisis']:
        # iterates through attribute dictionary
        print "attribute dictionary: " + str(attribute_dictionary)
        for k,v in attribute_dictionary.items():
            if k == 'name':
                c['us_name'] = str(v)
##            elif k == 'alternate-names':
##                #TODO: test this with xml containing alternate names
##                c['us_alternateNames'] = v
            elif k == 'alternate-names':
                altNames = []
                for name in v:
                    altNames.append(name)
                c['us_alternateNames'] = altNames
            elif k == 'kind':
                c['us_type'] = str(v)
            elif k == 'description':
                c['us_description'] = db.Text(v)
            elif k == 'location':
                for value in v:
                    if 'city' in value:
                        c['us_city'] = str(value['city'])
                    if 'state' in value:
                        c['us_state'] = str(value['state'])
                    if 'country' in value:
                        c['us_country'] = str(value['country'])
                    if 'latitude' in value:
                        c['us_latitude'] = str(value['latitude'])
                    if 'longitude' in value:
                        c['us_longitude'] = str(value['longitude'])
##            # TODO: images
##            elif k == 'images':
##                images = []
##                for image in v:
##                    images.append(image['image'])
##            # TODO: maps
##            elif k == 'maps':
##                maps = []
##                for map in v:
##                    maps.append(map['map'])
##                result['maps']
            # TODO: videos
            # TODO: social
            # TODO: citations
            # TODO: external links
            elif k == 'start-date':
                c['us_startDate'] = datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S')
            elif k == 'end-date':
                c['us_endDate'] = datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S')
            elif k == 'economic-impact':
                stats = []
                for statistic in v:
                    stats.append(statistic['statistic'])
                c['us_economicImpact'] = stats
            elif k == 'human-impact':
                stats = []
                for statistic in v:
                    stats.append(statistic['statistic'])
                c['us_humanImpact'] = stats
            elif k == 'resources-needed':
                res = []
                for resource in v:
                    res.append(resource['resource'])
                c['us_resoucesNeeded'] = res
            elif k == 'ways-to-help':
                ways = []
                for way in v:
                    ways.append(way['way'])
                c['us_waysToHelp'] = ways
    crisis_instance = Crisis(**c)

    #
    #   {crisis_instance: crisis_instance, external_links: [{source, description}], citations: [()]}
    # result['crisis'] =  crisis_instance
    # return result

    return crisis_instance

def process_organization(organization):
    result = {}
    print organization
    logging.info(organization)
    o = {}
    # iterates through list of dictionaries
    for attribute_dictionary in organization['organization']:
        # iterates through attribute dictionary
        print "attribute dictionary: " + str(attribute_dictionary)
        for k,v in attribute_dictionary.items():
            if k == 'name':
                o['us_name'] = str(v)
            elif k == 'alternate-names':
                #TODO: test this with xml containing alternate names
                o['us_alternateNames'] = v
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
                
##            # TODO: images
##            elif k == 'images':
##                images = []
##                for image in v:
##                    images.append(image['image'])
##            # TODO: maps
##            elif k == 'maps':
##                maps = []
##                for map in v:
##                    maps.append(map['map'])
##                result['maps']
            # TODO: videos
            # TODO: social
            # TODO: citations
            # TODO: external links
    org_instance = Organization(**o)

    #
    #   {crisis_instance: crisis_instance, external_links: [{source, description}], citations: [()]}
    # result['crisis'] =  crisis_instance
    # return result

    return org_instance

def process_person(person):
    result = {}
    print person
    p = {}
    # iterates through list of dictionaries
    for attribute_dictionary in person['person']:
        # iterates through attribute dictionary
        print "attribute dictionary: " + str(attribute_dictionary)
        for k,v in attribute_dictionary.items():
            if k == 'name':
                p['us_name'] = str(v)
            elif k == 'alternate-names':
                altNames = []
                for name in v:
                    altNames.append(name)
                p['us_alternateNames'] = altNames
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
                
##            # TODO: images
##            elif k == 'images':
##                images = []
##                for image in v:
##                    images.append(image['image'])
##            # TODO: maps
##            elif k == 'maps':
##                maps = []
##                for map in v:
##                    maps.append(map['map'])
##                result['maps']
            # TODO: videos
            # TODO: social
            # TODO: citations
            # TODO: external links
    person_instance = Person(**p)

    #
    #   {crisis_instance: crisis_instance, external_links: [{source, description}], citations: [()]}
    # result['crisis'] =  crisis_instance
    # return result

    return person_instance

#process(tree)
