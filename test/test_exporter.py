import unittest
import logging
from xml.etree.ElementTree import Element
from WC1 import get_tree_and_validate
from exporter import buildTree, addCrisis, addOrganization, addPerson
from google.appengine.ext import db
import importer

class TestExport(unittest.TestCase):
    def setUp(self):
        self.wc2_xml = open('WC2.xml', 'r').read()

        self.SCHEMA = 'WC2.xsd'
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
        root = buildTree()
        assert root.getchildren()[0].getchildren()[0].attrib['id'] == 'c1'
        assert root.getchildren()[1].getchildren()[0].attrib['id'] == 'o2'
        assert root.getchildren()[2].getchildren()[0].attrib['id'] == 'p3'

    def test_addCrisis(self):
        #fetch the object from the datastore
        crises_obj = db.GqlQuery("SELECT * FROM Crisis")
        crisis = addCrisis(crises_obj.run().next(), 1)
        #view it as a dict
        crisis_d = importer.etree_to_dict(crisis)
        assert crisis_d == {
            'crisis': [{'name': u'Test Crisis'},
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
                       {'resources-needed': None},
                       {'ways-to-help': [{'way': u'donations'}, {'way': u'volunteering'}]}]}

    def test_addOrganization(self):
        #fetch the object form the datastore
        org_obj = db.GqlQuery("SELECT * FROM Organization")
        organization = addOrganization(org_obj.run().next(), 1)
        #view it as a dict
        organization_d = importer.etree_to_dict(organization)
        assert organization_d == {
            'organization': [{'name': u'Test Organization'},
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
                                        {'description': u'Google'}]}]}]}

    def test_addPerson(self):
        person_obj = db.GqlQuery("SELECT * FROM Person")
        person = addPerson(person_obj.run().next(), 1)

        person_d = importer.etree_to_dict(person)
        assert person_d == {
            'person': [
                {'name': u'Bob TestPerson'},
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
                    {'external-link': [{'source': u'http://www.zombo.com/'}, {'description': u'Test Link'}]}]}]}