"""
Generic script for inserting JSON formated xml descriptions to local MongoDB listening on the default port
"""

import desc_tag_attribs as txml
import pprint
from pymongo import MongoClient

def connect_db(host="localhost", port=27017):
    client = MongoClient(host, port)
    return client

def test(infile = 'map', db_name = 'xml_descriptions', coll = 'map_tags'):
	client = connect_db()
	db = client[db_name]
	tag_xml = txml.get_tag_attrib_list(infile)
	db[coll].insert_many(tag_xml)

if __name__ == "__main__":
	test()