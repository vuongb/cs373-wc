#!/usr/bin/env python

from google.appengine.api import search
from Models import Crisis, Person, Organization
import logging

_INDEX_NAME = 'WC_SearchIndex'

def add_to_index(document):
    try:
        search.Index(name=_INDEX_NAME).put(document)
        logging.info("Built search index for %s", document)
    except search.Error:
        logging.exception('search.Index.Put() failed for %s', document)

def create_document(wcObject):
    """
    Creates a search.Document from a given Crisis, Person, Organization object.
    """

    fieldsList = []
    if type(wcObject)   == Crisis:
        fieldsList  = build_crisis_fields(wcObject)
    elif type(wcObject) == Person:
        fieldsList  = build_person_fields(wcObject)
    elif type(wcObject) == Organization:
        fieldsList  = build_organization_fields(wcObject)
    else:
        logging.error("Index not built for %s because it didn't match a model type")

    return search.Document(
            doc_id  = wcObject.us_id,
            fields  = fieldsList
    )


def build_crisis_fields(crisis):
    fields = []
    fields.append(search.TextField(name='name',               value = crisis.us_name))
    fields.append(search.TextField(name='alternate_names',    value = crisis.us_alternateNames))
    fields.append(search.TextField(name='type',               value = crisis.us_type))
    fields.append(search.TextField(name='description',        value = crisis.us_description))
    fields.append(search.TextField(name='city',               value = crisis.us_city))
    fields.append(search.TextField(name='state',              value = crisis.us_state))
    fields.append(search.TextField(name='country',            value = crisis.us_country))
    if crisis.us_latitude and crisis.us_longitude:
        fields.append(search.GeoField(name='place',               value = search.GeoPoint(float(crisis.us_latitude), float(crisis.us_longitude))))
    if crisis.us_startDate:
        fields.append(search.DateField(name='startDate',          value = crisis.us_startDate))
    if crisis.us_endDate:
        fields.append(search.DateField(name='endDate',            value = crisis.us_endDate))
    # Conversion to str (TextField) because humanDeaths, etc. may be greater value than max Integer value
    fields.append(search.TextField(name='economicImpact',   value = str(crisis.us_economicImpact)))
    fields.append(search.TextField(name='humanDeaths',      value = str(crisis.us_humanDeaths)))
    fields.append(search.TextField(name='humanMissing',     value = str(crisis.us_humanMissing)))
    fields.append(search.TextField(name='humanInjured',     value = str(crisis.us_humanInjured)))
    fields.append(search.TextField(name='humanDisplaced',   value = str(crisis.us_humanDisplaced)))
    # Conversion to str because resourcesNeeded and waysToHelp are lists
    fields.append(search.TextField(name='resourcesNeeded',    value = str(crisis.us_resourcesNeeded)))
    fields.append(search.TextField(name='waysToHelp',         value = str(crisis.us_waysToHelp)))
    return fields


def build_organization_fields(organization):
    fields = []
    fields.append(search.TextField(name='name',             value = organization.us_name))
    fields.append(search.TextField(name='alternate_names',  value = organization.us_alternateNames))
    fields.append(search.TextField(name='type',             value = organization.us_type))
    fields.append(search.TextField(name='description',      value = organization.us_description))
    fields.append(search.TextField(name='city',             value = organization.us_city))
    fields.append(search.TextField(name='state',            value = organization.us_state))
    fields.append(search.TextField(name='country',          value = organization.us_country))
    if organization.us_latitude and organization.us_longitude:
        fields.append(search.GeoField(name='place',             value = search.GeoPoint(float(organization.us_latitude), float(organization.us_longitude))))
    fields.append(search.TextField(name='address',          value = organization.us_address))
    fields.append(search.TextField(name='email',            value = organization.us_email))
    fields.append(search.TextField(name='phone',            value = organization.us_phone))
    return fields


def build_person_fields(person):
    fields = []
    fields.append(search.TextField(name='name',             value = person.us_name))
    fields.append(search.TextField(name='alternate_names',  value = person.us_alternateNames))
    fields.append(search.TextField(name='type',             value = person.us_type))
    fields.append(search.TextField(name='description',      value = person.us_description))
    fields.append(search.TextField(name='city',             value = person.us_city))
    fields.append(search.TextField(name='state',            value = person.us_state))
    fields.append(search.TextField(name='country',          value = person.us_country))
    if person.us_latitude and person.us_longitude:
        fields.append(search.GeoField(name='place',             value = search.GeoPoint(float(person.us_latitude), float(person.us_longitude))))
    return fields

def process_search_query(queryString):

    search_results      = {}

    # Catch search errors (such as single double-quotes or illegal characters)
    try:
        document_results = find_documents(queryString)
    except Exception as e:
        logging.error(e)
        return "invalid"

    if document_results:
        for scored_document in document_results:
            # grab all the descriptions
            descriptions = [x.value for x in scored_document.expressions if x.name == 'description']
            # build a dictionary of type {id: [description list]}
            search_results[scored_document.doc_id] = descriptions
    return search_results


def find_documents(queryString):
    assert type(queryString) == str

    # construct the terms to search against
    expr_list = [search.SortExpression(
        expression='name',
        default_value='',
        direction=search.SortExpression.DESCENDING)]

    # construct the sort options
    sort_opts = search.SortOptions(
        expressions=expr_list)

    # construct the options for returned query
    query_options = search.QueryOptions(
        limit           = 100,
        sort_options    = sort_opts,
        returned_fields = ['name'],
        snippeted_fields= ['description'])

    query_obj = search.Query(query_string=queryString, options=query_options)

    # For debugging purposes, lists index schemas
    for index in search.get_indexes(fetch_schema=True):
        logging.info("index %s", index.name)
        logging.info("schema: %s", index.schema)

    return search.Index(name=_INDEX_NAME).search(query=query_obj)
