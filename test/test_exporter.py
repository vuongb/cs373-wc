import unittest
from WC1 import get_tree_and_validate, etree_to_dict, store_special_classes
import importer

class TestImport(unittest.TestCase):
    def setUp(self):
        self.crisis_xml = open('test/test_crisis.xml', 'r').read()
        self.invalid_xml = open('test/test_invalid.xml', 'r').read()
        #        self.org_xml    = open('test/organization-oxfam.xml', 'r').read()
        #        self.person_xml = open('test/person-bono.xml', 'r').read()

        self.SCHEMA = 'WC2.xsd'
        self.crisis_tree = get_tree_and_validate(self.crisis_xml, open(self.SCHEMA, 'r').read())
    #        self.org_tree = get_tree_and_validate(self.org_xml, open(self.SCHEMA, 'r').read())
    #        self.person_tree = get_tree_and_validate(self.person_xml, open(self.SCHEMA, 'r').read())

    ##################################################################################

    def test_buildTree(self):
        pass

    def test_addCrisis(self):
        pass

    def test_addOrganization(self):
        pass

    def test_addPerson(self):
        pass