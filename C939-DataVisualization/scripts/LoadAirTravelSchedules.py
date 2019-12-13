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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract and prepare historic air travel schedule information')
    #parser.add_argument('--airports', nargs='+', default=["SLC"])
    parser.add_argument('--mongo_host',  default='localhost')
    parser.add_argument('--mongo_port',  default=27017)
    parser.add_argument('--config_dir',  default='./StaticFiles')
    #parser.add_argument('--raw_csv_dir',  default='../Raws')
    parser.add_argument('--raw_csv_dir',  default='../TestData')
    parser.add_argument('--load_airport_csv', action = 'store_true')
    parser.add_argument('--load_raw_schedules', action = 'store_true')
    argv = parser.parse_args()

    mongo_client = MongoClient(argv.mongo_host, argv.mongo_port)
    db = mongo_client['AirTravel']

    if argv.load_airport_csv:
        from consume_airport_csv import consume_airport_csv
        print("loading airport csv to mongodb")
        drop
        airport_info = consume_airport_csv(os.path.join(argv.config_dir, "airports.csv"))
        db['airports'].insert_many(airport_info)

    # Load raw schedule information
    if argv.load_raw_schedules:
        from consume_schedule import consume_schedule_csv
        for csvFile in os.listdir(argv.raw_csv_dir):
            print("Processing: {}".format(csvFile))
            db['raw_schedules'].insert_many(consume_schedule_csv(os.path.join(argv.raw_csv_dir, csvFile)))

    # Create route collection if it does not exist.
    #db['routes'].create_index(['origin', 'destination'], unique=True)

#    get_airport_schedule(argv.airports)