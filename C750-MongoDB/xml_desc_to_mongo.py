"""
Generic script to insert xml description to local MongoDB listening on the default port
"""

import describe_xml as dxml
import pprint
from pymongo import MongoClient

def insert_to_db(data, db, doc):
    for item in data: 
        db[doc].insert_one(item)

def connect_db(host="localhost", port=27017):
    client = MongoClient(host, port)
    return client

def test(infile = 'map.small.snip', doc = 'map'):
	client = connect_db()
	db = client['xml_descriptions']
	xml_desc = dxml.get_xml_description(infile)
	insert_to_db(xml_desc['elements'], db, doc)

if __name__ == "__main__":
	test()