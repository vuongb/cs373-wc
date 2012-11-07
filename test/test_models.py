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