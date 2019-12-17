#!/usr/bin/python

""" 
    Consume source air travel csv files to MongoDB prior to further analysis
"""

import os
import sys
import argparse

sys.path.append("./tools/")

from pymongo import MongoClient

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract and prepare historic air travel schedule information')
    #parser.add_argument('--airports', nargs='+', default=["SLC"])
    parser.add_argument('--mongo_host',  default='localhost')
    parser.add_argument('--mongo_port',  default=27017)
    parser.add_argument('--config_dir',  default='./StaticFiles')
    parser.add_argument('--raw_csv_dir',  default='../Raws')
    #parser.add_argument('--raw_csv_dir',  default='../TestData')
    parser.add_argument('--load_Airports', action = 'store_true')
    parser.add_argument('--load_Carriers', action = 'store_true')
    parser.add_argument('--load_RawSchedules', action = 'store_true')
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

    # Load raw schedule information
    if argv.load_RawSchedules:
        from consume_schedule import consume_schedule_csv
        db['RawSchedules'].drop()
        print("Collection prepared for reloading")
        for csvFile in os.listdir(argv.raw_csv_dir):
            print("Processing csv: {}".format(csvFile))
            raw_schedule = consume_schedule_csv(os.path.join(argv.raw_csv_dir, csvFile))
            print("Appending raw schedule to mongodb.AirTravel.RawSchedules")
            db['RawSchedules'].insert_many(raw_schedule)
