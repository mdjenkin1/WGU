"""
Find answers to generic questions about xml metadata.
xml metadata is assumed to be loaded to mongodb
"""

from pymongo import MongoClient
import pprint

## Which have attributes have more than one data type?
# What are all the attributes in the data set?
# What data types do those attributes have?
# Return which attributes have more than one data type.
# Which elements have those attributes?
def many_typed_attribs(db):
    all_attribs = []
    multi_attribs = []
    return multi_attribs

## Which elements are nested in other elements?
# 
# 
# 

def connect_db(host="localhost", port=27017):
    client = MongoClient(host, port)
    return client

def test(db_name = 'xml_descriptions', coll = "map"):
    client = connect_db()
    db = client[db_name]
    pprint.pprint(many_typed_attribs(db))
    pass

if __name__ == "__main__":
    test()