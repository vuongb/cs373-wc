import unittest
from google.appengine.ext import db
from Models import Crisis, Organization, Person
from WC3 import get_tree_and_validate, etree_to_dict
from exporter import buildTree, addCrisis, addOrganization, addPerson
import importer

class TestImport(unittest.TestCase):
    def setUp(self):
        self.crisis_xml  = open('test/test_crisis.xml', 'r').read()
        self.invalid_xml = open('test/test_invalid.xml', 'r').read()
        self.org_xml     = open('test/test_organization.xml', 'r').read()
        self.person_xml  = open('test/test_person.xml', 'r').read()
        self.wc2_xml     = open('WC3.xml', 'r').read()

        self.SCHEMA      = 'WC3.xsd'
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

    def test_validate_wc2(self):
        """WC2 XML should validate"""
        assert self.wc2_tree != 0

    def test_etree_to_dict(self):
        """ElementTree should fully convert to dict
        """
        person_d = etree_to_dict(self.person_tree.getroot())
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


class TestExport(unittest.TestCase):
    def setUp(self):
    #        self.wc2_xml = open('WC3.xml', 'r').read()

        self.SCHEMA = 'WC3.xsd'
        self.crisis_tree = get_tree_and_validate(open('test/test_crisis.xml', 'r').read(),
            open(self.SCHEMA, 'r').read())
        self.organization_tree = get_tree_and_validate(open('test/test_organization.xml', 'r').read(),
            open(self.SCHEMA, 'r').read())
        self.person_tree = get_tree_and_validate(open('test/test_person.xml', 'r').read(),
            open(self.SCHEMA, 'r').read())

        importer.put_objects(self.crisis_tree.getroot())
        importer.put_objects(self.organization_tree.getroot())
        importer.put_objects(self.person_tree.getroot())

    ##################################################################################

    def test_buildTree(self):
        """should build Element Tree pulled from imported elements"""
        root = buildTree()
        assert root.getchildren()[0].getchildren()[0].attrib['id'] == 'c1'
        assert root.getchildren()[1].getchildren()[0].attrib['id'] == 'o9'
        assert root.getchildren()[2].getchildren()[0].attrib['id'] == 'p16'

    def test_addCrisis(self):
        """should build Element Tree pulled from imported Crisis"""
        #fetch the object from the datastore
        crises_obj = db.GqlQuery("SELECT * FROM Crisis")
        crisis = addCrisis(crises_obj.run().next())
        #view it as a dict
        crisis_d = importer.etree_to_dict(crisis)
        assert [{'name': u'Test Crisis'},
                {'kind': u'TestKind'},
                {'description': u'Description of test crisis'},
                {'location': [{'country': u'USA'}]},
                {'images': [
                    {'image': [{'source': u'http://www.testimage.com'},
                               {'description': u'Description of TestImage'}]}]},
                {'maps': [{'map': [{'source': u'http://maps.google.com'}, {'description': u'Map Description'}]}]},
                {'videos': [{u'youtube': u'r_8om4dsEmw'}]}, {'social': [{u'twitter': u'@billgates'}]},
                {'citations': [
                    {'citation': [{'source': u'http://maps.google.com'}, {'description': u'Map Description'}]}]},
                {'external-links': [
                    {'external-link': [{'source': u'http://www.google.com'}, {'description': u'Google'}]},
                    {'external-link': [{'source': u'http://www.yahoo.com'}, {'description': u'Yahoo'}]}]},
                {'start-date': '1776-07-04T00:00:00'},
                {'end-date': '1776-07-04T00:00:00'},
                {'human-impact': [{'deaths': '12345'}]},
                {'economic-impact': '1234567890'},
                {'resources-needed': []},
                {'ways-to-help': [{'way': u'donations'}, {'way': u'volunteering'}]}] in crisis_d.values()

    def test_addOrganization(self):
        """should build element tree pulled from imported Organization"""
        #fetch the object form the datastore
        org_obj = db.GqlQuery("SELECT * FROM Organization")
        organization = addOrganization(org_obj.run().next())
        #view it as a dict
        organization_d = importer.etree_to_dict(organization)
        assert [{'name': u'Test Organization'},
                {'kind': u'TestOrgKind'},
                {'description': u'TestOrgDescription'},
                {'location': [{'city': u'Organization City'}, {'country': u'USA'}]},
                {'images': [
                    {'image': [
                        {'source': u'http://www.testimage.com'},
                        {'description': u'Description of TestImage'}]}]},
                {'maps': [
                    {'map': [{'source': u'http://maps.google.com'}, {'description': u'Map Description'}]}]},
                {'videos': [{u'youtube': u'r_8om4dsEmw'}]},
                {'social': [{u'twitter': u'@billgates'}]},
                {'citations': [
                    {'citation': [
                        {'source': u'http://maps.google.com'},
                        {'description': u'Map Description'}]}]},
                {'external-links': [
                    {'external-link': [
                        {'source': u'http://www.google.com'},
                        {'description': u'Google'}]}]}] in organization_d.values()

    def test_addPerson(self):
        """should build element tree pulled from imported Person"""
        person_obj = db.GqlQuery("SELECT * FROM Person")
        person = addPerson(person_obj.run().next())
        person_d = importer.etree_to_dict(person)
        assert [{'name': u'Bob TestPerson'},
                {'alternate-names': u'TestDude'},
                {'kind': u'TestPersonKind'},
                {'description': u'PersonTestDescription'},
                {'location': [{'city': u'Test Person City'}, {'country': u'United States'}]},
                {'images': [
                    {'image': [{'source': u'http://www.testimage.com'}, {'description': u'Description of TestImage'}]}]},
                {'maps': [{'map': [{'source': u'http://maps.google.com'}, {'description': u'Map Description'}]}]},
                {'videos': [{u'youtube': u'r_8om4dsEmw'}]},
                {'social': [{u'twitter': u'@billgates'}]},
                {'citations': [
                    {'citation': [{'source': u'http://maps.google.com'}, {'description': u'Map Description'}]}]},
                {'external-links': [
                    {'external-link': [{'source': u'http://www.zombo.com/'}, {'description': u'Test Link'}]}]}] in person_d.values()

