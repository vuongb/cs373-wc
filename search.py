#!/usr/bin/env python

from google.appengine.api import search
import logging

_INDEX_NAME = 'WC_SearchIndex'

def add_to_index(document):
    try:
        search.Index(name=_INDEX_NAME).put(document)
    except search.Error:
        logging.exception('search.Index.Put() failed for %s', document)

def create_crisis_document(crisis):
    """
    Creates a Crisis search.Document from a crisis dictionary.
    """
    assert type(crisis) == dict
    return search.Document(
        doc_id  = crisis.get('us_id'),
        fields=[search.TextField(name='name',               value = crisis.get('us_name')),
                search.TextField(name='altername_names',    value = crisis.get('us_alternateNames')),
                search.TextField(name='type',               value = crisis.get('us_type')),
                search.TextField(name='description',        value = crisis.get('us_description')),
                search.TextField(name='city',               value = crisis.get('us_city')),
                search.TextField(name='state',              value = crisis.get('us_state')),
                search.TextField(name='country',            value = crisis.get('us_country')),
                search.GeoField(name='place',               value = search.GeoPoint(crisis.get('us_latitude'), crisis.get('us_longitude'))),
                search.DateField(name='startDate',          value = crisis.get('us_startDate')),
                search.DateField(name='endDate',            value = crisis.get('us_endDate')),
                search.NumberField(name='economicImpact',   value = crisis.get('us_economicImpact')),
                search.NumberField(name='humanDeaths',      value = crisis.get('us_humanDeaths')),
                search.NumberField(name='humanMissing',     value = crisis.get('us_humanMissing')),
                search.NumberField(name='humanInjured',     value = crisis.get('us_humanInjured')),
                search.NumberField(name='humanDisplaced',   value = crisis.get('us_humanDisplaced')),
                search.TextField(name='resourcesNeeded',    value = crisis.get('us_resourcesNeeded')),
                search.TextField(name='waysToHelp',         value = crisis.get('us_waysToHelp')),

        ])