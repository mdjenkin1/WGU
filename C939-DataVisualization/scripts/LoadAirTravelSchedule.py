#!/usr/bin/python

""" 
    Consume source air travel csv files to MongoDB prior to further analysis
"""

import os
import sys
import argparse
#import pickle
#import math

#import json
#import csv

#import pprint

sys.path.append("./tools/")
#import air_journey_describer
#import dst_asylum

from pymongo import MongoClient

cfgDir = "./StaticFiles"
#rawDir = "../Raws"
rawDir = "../TestData"

def get_airport_schedule(airports):
    print("received airports: {}".format(airports))
    return True

def connect_mongodb(host = 'localhost', port = 27017):
    client = MongoClient(host, port)
    return client

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract and prepare historic air travel schedule information')
    parser.add_argument('--airports', nargs='+', default=["SLC"])
    parser.add_argument('--mongo_host',  default='localhost')
    parser.add_argument('--mongo_port',  default=27017)
    parser.add_argument('--load_airport_csv', action = 'store_true')
    parser.add_argument('--load_schedules_csv', action = 'store_true')
    argv = parser.parse_args()

    mongo_client = MongoClient(argv.mongo_host, argv.mongo_port)
    db = mongo_client['AirTravel']

    if argv.load_airport_csv:
        from consume_airport_csv import consume_airport_csv
        print("loading airport csv to mongodb")
        airport_info = consume_airport_csv(os.path.join(cfgDir, "airports.csv"))
        db['airports'].insert_many(airport_info)

    # Load raw schedule information
    if argv.load_schedules_csv:



    # Create route collection if it does not exist.
    db['routes'].create_index(['origin', 'destination'], unique=True)

    get_airport_schedule(argv.airports)