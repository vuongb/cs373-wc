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

def merge(id, model_class):
    query = db.GqlQuery("SELECT * FROM " + model_class.__name__ + " WHERE us_id = " + str(id))

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
            for name in obj.us_alternateName.split(','):
                if name not in result['Alternate Names']:
                    result['Alternate Names'] += ', ' + name
        else:
            result['Alternate Names'] = obj.us_name

        if 'Kind' in result:
            pass
        else:
            result['Kind'] = obj.us_kind

        if 'Description' in result:
            pass
        else:
            result['Description'] = obj.us_description

        merge_location(result, obj)

def merge_location(result, obj):
    pass

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