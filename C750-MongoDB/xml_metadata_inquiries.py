"""
A quick and dirty script to perform inquiries on XML Metadata.
Expectation is:
The metadata is stored in a local MongoDB engine.
The metadata was generated in the following structure.

{
    name: string
    attribs: {attrib_name:set(types...)},
    nested_elements: set(),
    text: set()
}

XML Description structure:
{
    elements:[
        {elem1}
        ...,
        {elemn}
    ]
}

"""

from pymongo import MongoClient

# The get_db and connect_db functions 
# are modified versions of the same functions provided by
# the Udacity MongoDB data wrangling course
def connect_db(host="localhost", port=27017):
    client = MongoClient(host, port)
    return client

def get_db(database):
    client = connect_db()
    db = client[database]
    return db

def loaner_elements(db, coll):
    all_elements = [doc for doc in db[coll].aggregate([{'$project': {"_id": "$name"}}])]
    parent_elements = [doc for doc in db[coll].aggregate([
        {'$match': {"nested_elements": {'$ne': None}}}, 
        {'$group': {"_id": "$name"}}
    ])]
    child_elements = [doc for doc in db[coll].aggregate([
        {'$match': {"nested_elements": {'$ne': None}}}, 
        {'$unwind': "$nested_elements"}, 
        {'$group': {"_id": "$nested_elements"}}
    ])]
    
    # convert our list of dicts to a set of values
    all_elem = { elem["_id"] for elem in all_elements }
    parent_elem = { elem["_id"] for elem in parent_elements }
    child_elem = { elem["_id"] for elem in child_elements }

    return all_elem - parent_elem - child_elem

def test():
    db = get_db('xml_descriptions')
    print("These are the elements that have no nested elements and are not nested elements.")
    print(loaner_elements(db, 'osm_map'))

if __name__ == "__main__":
    test()