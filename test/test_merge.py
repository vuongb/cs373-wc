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