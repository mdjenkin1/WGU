"""
Generic script to insert xml described  MongoDB listening on the default port

script from lesson
#!/usr/bin/env python

Add a single line of code to the insert_autos function that will insert the
automobile data into the 'autos' collection. The data variable that is
returned from the process_file function is a list of dictionaries, as in the
example in the previous video.


from autos import process_file


def insert_autos(infile, db):
	data = process_file(infile)
	# Add your code here. Insert the data in one command.
	for item in data: db.autos.insert(item)
  
if __name__ == "__main__":
	# Code here is for local use on your own computer.
	from pymongo import MongoClient
	client = MongoClient("mongodb://localhost:27017")
	db = client.examples

	insert_autos('autos-small.csv', db)
	print(db.autos.find_one())

"""
import describe_xml as dxml
import pprint
from pymongo import MongoClient

def insert_to_db(data, db, doc):
    for item in data: 
        #pprint.pprint(item)
        db[doc].insert(item)

def connect_db(host="localhost", port=27017):
    client = MongoClient(host, port)
    return client

def test(infile = 'map', doc = 'map'):
	client = connect_db()
	db = client['xml_descriptions']
	xml_desc = dxml.get_xml_description(infile)
	insert_to_db(xml_desc['elements'], db, doc)
	print(db[doc].find_one())

if __name__ == "__main__":
	test()