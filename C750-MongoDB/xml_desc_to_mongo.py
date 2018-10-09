"""
Generic script to insert xml description to local MongoDB listening on the default port
"""

import describe_xml as dxml
import pprint
from pymongo import MongoClient

def connect_db(host="localhost", port=27017):
    client = MongoClient(host, port)
    return client

def test(infile = 'map', db_name = 'xml_descriptions', coll = 'map'):
	client = connect_db()
	db = client[db_name]
	xml_desc = dxml.get_xml_description(infile)
	db[coll].insert_many(xml_desc['elements'])

if __name__ == "__main__":
	test()