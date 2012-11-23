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
    return fields


# TODO: See Piazza post @134. Because of checking for empty values, this method calls .get() twice for each attribute. Inefficient.
def build_organization_fields(organization):
    fields = []
    if organization.get('us_name'):
        fields.append(search.TextField(name='name',             value = organization.get('us_name')))
    if organization.get('us_alternateNames'):
        fields.append(search.TextField(name='alternate_names',  value = organization.get('us_alternateNames')))
    if organization.get('us_type'):
        fields.append(search.TextField(name='type',             value = organization.get('us_type')))
    if organization.get('us_description'):
        fields.append(search.TextField(name='description',      value = organization.get('us_description')))
    if organization.get('us_city'):
        fields.append(search.TextField(name='city',             value = organization.get('us_city')))
    if organization.get('us_state'):
        fields.append(search.TextField(name='state',            value = organization.get('us_state')))
    if organization.get('us_country'):
        fields.append(search.TextField(name='country',          value = organization.get('us_country')))
    if organization.get('us_latitude') and organization.get('us_longitude'):
        fields.append(search.GeoField(name='place',             value = search.GeoPoint(organization.get('us_latitude'), organization.get('us_longitude'))))
    if organization.get('us_address'):
        fields.append(search.TextField(name='address',          value = organization.get('us_address')))
    if organization.get('us_email'):
        fields.append(search.TextField(name='email',            value = organization.get('us_email')))
    if organization.get('us_phone'):
        fields.append(search.TextField(name='phone',            value = organization.get('us_phone')))


# TODO: See Piazza post @134. Because of checking for empty values, this method calls .get() twice for each attribute. Inefficient.
def build_person_fields(person):
    fields = []
    if person.get('us_name'):
        fields.append(search.TextField(name='name',             value = person.get('us_name')))
    if person.get('us_alternateNames'):
        fields.append(search.TextField(name='alternate_names',  value = person.get('us_alternateNames')))
    if person.get('us_type'):
        fields.append(search.TextField(name='type',             value = person.get('us_type')))
    if person.get('us_description'):
        fields.append(search.TextField(name='description',      value = person.get('us_description')))
    if person.get('us_city'):
        fields.append(search.TextField(name='city',             value = person.get('us_city')))
    if person.get('us_state'):
        fields.append(search.TextField(name='state',            value = person.get('us_state')))
    if person.get('us_country'):
        fields.append(search.TextField(name='country',          value = person.get('us_country')))
    if person.get('us_latitude') and person.get('us_longitude'):
        fields.append(search.GeoField(name='place',             value = search.GeoPoint(person.get('us_latitude'), person.get('us_longitude'))))
        

def process_search_query(queryString):

    search_results = {}

    document_results = find_documents(queryString)

    if document_results:
        for scored_document in document_results:
            # process scored_document
            for index, field in enumerate(scored_document.fields):
                # Right now, only include names as results
                if field.name == "name":
                    name = field.value
                    # if there's a snippet, include it
                    if scored_document.expressions[index]:
                        snippet = scored_document.expressions[index].value
                    else:
                        snippet = ""
                    search_results[name] = snippet
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
        limit           = 3,
        sort_options    = sort_opts,
        returned_fields = ['name'],
        snippeted_fields= ['description'])

    query_obj = search.Query(query_string=queryString, options=query_options)

    # For debugging purposes, lists index schemas
    for index in search.get_indexes(fetch_schema=True):
        logging.info("index %s", index.name)
        logging.info("schema: %s", index.schema)

    return search.Index(name=_INDEX_NAME).search(query=query_obj)
