from google.appengine.ext import db

def get_location(model_class, id):
    """
    returns the locations associated with an object of a particular model and id
    model_class is the class of the model, ie Person, Organization...
    id is the id of the desired object from which to get the location
    returns a set of locations
    """
    location = db.GqlQuery("SELECT us_city, us_state, us_country, us_latitude, us_longitude FROM " + model_class.__name__ + " WHERE us_id = " + str(id)).run()
    return distinct([(l.us_city, l.us_state, l.us_latitude, l.us_longitude) for l in location])
    #todo: edge case, if a city-state-country duplicate exists, but one has latitude/longitude and the other doesn't, the call to distinct will keep both. we should handle latitude-longitude differently

def get_contact_info(id):
    contact_info = db.GqlQuery("SELECT us_address, us_email, us_phone FROM Organization WHERE us_id = " + str(id)).run()
    return distinct([(c.us_address, c.us_email, c.us_phone) for c in contact_info])

def get_names(model_class, id):
    query = db.GqlQuery("SELECT us_name, us_alternateNames FROM " + model_class.__name__ + " WHERE us_id = " + str(id)).run()
    names = set()
    try:
        for i in query:
            names.add(i.us_name)
            for name in i.us_alternateNames:
                names.add(name)
    except StopIteration:
        return names

def distinct(l):
    """
    returns a set containing the distinct values in a collection
    """
    #todo: How important is order? Should this be rewritten to return a list honoring order of l?
    return set(l)

def merge(id, model_str):
    """
    creates a dictionary containing all the merged data for a model of a specific id to render to html
    id is the id of the object to render
    model_class is the class of the object, ie Organization, Person, Crisis
    returns a dictionary with attribute names as keys and string results as values
    """
    query = db.GqlQuery("SELECT * FROM " + model_str + " WHERE us_id = :1", id)

    ## result dict
    result = {'ID': str(id)}

    ## merge common data
    for obj in query:
        if 'Name' in result:
            if 'Alternate Names' in result:
                if obj.us_name not in result['Alternate Names'].split(','):
                    result['Alternate Names'] += ', ' + obj.us_name
        else:
            result['Name'] = obj.us_name

        if 'Alternate Names' in result:
            if obj.us_alternateNames is not None:
                for name in obj.us_alternateNames.split(','):
                    if name not in result['Alternate Names']:
                        result['Alternate Names'] += ', ' + name
        else:
            result['Alternate Names'] = obj.us_name

        if 'Kind' in result:
            for kind in obj.us_type.split(','):
                if kind not in result['Kind']:
                    result['Kind'] += ', ' + kind
        else:
            result['Kind'] = obj.us_type

        if 'Description' in result:
            for descrip in obj.us_description.split('\n'):
                if descrip not in result['Description']:
                    result['Description'] += '\n \n' + descrip
        else:
            result['Description'] = obj.us_description

        if 'Location' in result:
            merge_location(result, obj)
        else:
            result['Location'] = [(obj.us_city, obj.us_state, obj.us_country)]

    return result

def merge_location(result, obj):
    for location in result['Location']:
        if location[0] == obj.us_city:
            return
        elif obj.us_city is None and obj.us_country == location[2]:
            return

    result['Location'].append((obj.us_city, obj.us_state, obj.us_country))


def merge_org(id):
    pass

def merge_person(id):
    pass

# Test code
#print(distinct([
#    ("New York", "NY", "12345", None, None),
#    ("New York", "NY", "12345", None, None),
#    ("Austin", "TX", "78705", None, None),
#    ("Austin", "TX", "78705", 1, 2)
#]))