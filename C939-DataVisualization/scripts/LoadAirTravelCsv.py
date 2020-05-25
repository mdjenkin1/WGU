#!/usr/bin/python

""" 
    Consume source air travel csv files to MongoDB prior to further analysis
"""

import os
import sys
import argparse
import pprint
import math

sys.path.append("./tools/")

from pymongo import MongoClient
from pymongo.errors import BulkWriteError

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract and prepare historic air travel schedule information')
    #parser.add_argument('--airports', nargs='+', default=["SLC"])
    parser.add_argument('--mongo_host', default='localhost')
    parser.add_argument('--mongo_port', default=27017)
    parser.add_argument('--config_dir', default='./StaticFiles')
    parser.add_argument('--test_set', action = 'store_true')
    parser.add_argument('--load_airports', action = 'store_true')
    parser.add_argument('--load_schedules', action = 'store_true')
    parser.add_argument('--generate_routes', action = 'store_true')
    parser.add_argument('--load_carriers', action = 'store_true')
    argv = parser.parse_args()

    mongo_client = MongoClient(argv.mongo_host, argv.mongo_port)
    db = mongo_client['air_travel']

    if argv.load_airports:
        from consume_airport_csv import consume_airport_csv
        print("reloading airport csv to mongodb.air_travel.airports")
        airport_info = consume_airport_csv(os.path.join(argv.config_dir, "airports.csv"))
        
        db['airports'].drop()
        db['airports'].create_index("iata", unique = True)
        db['airports'].insert_many(airport_info)

        # Missing Airport populated with information found: https://en.wikipedia.org/wiki/Columbus_Air_Force_Base
        # Appended value to source Airport CSV
        # pytz uses US/Central
        # timezonefinder uses America/Central
        #missingAirport = { 
        #    "iata" : "CBM", "airport" : "Columbus Air Force Base", 
        #    "city" : "Columbus", "state" : "MS", "country" : "USA", 
        #    "lat" : float(33.64379883),
        #    "long" : float(-88.44380188), 
        #    "timezone" : "US/Central" }
        #db['airports'].insert_one(missingAirport)

    if argv.test_set:
        rawsDir = "../TestData" 
        rawCollection = "raw_test_set"
    else:
        rawsDir = "../Raws" 
        rawCollection = "raw_schedules"

    # Load raw schedule information
    if argv.load_schedules or argv.test_set:
        from consume_schedule import consume_schedule_csv
        
        db[rawCollection].drop()
        print("Collection prepared for reloading")

        for csvFile in os.listdir(rawsDir):
            print("Processing csv: {}".format(csvFile))
            raw_schedule = consume_schedule_csv(os.path.join(rawsDir, csvFile))
            print("Appending to mongodb.air_travel.{}".format(rawCollection))
            db[rawCollection].insert_many(raw_schedule)
        print("Completed load of raw schedule data from csv.")

    # Process flight data to populate route data
    # Assume the raw_schedules and airports collections are populated
    if argv.generate_routes:
        print("Gathering origin and destination pairs")
        from airtravel_routes import get_route_description
        raw_routes = [doc for doc in db[rawCollection].aggregate([
            {'$group':{'_id':{'origin':'$origin', 'destination':'$destination'}}}
        ])]
        #pprint.pprint(raw_routes)
        
        print("Calculating route detail")
        routes = []
        for route in raw_routes:
            o = db['airports'].find_one({'iata' : route['_id']['origin']})
            d = db['airports'].find_one({'iata' : route['_id']['destination']})
            #pprint.pprint(route)
            #print(origin: {}".format(o))
            #print(destination: {}".format(d))
            #if o and d:
            routes.append(get_route_description(o, d))

        print("Loading route collection to MongoDB")
        #pprint.pprint(routes)
        db['routes'].drop_indexes()
        db['routes'].drop()
        db['routes'].create_index([("destination", -1), ("origin", -1)], unique = True)
        try:
            db['routes'].insert_many(routes)
        except BulkWriteError as bwe:
            print(bwe.details)

    if argv.load_carriers:
        print("Loading carriers csv")
        from consume_carriers_csv import consume_carriers_csv

        db['carriers'].drop_indexes()
        db['carriers'].drop()
        db['carriers'].create_index([('code', -1)], unique = True)
        
        carriers = consume_carriers_csv(os.path.join(argv.config_dir, "carriers.csv"))

        db['carriers'].insert_many(carriers)
        
