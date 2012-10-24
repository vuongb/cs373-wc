from minixsv import pyxsval as xsv
import xml.etree.ElementTree as ET
from Models import Crisis


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

def process_crises(element):
    # Iterates through all crises
    dict = etree_to_dict(element)
    # for all crises
    for crisis in dict.get('crises'):
        print crisis
        c = Crisis
        # iterates through list of dictionaries
        for attribute_dictionary in crisis['crisis']:
            # iterates through attribute dictionary
            print "attribute dictionary: " + str(attribute_dictionary)
            for k,v in attribute_dictionary.items():
                print "k: " + str(k)
                print "v: " + str(v)
                # set attributes of crisis class and prepend 'us_' to field names
                setattr(c, "us_" + str(k), v)
        print crisis
    print
    print
    print
    print Crisis


def process_organizations(element):
    for i in element.iter():
        print(i)

def process_people(element):
    for i in element:
        print(i)

process(tree)
