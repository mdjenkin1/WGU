#!/usr/bin/python

""" 
    Consume source air travel csv files to MongoDB prior to further analysis
"""

import os
import sys
import argparse
import pprint

sys.path.append("./tools/")

from pymongo import MongoClient

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract and prepare historic air travel schedule information')
    #parser.add_argument('--airports', nargs='+', default=["SLC"])
    parser.add_argument('--mongo_host',  default='localhost')
    parser.add_argument('--mongo_port',  default=27017)
    parser.add_argument('--config_dir',  default='./StaticFiles')
    parser.add_argument('--test_raws',  action = 'store_true')
    parser.add_argument('--load_Airports', action = 'store_true')
    parser.add_argument('--load_Carriers', action = 'store_true')
    parser.add_argument('--load_RawSchedules', action = 'store_true')
    parser.add_argument('--generate_routes', action = 'store_true')
    argv = parser.parse_args()

    mongo_client = MongoClient(argv.mongo_host, argv.mongo_port)
    db = mongo_client['AirTravel']

    if argv.load_Airports:
        from consume_airport_csv import consume_airport_csv
        print("reloading airport csv to mongodb.AirTravel.Airports")
        db['Airports'].drop()
        airport_info = consume_airport_csv(os.path.join(argv.config_dir, "airports.csv"))
        db['Airports'].insert_many(airport_info)
        
    if argv.load_Carriers:
        from consume_carriers_csv import consume_carriers_csv
        print("reloading carriers csv to mongodb.AirTravel.Carriers")
        db['Carriers'].drop()
        airport_info = consume_airport_csv(os.path.join(argv.config_dir, "airports.csv"))
        db['Carriers'].insert_many(airport_info)

    if argv.test_raws:
        rawsDir = "../TestData" 
        rawCollection = "RawsTestSet"
    else:
        rawsDir = "../Raws" 
        rawCollection = "RawSchedules"

    # Load raw schedule information
    if argv.load_RawSchedules or argv.test_raws:
        from consume_schedule import consume_schedule_csv
        
        db[rawCollection].drop()
        print("Collection prepared for reloading")

        for csvFile in os.listdir(rawsDir):
            print("Processing csv: {}".format(csvFile))
            raw_schedule = consume_schedule_csv(os.path.join(rawsDir, csvFile))
            print("Appending to mongodb.AirTravel.{}".format(rawCollection))
            db[rawCollection].insert_many(raw_schedule)

    # Process flight data to populate route data
    # Assume the RawSchedules and Airports collections are populated
    if argv.generate_routes:
        from airtravel_routes import get_route_description
        raw_routes = [doc for doc in db[rawCollection].aggregate([
            {'$group':{'_id':{'origin':'$Airport_Origin', 'destination':'$Airport_Destination'}}}
        ])]
        routes = []
        for route in raw_routes:
            o = db['Airports'].find_one({'iata' : route['_id']['origin']})
            d = db['Airports'].find_one({'iata' : route['_id']['destination']})
            pprint.pprint(route)
            print("Origin: {}".format(o))
            print("Destination: {}".format(d))
            routes.append(get_route_description(o, d))

        pprint.pprint(routes)

