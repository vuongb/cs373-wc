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

    def test_validate_valid(self):
        """valid xml should validate
        """
        assert self.crisis_tree

    def test_validate_invalid(self):
        """invalid xml should not validate
        """
        self.assertEqual(get_tree_and_validate(self.invalid_xml, open(self.SCHEMA, 'r').read()), 0)

    def test_etree_to_dict(self):
        """
        """



    def test_upload_crisis(self):
        tree = self.crisis_tree
        root = tree.getroot()
        for i in root.iter():
            if i.tag == 'crises':
                # iterate through all crises
                d = etree_to_dict(i)

                for c in d.get('crises'):
                    if type(c) != str:
                        result_dict     = importer.process_crisis(c)
                        crisis          = result_dict.get('crisis')
                        crisis.put()