import unittest
from Models import Crisis, Organization, Person

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

import unittest
import logging
from Models import Organization, Crisis, Person
from merge import merge


class TestMerge(unittest.TestCase):
    def setUp(self):
        ## different orgs
        self.organization_a = Organization(
            us_id='ot_id',
            us_name='testOrganization',
            us_type='testOrgType',
            us_description='testOrg Description',
            us_city='testCity',
            us_state='testState',
            us_country='testCountry'
        ).put()
        self.organization_b = Organization(
            us_id='ot_id',
            us_name='a different Org',
            us_type='another type',
            us_description='Add to description',
            us_city='Austin',
            us_state='TX',
            us_country='Uganda'
        ).put()

        ## identical orgs
        self.organization_a = Organization(
            us_id='ot_same',
            us_name='testOrganization',
            us_type='testOrgType',
            us_description='testOrg Description',
            us_city='testCity',
            us_state='testState',
            us_country='testCountry'
        ).put()
        self.organization_a = Organization(
            us_id='ot_same',
            us_name='testOrganization',
            us_type='testOrgType',
            us_description='testOrg Description',
            us_city='testCity',
            us_state='testState',
            us_country='testCountry'
        ).put()

        ## different crises
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
        ).put()
        self.crisis_model = Crisis(
            us_id='ct_id',
            us_name='Some Other crisis of a different name',
            us_type='Another type',
            us_description='additional description',
            us_city='Austin',
            us_country='USA',
            us_state='Texas',
            us_economicImpact=5689,
            us_resoucesNeeded=['water', 'clothes'],
            us_waysToHelp=['way3', 'way4']
        ).put()

        ## identical crises
        self.crisis_model = Crisis(
            us_id='ct_same',
            us_name='testCrisis',
            us_type='testCrisisType',
            us_description='testCrisis Description',
            us_city='testCity',
            us_country='testCountry',
            us_state='testState',
            us_economicImpact=1234,
            us_resoucesNeeded=['food', 'donations'],
            us_waysToHelp=['way1', 'way2']
        ).put()
        self.crisis_model = Crisis(
            us_id='ct_same',
            us_name='testCrisis',
            us_type='testCrisisType',
            us_description='testCrisis Description',
            us_city='testCity',
            us_country='testCountry',
            us_state='testState',
            us_economicImpact=1234,
            us_resoucesNeeded=['food', 'donations'],
            us_waysToHelp=['way1', 'way2']
        ).put()

        ## different people
        self.person_model = Person(
            us_id='op_id',
            us_name='testPerson',
            us_type='testPersonType',
            us_description='testPerson Description',
            us_city='testCity',
            us_state='testState',
            us_country='testCountry'
        ).put()
        self.person_model = Person(
            us_id='op_id',
            us_name='Nickname',
            us_type='Dude',
            us_description='Dude abides',
            us_city='New York',
            us_state='New York',
            us_country='USA'
        ).put()

        ## identical people
        self.person_model = Person(
            us_id='op_same',
            us_name='Nickname',
            us_type='Dude',
            us_description='Dude abides',
            us_city='New York',
            us_state='New York',
            us_country='USA'
        ).put()
        self.person_model = Person(
            us_id='op_same',
            us_name='Nickname',
            us_type='Dude',
            us_description='Dude abides',
            us_city='New York',
            us_state='New York',
            us_country='USA'
        ).put()

    ##################################################################################

    def test_merge_org_1(self):
        """ should show all differing data when orgs are merged
        """
        result = merge('ot_id', "Organization")
        self.assertEqual(result,
            {'Related People': '<ul></ul>',
             'Kind': u'testOrgType, another type',
             'Alternate Names': u'a different Org',
             'Related Crises': '<ul></ul>',
             'Maps': '<ul class="unstyled"><li><iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.com/maps?q=testCity, testState, testCountry&amp;output=embed"></iframe></li><br /><li><iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.com/maps?q=Austin, TX, Uganda&amp;output=embed"></iframe></li><br /></ul>',
             'Citations': '<ul></ul>',
             'External Links': '<ul></ul>',
             'Location': 'testCity, testState, testCountry<br />\nAustin, TX, Uganda<br />',
             'Social': '<ul class="unstyled"></ul>',
             'Images': '<ul class="thumbnails"></ul>',
             'Name': u'testOrganization',
             'Description': u'testOrg Description<p /><p />Add to description'}
        )

    def test_merge_org_2(self):
        """ should not alter results when duplicate orgs is merged
        """
        result = merge('ot_same', "Organization")
        self.assertEqual(result,
            {'Related People': '<ul></ul>',
             'Kind': u'testOrgType',
             'Alternate Names': u'testOrganization',
             'Related Crises': '<ul></ul>',
             'Maps': '<ul class="unstyled"><li><iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.com/maps?q=testCity, testState, testCountry&amp;output=embed"></iframe></li><br /></ul>',
             'Citations': '<ul></ul>',
             'External Links': '<ul></ul>',
             'Location': 'testCity, testState, testCountry<br />',
             'Social': '<ul class="unstyled"></ul>',
             'Images': '<ul class="thumbnails"></ul>',
             'Name': u'testOrganization',
             'Description': u'testOrg Description'}
        )

    def test_merge_crisis_1(self):
        """
        should merge all differing data when merging crises of one id
        """
        result = merge('ct_id', "Crisis")
        self.assertEqual(result,
            {'Related Organizations': '<ul></ul>',
             'Related People': '<ul></ul>',
             'Kind': u'testCrisisType, Another type',
             'Alternate Names': u'Some Other crisis of a different name',
             'Resources Needed': '',
             'Ways To Help': u'way3, way4',
             'Economic Impact': '5689',
             'Maps': '<ul class="unstyled"><li><iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.com/maps?q=testCity, testState, testCountry&amp;output=embed"></iframe></li><br /><li><iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.com/maps?q=Austin, Texas, USA&amp;output=embed"></iframe></li><br /></ul>',
             'Citations': '<ul></ul>',
             'External Links': '<ul></ul>',
             'Location': 'testCity, testState, testCountry<br />\nAustin, Texas, USA<br />',
             'Social': '<ul class="unstyled"></ul>',
             'Images': '<ul class="thumbnails"></ul>',
             'Name': u'testCrisis',
             'Description': u'testCrisis Description<p /><p />additional description'}
        )

    def test_merge_crisis_2(self):
        """
        should not alter final result when merging two identical crises
        """
        result = merge('ct_same', "Crisis")
        self.assertEqual(result,
            {'Related Organizations': '<ul></ul>',
             'Related People': '<ul></ul>',
             'Kind': u'testCrisisType',
             'Alternate Names': u'testCrisis',
             'Resources Needed': '',
             'Ways To Help': u'way1, way2',
             'Economic Impact': '1234',
             'Maps': '<ul class="unstyled"><li><iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.com/maps?q=testCity, testState, testCountry&amp;output=embed"></iframe></li><br /></ul>',
             'Citations': '<ul></ul>',
             'External Links': '<ul></ul>',
             'Location': 'testCity, testState, testCountry<br />',
             'Social': '<ul class="unstyled"></ul>',
             'Images': '<ul class="thumbnails"></ul>',
             'Name': u'testCrisis',
             'Description': u'testCrisis Description'}
        )

    def test_merge_person_1(self):
        """
        should merge all differing data when merging people of one id
        """
        result = merge('op_id', "Person")
        self.assertEqual(result,
            {'Related Organizations': '<ul></ul>',
             'Kind': u'testPersonType, Dude',
             'Alternate Names': u'Nickname',
             'Related Crises': '<ul></ul>',
             'Maps': '<ul class="unstyled"><li><iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.com/maps?q=testCity, testState, testCountry&amp;output=embed"></iframe></li><br /><li><iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.com/maps?q=New York, New York, USA&amp;output=embed"></iframe></li><br /></ul>',
             'Citations': '<ul></ul>',
             'External Links': '<ul></ul>',
             'Location': 'testCity, testState, testCountry<br />\nNew York, New York, USA<br />', 'Social': '<ul class="unstyled"></ul>',
             'Images': '<ul class="thumbnails"></ul>',
             'Name': u'testPerson',
             'Description': u'testPerson Description<p /><p />Dude abides'}
        )

    def test_merge_person_2(self):
        """
        should not alter final result when merging two identical people
        """
        result = merge('op_same', 'Person')
        self.assertEqual(result,
            {'Related Organizations': '<ul></ul>',
             'Kind': u'Dude',
             'Alternate Names': u'Nickname',
             'Related Crises': '<ul></ul>',
             'Maps': '<ul class="unstyled"><li><iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.com/maps?q=New York, New York, USA&amp;output=embed"></iframe></li><br /></ul>',
             'Citations': '<ul></ul>',
             'External Links': '<ul></ul>',
             'Location': 'New York, New York, USA<br />',
             'Social': '<ul class="unstyled"></ul>',
             'Images': '<ul class="thumbnails"></ul>',
             'Name': u'Nickname',
             'Description': u'Dude abides'}
        )

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

