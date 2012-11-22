#!/usr/bin/env python

from google.appengine.api import search
import logging

_INDEX_NAME = 'WC_SearchIndex'

def add_to_index(document):
    try:
        search.Index(name=_INDEX_NAME).put(document)
        logging.info("Built search index for %s", document)
    except search.Error:
        logging.exception('search.Index.Put() failed for %s', document)

def create_document(wcObjectDctionary):
    """
    Creates a search.Document from a given dictionary.
    """
    assert type(wcObjectDctionary) == dict
    return search.Document(
            doc_id  = wcObjectDctionary.get('us_id'),
        # TODO: if it's a crisis, call build_crisis_fields, etc
            fields  = build_crisis_fields(wcObjectDctionary)
    )

# TODO: See Piazza post @134. Because of checking for empty values, this method calls .get() twice for each attribute. Inefficient.
def build_crisis_fields(crisis):
    fields = []
    if crisis.get('us_name'):
        fields.append(search.TextField(name='name',               value = crisis.get('us_name')))
    if crisis.get('us_alternateNames'):
        fields.append(search.TextField(name='alternate_names',    value = crisis.get('us_alternateNames')))
    if crisis.get('us_type'):
        fields.append(search.TextField(name='type',               value = crisis.get('us_type')))
    if crisis.get('us_description'):
        fields.append(search.TextField(name='description',        value = crisis.get('us_description')))
    if crisis.get('us_city'):
        fields.append(search.TextField(name='city',               value = crisis.get('us_city')))
    if crisis.get('us_state'):
        fields.append(search.TextField(name='state',              value = crisis.get('us_state')))
    if crisis.get('us_country'):
        fields.append(search.TextField(name='country',            value = crisis.get('us_country')))
    if crisis.get('us_latitude') and crisis.get('us_longitude'):
        fields.append(search.GeoField(name='place',               value = search.GeoPoint(crisis.get('us_latitude'), crisis.get('us_longitude'))))
    if crisis.get('us_startDate'):
        fields.append(search.DateField(name='startDate',          value = crisis.get('us_startDate')))
    if crisis.get('us_endDate'):
        fields.append(search.DateField(name='endDate',            value = crisis.get('us_endDate')))
    # Conversion to str (TextField) because humanDeaths, etc. may be greater value than max Integer value
    if crisis.get('us_economicImpact'):
        fields.append(search.TextField(name='economicImpact',   value = str(crisis.get('us_economicImpact'))))
    if crisis.get('us_humanDeaths'):
        fields.append(search.TextField(name='humanDeaths',      value = str(crisis.get('us_humanDeaths'))))
    if crisis.get('us_humanMissing'):
        fields.append(search.TextField(name='humanMissing',     value = str(crisis.get('us_humanMissing'))))
    if crisis.get('us_humanInjured'):
        fields.append(search.TextField(name='humanInjured',     value = str(crisis.get('us_humanInjured'))))
    if crisis.get('us_humanDisplaced'):
        fields.append(search.TextField(name='humanDisplaced',   value = str(crisis.get('us_humanDisplaced'))))
    # Conversion to str because resourcesNeeded and waysToHelp are lists
    if crisis.get('us_resourcesNeeded'):
        fields.append(search.TextField(name='resourcesNeeded',    value = str(crisis.get('us_resourcesNeeded'))))
    if crisis.get('us_waysToHelp'):
        fields.append(search.TextField(name='waysToHelp',         value = str(crisis.get('us_waysToHelp'))))
