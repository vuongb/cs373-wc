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

def process(tree):
    '''
    go through elementtree and create objects from elements
    '''
    root = tree.getroot()
    for i in root:
        if i.tag == 'crises':
            process_crises(i)
        elif i.tag == 'organizations':
            process_organizations(i)
        elif i.tag == 'people':
            process_people(i)

def process_crises(element):
    for i in element:
        pass

def process_organizations(element):
    root = tree.getroot()
    print(root)

def process_people(element):
    root = tree.getroot()
    print(root)

process(tree)
