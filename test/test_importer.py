import unittest
import datetime
from google.appengine.ext import db
import xml.etree.ElementTree as ETree
import importer
import Models

class TestImport(unittest.TestCase):
    def setUp(self):
        importer.importer(
            '''<world-crises>
    <crises>
	<crisis id="c-id">
	    <name>name</name>
	    <alternate-names>
		<alternate-name>name1</alternate-name>
		<alternate-name>name2</alternate-name>
	    </alternate-names>
	    <kind>kind</kind>
	    <description>long description</description>
	    <location>
		<city>city</city>
		<state>ST</state>
		<country>country</country>
		<latitude>1.23456</latitude>
		<longitude>1.23456</longitude>
	    </location>
	    <images>
		<image>
		    <source>http://www.images.com/random.jpg</source>
		    <description>image des</description>
		</image>
	    </images>
	    <maps>
		<map>
		    <source>http://www.maps.com/map</source>
		    <description>map des</description>
		</map>
	    </maps>
	    <videos>
		<youtube>youtube</youtube>
		<vimeo>12345</vimeo>
	    </videos>
	    <social>
		<facebook>facebookusername</facebook>
		<twitter>@twittername</twitter>
		<twitter>#twitterhashtag</twitter>
		<youtube>youtubeusername</youtube>
	    </social>
	    <citations>
		<citation>
		    <source>http://www.wikipedia.org/</source>
		    <description>citation des</description>
		</citation>
	    </citations>
	    <external-links>
		<external-link>
		    <source>http://www.somecoolplace.org/</source>
		    <description>link des</description>
		</external-link>
	    </external-links>
	    <start-date>2012-10-24T20:00:00</start-date>
	    <human-impact>
		<statistic>1000 people</statistic>
	    </human-impact>
	    <economic-impact>
		<statistic>$1000</statistic>
	    </economic-impact>
	    <resources-needed>
		<resource>resource</resource>
	    </resources-needed>
	    <ways-to-help>
		<way>way</way>
	    </ways-to-help>
	    <organization-refs>o-id</organization-refs>
	    <person-refs>p-id</person-refs>
	</crisis>
    </crises>
    <organizations>
	<organization id="o-id">
	    <name>name</name>
	    <alternate-names>
		<alternate-name>name1</alternate-name>
		<alternate-name>name2</alternate-name>
	    </alternate-names>
	    <kind>kind</kind>
	    <description>long description</description>
	    <location>
		<city>city</city>
		<state>ST</state>
		<country>country</country>
		<latitude>1.23456</latitude>
		<longitude>1.23456</longitude>
	    </location>
	    <images>
		<image>
		    <source>http://www.images.com/random.jpg</source>
		    <description>image des</description>
		</image>
	    </images>
	    <maps>
		<map>
		    <source>http://www.maps.com/map</source>
		    <description>map des</description>
		</map>
	    </maps>
	    <videos>
		<youtube>youtube</youtube>
		<vimeo>12345</vimeo>
	    </videos>
	    <social>
		<facebook>facebookusername</facebook>
		<twitter>@twittername</twitter>
		<twitter>#twitterhashtag</twitter>
		<youtube>youtubeusername</youtube>
	    </social>
	    <citations>
		<citation>
		    <source>http://www.wikipedia.org/</source>
		    <description>citation des</description>
		</citation>
	    </citations>
	    <external-links>
		<external-link>
		    <source>http://www.somecoolplace.org/</source>
		    <description>link des</description>
		</external-link>
	    </external-links>
	    <address>
		address
		city, st zipcode
	    </address>
	    <email>email@name.org</email>
	    <phone>123 456 - 7890</phone>
	    <crisis-refs>c-id</crisis-refs>
	    <person-refs>p-id</person-refs>
	</organization>
    </organizations>
    <people>
	<person id="p-id">
	    <name>name</name>
	    <alternate-names>
		<alternate-name>name1</alternate-name>
		<alternate-name>name2</alternate-name>
	    </alternate-names>
	    <kind>kind</kind>
	    <description>long description</description>
	    <location>
		<city>city</city>
		<state>ST</state>
		<country>country</country>
		<latitude>1.23456</latitude>
		<longitude>1.23456</longitude>
	    </location>
	    <images>
		<image>
		    <source>http://www.images.com/random.jpg</source>
		    <description>image des</description>
		</image>
	    </images>
	    <maps>
		<map>
		    <source>http://www.maps.com/map</source>
		    <description>map des</description>
		</map>
	    </maps>
	    <videos>
		<youtube>youtube</youtube>
		<vimeo>12345</vimeo>
	    </videos>
	    <social>
		<facebook>facebookusername</facebook>
		<twitter>@twittername</twitter>
		<twitter>#twitterhashtag</twitter>
		<youtube>youtubeusername</youtube>
	    </social>
	    <citations>
		<citation>
		    <source>http://www.wikipedia.org/</source>
		    <description>citation des</description>
		</citation>
	    </citations>
	    <external-links>
		<external-link>
		    <source>http://www.somecoolplace.org/</source>
		    <description>link des</description>
		</external-link>
	    </external-links>
	    <crisis-refs>c-id</crisis-refs>
	    <person-refs>p-id</person-refs>
	</person>
    </people>
</world-crises>''')

        self.crisis = db.Query(Models.Crisis).get()
        self.org = db.Query(Models.Organization).get()
        self.person = db.Query(Models.Person).get()

        self.co = db.Query(Models.CrisisOrganization).get()
        self.cp = db.Query(Models.CrisisPerson).get()
        self.op = db.Query(Models.OrganizationPerson).get()

    ##################################################################################

    def test_upload_crisis(self):
        # Base Data
        self.assertEqual('name', self.crisis.us_name)
        self.assertEqual(['name1', 'name2'], self.crisis.us_alternateNames)
        self.assertEqual('kind', self.crisis.us_type)
        self.assertEqual('long description', self.crisis.us_description)
        # Location
        self.assertEqual('city', self.crisis.us_city)
        self.assertEqual('st', self.crisis.us_state)
        self.assertEqual('country', self.crisis.us_country)
        self.assertEqual('1.23456', self.crisis.us_latitude)
        self.assertEqual('1.23456', self.crisis.us_longitude)
        # Other Data
        self.assertEqual('', self.crisis.us_startDate)
        self.assertEqual('', self.crisis.us_endDate)
        self.assertEqual(['$1000'], self.crisis.us_economicImpact)
        self.assertEqual(['1000 people'], self.crisis.us_humanImpact)
        self.assertEqual(['resource'], self.crisis.us_resourcesNeeded)
        self.assertEqual(['way'], self.crisis.us_waysToHelp)
        # Media and Links
        for link in self.crisis.external_links:
            self.assertEqual('http://www.somecoolplace.org/', link.source)
            self.assertEqual('link des', link.description)
        for cit in self.crisis.citations:
            self.assertEqual('http://www.wikipedia.org/', cit.source)
            self.assertEqual('citation des', cit.description)
        for m in self.crisis.maps:
            self.assertEqual('http://www.maps.com/map', m.source)
            self.assertEqual('map des', m.description)
        for image in self.crisis.images:
            self.assertEqual('http://www.images.com/random.jpg', image.source)
            self.assertEqual('image des', image.description)
        for social in self.crisis.social:
            self.assertTrue(
                social.social_id in ['facebookusername', '@twittername', 'twitterhashtag', 'youtubeusername'])
            self.assertTrue(social.social_type in ['facebook', 'twitter', 'youtube'])
        for video in self.crisis.videos:
            self.assertTrue(video.video_id in ['youtube', '12345'])
            self.assertTrue(video.video_type in ['youtube', 'vimeo'])

    def test_upload_org(self):
        # Base Data
        self.assertEqual('name', self.org.us_name)
        self.assertEqual(['name1', 'name2'], self.org.us_alternateNames)
        self.assertEqual('kind', self.org.us_type)
        self.assertEqual('long description', self.org.us_description)
        # Location
        self.assertEqual('city', self.org.us_city)
        self.assertEqual('st', self.org.us_state)
        self.assertEqual('country', self.org.us_country)
        self.assertEqual('1.23456', self.org.us_latitude)
        self.assertEqual('1.23456', self.org.us_longitude)
        # Other Data
        self.assertEqual('address\ncity, st zipcode', self.org.us_address)
        self.assertEqual('email@name.org', self.org.us_email)
        self.assertEqual('123 456 - 7890', self.org.us_phone)
        # Media and Links
        for link in self.org.external_links:
            self.assertEqual('http://www.somecoolplace.org/', link.source)
            self.assertEqual('link des', link.description)
        for cit in self.org.citations:
            self.assertEqual('http://www.wikipedia.org/', cit.source)
            self.assertEqual('citation des', cit.description)
        for m in self.org.maps:
            self.assertEqual('http://www.maps.com/map', m.source)
            self.assertEqual('map des', m.description)
        for image in self.org.images:
            self.assertEqual('http://www.images.com/random.jpg', image.source)
            self.assertEqual('image des', image.description)
        for social in self.org.social:
            self.assertTrue(
                social.social_id in ['facebookusername', '@twittername', 'twitterhashtag', 'youtubeusername'])
            self.assertTrue(social.social_type in ['facebook', 'twitter', 'youtube'])
        for video in self.org.videos:
            self.assertTrue(video.video_id in ['youtube', '12345'])
            self.assertTrue(video.video_type in ['youtube', 'vimeo'])

    def test_upload_person(self):
        # Base Data
        self.assertEqual('name', self.person.us_name)
        self.assertEqual(['name1', 'name2'], self.person.us_alternateNames)
        self.assertEqual('kind', self.person.us_type)
        self.assertEqual('long description', self.person.us_description)
        # Location
        self.assertEqual('city', self.person.us_city)
        self.assertEqual('st', self.person.us_state)
        self.assertEqual('country', self.person.us_country)
        self.assertEqual('1.23456', self.person.us_latitude)
        self.assertEqual('1.23456', self.person.us_longitude)
        # Media and Links
        for link in self.person.external_links:
            self.assertEqual('http://www.somecoolplace.org/', link.source)
            self.assertEqual('link des', link.description)
        for cit in self.person.citations:
            self.assertEqual('http://www.wikipedia.org/', cit.source)
            self.assertEqual('citation des', cit.description)
        for m in self.person.maps:
            self.assertEqual('http://www.maps.com/map', m.source)
            self.assertEqual('map des', m.description)
        for image in self.person.images:
            self.assertEqual('http://www.images.com/random.jpg', image.source)
            self.assertEqual('image des', image.description)
        for social in self.person.social:
            self.assertTrue(
                social.social_id in ['facebookusername', '@twittername', 'twitterhashtag', 'youtubeusername'])
            self.assertTrue(social.social_type in ['facebook', 'twitter', 'youtube'])
        for video in self.person.videos:
            self.assertTrue(video.video_id in ['youtube', '12345'])
            self.assertTrue(video.video_type in ['youtube', 'vimeo'])

    def test_relations(self):
        self.assertEqual(self.org.name, self.co.organization.name)
        self.assertEqual(self.crisis.name, self.co.crisis.name)
        self.assertEqual(self.crisis.name, self.cp.crisis.name)
        self.assertEqual(self.person.name, self.cp.person.name)
        self.assertEqual(self.org.name, self.op.organization.name)
        self.assertEqual(self.person.name, self.op.person.name)