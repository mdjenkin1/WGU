"""
General script to insert xml description to local MongoDB listening on the default port
"""

import describe_xml as dxml
import pprint
from pymongo import MongoClient

def connect_db(host="localhost", port=27017):
    client = MongoClient(host, port)
    return client

def load_xml_desc_to_mongo(infile, coll, db_name = 'xml_descriptions'):
	client = connect_db()
	db = client[db_name]
	xml_desc = dxml.get_xml_description(infile)
	db[coll].insert_many(xml_desc['elements'])

def test():
	load_xml_desc_to_mongo('map', 'osm_map')

if __name__ == "__main__":
	test()