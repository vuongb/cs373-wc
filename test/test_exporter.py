import logging
import unittest
from google.appengine.ext import db
import xml.etree.ElementTree as ETree
from Models import *
from WC1 import get_tree_and_validate
from exporter import *

class TestExport(unittest.TestCase):
    def setUp(self):
        self.person_obj = Person(us_name='test name', us_type='test type', us_description='test description', us_country='USA')
        self.crisis_obj = Crisis(us_name='test namec', us_type='test typec', us_description='test descriptionc', us_economicImpact=['$3'], us_humanImpact=['39'], us_resoucesNeeded=['gold'], us_waysToHelp=['donate'])
        self.org_obj    = Organization(us_name='test nameo', us_type='test typeo', us_description='test descriptiono', us_country='USA', us_email='bob@org.com')

        addPerson(self.person_obj, 0)
        addCrisis(self.crisis_obj, 0)
        addOrganization(self.org_obj, 0)

        self.tree = buildTree()
        self.xml_tree = ETree.tostring(self.tree)

    def test_export(self):
        assert self.xml_tree