import unittest
from importer import get_tree_and_validate
import search
import importer

class TestImport(unittest.TestCase):
    def setUp(self):
        self.crisis_xml  = open('test/test_crisis.xml', 'r').read()
        self.invalid_xml = open('test/test_invalid.xml', 'r').read()
        self.org_xml     = open('test/test_organization.xml', 'r').read()
        self.person_xml  = open('test/test_person.xml', 'r').read()
        self.wc2_xml     = open('WC2.xml', 'r').read()

        self.SCHEMA      = 'WC2.xsd'
        self.crisis_tree = get_tree_and_validate(self.crisis_xml, open(self.SCHEMA, 'r').read())
        self.org_tree    = get_tree_and_validate(self.org_xml, open(self.SCHEMA, 'r').read())
        self.person_tree = get_tree_and_validate(self.person_xml, open(self.SCHEMA, 'r').read())
        self.wc2_tree    = get_tree_and_validate(self.wc2_xml, open(self.SCHEMA, 'r').read())

    ##################################################################################

    def test_validate_valid_crisis(self):
        """valid crisis xml should validate
        """
        assert self.crisis_tree != 0

    def test_validate_valid_org(self):
        """valid organization xml should validate
        """
        assert self.org_tree != 0

    def test_validate_valid_person(self):
        """valid organization xml should validate
        """
        assert self.person_tree != 0

    def test_validate_invalid(self):
        """invalid xml should not validate
        """
        self.assertEqual(get_tree_and_validate(self.invalid_xml, open(self.SCHEMA, 'r').read()), 0)

    def test_validate_wc3(self):
        """WC2 XML should validate"""
        assert self.wc2_tree != 0

    def test_etree_to_dict(self):
        """ElementTree should fully convert to dict
        """
        person_d = importer.etree_to_dict(self.person_tree.getroot())
        assert person_d == {
            'world-crises': [
                {'crises': []},
                {'organizations': []},
                {'people': [
                    {'person': [
                        {'name': 'Bob TestPerson'},
                        {'alternate-names': 'TestDude'},
                        {'kind': 'TestPersonKind'},
                        {'description': 'PersonTestDescription'},
                        {'location': [
                            {'city': 'Test Person City'},
                            {'country': 'United States'}]},
                        {'images': [
                            {'image': [
                                {'source': 'http://www.testimage.com'},
                                {'description': 'Description of TestImage'}]}]},
                        {'maps': [
                            {'map': [
                                {'source': 'http://maps.google.com'},
                                {'description': 'Map Description'}]}]},
                        {'videos': [{'youtube': 'r_8om4dsEmw'}]},
                        {'social': [{'twitter': '@billgates'}]},
                        {'citations': [
                            {'citation': [
                                {'source': 'http://en.wikipedia.org/wiki/Test'},
                                {'description': 'Wiki'}]}]},
                        {'external-links': [
                            {'external-link': [
                                {'source': 'http://www.zombo.com/'},
                                {'description': 'Test Link'}]}]}],
                     'id': 'p-algore'}]}]}

    def test_import_crisis(self):
        """should import a crisis"""
        tree = self.crisis_tree
        root = tree.getroot()
        assert importer.put_objects(root) == True

    def test_import_organization(self):
        """should import a organization"""
        tree = self.org_tree
        root = tree.getroot()
        assert importer.put_objects(root) == True
#
    def test_import_person(self):
        """should import a person"""
        tree = self.person_tree
        root = tree.getroot()
        assert importer.put_objects(root) == True
#
    def test_import_wc2(self):
        """should import our site schema instance"""
        tree = self.wc2_tree
        root = tree.getroot()
        assert importer.put_objects(root) == True
