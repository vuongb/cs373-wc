from minixsv import pyxsval as xsv
import xml.etree.ElementTree as ET


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
    d = {t.tag : map(etree_to_dict, t.getchildren())}
    d.update(('@' + k, v) for k, v in t.attrib.iteritems())
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
    print etree_to_dict(element)
    '''
    returns a dict of the element tree
    '''
    for i in element.iter():
        tag = i.tag
        attrib = i.attrib
        for key, value in attrib.items():
            print(str(key) + " " + str(value))

def process_organizations(element):
    for i in element.iter():
        print(i)

def process_people(element):
    for i in element:
        print(i)

process(tree)
