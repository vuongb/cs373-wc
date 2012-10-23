from minixsv import pyxsval as xsv
import xml.etree.ElementTree as ET


SCHEMA='cassie-schema-statistics.xsd'

#tree = ET.parse('crisis-breast_cancer.xml')
#root = tree.getroot()
#print(root.tag, root.attrib)

def parse_xml(data, schema):
    try:
        wrapper = xsv.parseAndValidateXmlInput(data, schema, xmlIfClass=xsv.XMLIF_ELEMENTTREE)
        tree = wrapper.getTree()
        root = tree.getroot()
               

    except xsv.XsvalError as e:
        print("XML did not validate\n"+str(e))


parse_xml('crisis-breast_cancer.xml', SCHEMA)