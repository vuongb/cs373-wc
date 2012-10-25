import unittest
import datetime
from google.appengine.ext import db
import xml.etree.ElementTree as ETree
from WC1 import get_tree_and_validate, etree_to_dict, store_special_classes
import importer
import Models

class TestImport(unittest.TestCase):
    def setUp(self):
        self.crisis_xml = open('test/crisis-breast_cancer.xml', 'r').read()
        self.org_xml    = open('test/organization-oxfam.xml', 'r').read()
        self.person_xml = open('test/person-bono.xml', 'r').read()

        self.SCHEMA = 'unicornSteroids.xsd'


        self.crisis_tree = get_tree_and_validate(self.crisis_xml, open(self.SCHEMA, 'r').read())
        self.org_tree = get_tree_and_validate(self.org_xml, open(self.SCHEMA, 'r').read())
        self.person_tree = get_tree_and_validate(self.person_xml, open(self.SCHEMA, 'r').read())


    ##################################################################################

    def test_valid_schema(self):
        assert self.crisis_tree
        assert self.org_tree
        assert self.person_tree

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
                        store_special_classes(result_dict, crisis)
            elif i.tag == 'organizations':
                # iterate through all organizations
                d = etree_to_dict(i)
                for o in d.get('organizations'):
                    if type(o) != str:
                        result_dict     = importer.process_organization(o)
                        organization    = result_dict.get('organization')
                        organization.put()
                        store_special_classes(result_dict, organization)
            elif i.tag == 'people':
                # iterate through all person
                d = etree_to_dict(i)
                for p in d.get('people'):
                    if type(p) != str:
                        result_dict     = importer.process_person(p)
                        person          = result_dict.get('person')
                        person.put()
                        store_special_classes(result_dict, person)

    def test_upload_org(self):
        tree = self.org_tree

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
                        store_special_classes(result_dict, crisis)
            elif i.tag == 'organizations':
                # iterate through all organizations
                d = etree_to_dict(i)
                for o in d.get('organizations'):
                    if type(o) != str:
                        result_dict     = importer.process_organization(o)
                        organization    = result_dict.get('organization')
                        organization.put()
                        store_special_classes(result_dict, organization)
            elif i.tag == 'people':
                # iterate through all person
                d = etree_to_dict(i)
                for p in d.get('people'):
                    if type(p) != str:
                        result_dict     = importer.process_person(p)
                        person          = result_dict.get('person')
                        person.put()
                        store_special_classes(result_dict, person)

    def test_upload_person(self):
        tree = self.person_tree

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
                        store_special_classes(result_dict, crisis)
            elif i.tag == 'organizations':
                # iterate through all organizations
                d = etree_to_dict(i)
                for o in d.get('organizations'):
                    if type(o) != str:
                        result_dict     = importer.process_organization(o)
                        organization    = result_dict.get('organization')
                        organization.put()
                        store_special_classes(result_dict, organization)
            elif i.tag == 'people':
                # iterate through all person
                d = etree_to_dict(i)
                for p in d.get('people'):
                    if type(p) != str:
                        result_dict     = importer.process_person(p)
                        person          = result_dict.get('person')
                        person.put()
                        store_special_classes(result_dict, person)