class TestModels(unittest.TestCase):
    """Unit tests of Model helper methods"""

    def setUp(self):
        self.crisis_model = Crisis(
            us_id='ct_id',
            us_name='testCrisis',
            us_type='testCrisisType',
            us_description='testCrisis Description',
            us_city='testCity',
            us_country='testCountry',
            us_state='testState',
            us_economicImpact=1234,
            us_resoucesNeeded=['food', 'donations'],
            us_waysToHelp=['way1', 'way2']
        )
        self.organization_model = Organization(
            us_id='ot_id',
            us_name='testOrganization',
            us_type='testOrgType',
            us_description='testOrg Description',
            us_city='testCity',
            us_state='testState',
            us_country='testCountry'
        )
        self.person_model = Person(
            us_id='op_id',
            us_name='testPerson',
            us_type='testPersonType',
            us_description='testPerson Description',
            us_city='testCity',
            us_state='testState',
            us_country='testCountry'
        )

        self.crisis_model.put()
        self.organization_model.put()
        self.person_model.put()

    def test_getUrl_c(self):
        assert self.crisis_model.getUrl() == '/c/1'

    def test_getUrl_o(self):
        assert self.organization_model.getUrl() == '/o/2'

    def test_getUrl_p(self):
        assert self.person_model.getUrl() == '/p/3'

    def test_getLocation_c(self):
        assert self.crisis_model.getLocation() == 'testCity, testState, testCountry'

    def test_getLocation_o(self):
        assert self.organization_model.getLocation() == 'testCity, testState, testCountry'

    def test_getLocation_p(self):
        assert self.person_model.getLocation() == 'testCity, testState, testCountry'