import unittest
from exporter import buildTree, addCrisis, addOrganization, addPerson
from WC3 import get_tree_and_validate
from google.appengine.ext import db
import importer

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
        assert root.getchildren()[0].getchildren()[0].attrib['id'] == 'c-test_crisis'
        assert root.getchildren()[1].getchildren()[0].attrib['id'] == 'o-test_org'
        assert root.getchildren()[2].getchildren()[0].attrib['id'] == 'p-algore'

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
                {'images': [{'image':
                                 [{'source': u'http://www.testimage.com'},
                                  {'description': u'Description of TestImage'}]}]},
                {'maps': [{'map':
                               [{'source': u'http://maps.google.com'},
                                {'description': u'Map Description'}]}]},
                {'videos': [{u'youtube': u'r_8om4dsEmw'}]},
                {'social': [{u'twitter': u'@billgates'}]},
                {'citations': [{'citation':
                                    [{'source': u'http://maps.google.com'},
                                     {'description': u'Map Description'}]}]},
                {'external-links':
                     [{'external-link':
                           [{'source': u'http://www.google.com'},
                            {'description': u'Google'}]},
                      {'external-link':
                           [{'source': u'http://www.yahoo.com'},
                            {'description': u'Yahoo'}]}]},
                {'start-date': '1776-07-04T00:00:00'},
                {'end-date': '1776-07-04T00:00:00'},
                {'human-impact': [{'deaths': '12345'}]},
                {'economic-impact': '1234567890'},
                {'resources-needed':
                     [{'resource': u'money'},
                      {'resource': u'donations'}]},
                {'ways-to-help':
                     [{'way': u'donations'},
                      {'way': u'volunteering'}]}] in crisis_d.values()

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
