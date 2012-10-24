from google.appengine.ext import db
from minixsv import pyxsval as xsv
import xml.etree.ElementTree as ET
from Models import Crisis
import datetime
import time


SCHEMA='cassie-schema-statistics.xsd'

#tree = ET.parse('crisis-breast_cancer.xml')
#root = tree.getroot()
#print(root.tag, root.attrib)

def get_tree_and_validate(data, schema):
    try:
        wrapper = xsv.parseAndValidateXmlInput(data, schema, xmlIfClass=xsv.XMLIF_ELEMENTTREE)
        validates = wrapper.getTree()
        return ET.parse(data)
    except xsv.XsvalError as e:
        print("XML did not validate\n"+str(e))

tree = get_tree_and_validate('xml_instances/crisis-breast_cancer.xml', SCHEMA)

#http://stackoverflow.com/questions/7684333/converting-xml-to-dictionary-using-elementtree
def etree_to_dict(t):
    if t.getchildren() == []:
        d = {t.tag: t.text}
    else:
        d = {t.tag : map(etree_to_dict, t.getchildren())}
    return d

def process(tree):
    '''
    go through elementtree and create objects from elements
    '''
    root = tree.getroot()
    for i in root.iter():
        if i.tag == 'crises':

            process_crises(i)
        elif i.tag == 'organizations':
            process_organizations(i)
        elif i.tag == 'people':
            process_people(i)

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
def process_crises(element):
    # Iterates through all crises
    dict = etree_to_dict(element)
    # for all crises
    for crisis in dict.get('crises'):
        print crisis
        c = dict
        # iterates through list of dictionaries
        for attribute_dictionary in crisis['crisis']:
            # iterates through attribute dictionary
            print "attribute dictionary: " + str(attribute_dictionary)
            for k,v in attribute_dictionary.items():
                if k == 'name':
                    c.us_name = str(v)
                elif k == 'alternate-names':
                    #TODO: test this with xml containing alternate names
                    c.us_alternateNames = v
                elif k == 'kind':
                    c.us_type = str(v)
                elif k == 'description':
                    c.us_description = db.Text(v)
                elif k == 'location':
                    for value in v:
                        if 'city' in value:
                            c.us_city = str(value['city'])
                        if 'state' in value:
                            c.us_state = str(value['state'])
                        if 'country' in value:
                            c.us_country = str(value['country'])
                        if 'latitude' in value:
                            c.us_latitude = str(value['latitude'])
                        if 'longitude' in value:
                            c.us_longitude = str(value['longitude'])
                # TODO: images
                # TODO: maps
                # TODO: videos
                # TODO: social
                # TODO: citations
                # TODO: external links
                elif k == 'start-date':
                    c.us_startDate = datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S').date()
                elif k == 'end-date':
                    c.us_endDate = datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S').date()
                elif k == 'economic-impact':
                    stats = []
                    for statistic in v:
                        stats.append(statistic['statistic'])
                    c.us_economicImpact = stats
                elif k == 'human-impact':
                    stats = []
                    for statistic in v:
                        stats.append(statistic['statistic'])
                    c.us_humanImpact = stats
                elif k == 'resources-needed':
                    res = []
                    for resource in v:
                        res.append(resource['resource'])
                    c.us_resoucesNeeded = res
                elif k == 'ways-to-help':
                    ways = []
                    for way in v:
                        ways.append(way['way'])
                    c.us_waysToHelp = ways
    print c



def process_organizations(element):
    for i in element.iter():
        print(i)

def process_people(element):
    for i in element:
        print(i)

process(tree)
