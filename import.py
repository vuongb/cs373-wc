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
    root = tree.getroot()

    print(str(root.tag))
    if str(root.tag) == 'world-crises':
        process(root.getroot())
    elif str(root.tag) == 'crises':
        process_crises(root.gettree())
    elif str(root.tag) == 'organizations':
        process_organizations(root.gettree())
    elif str(root.tag) == 'people':
        process_people(root.gettree())

def process_crises(tree):
    root = tree.getroot()
    print(root)

def process_organizations(tree):
    root = tree.getroot()
    print(root)

def process_people(tree):
    root = tree.getroot()
    print(root)

process(tree)
