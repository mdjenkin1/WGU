#! /bin/python

'''
    Seems we forgot to provide carrier detail
'''

import os
import sys
import argparse
import pprint
import math

sys.path.append("./tools/")

from pymongo import MongoClient
from flight_times import GetFlightTimeData,GetFlightStats

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract and prepare historic air travel schedule information")
    parser.add_argument("--mongo_host", default="localhost")
    parser.add_argument("--mongo_port", default=27017)
    parser.add_argument("--config_dir", default="./StaticFiles")
    parser.add_argument('--add_carriers', action = 'store_true')
    parser.add_argument("--skip_records", default=0)
    argv = parser.parse_args()
    
    mongo_client = MongoClient(argv.mongo_host, argv.mongo_port)

    argv.add_carriers = True

    with mongo_client:
        i = offset = int(argv.skip_records)

        db = mongo_client['air_travel']

        for carrier in db.carriers.find().skip(offset):
            i += 1
            db['detailed_flights'].update_many({'flight.carrier': carrier['code']}, {'$set': {'flight.carrier': carrier}})
            print("finished updating flights for carrier: {} skip {} to start on next.".format(carrier['code'], i))




#        detailed_flights = db['detailed_flights'].find({}, batch_size=10000).skip(offset).limit(4)
        #carriers = db['carriers'].find()
#        for record in detailed_flights:
#            carrier = record['flight']['carrier']
#            print("looking for carrier: {}".format(carrier))
#
#            detailed_carrier = db['carriers'].find_one({'code':carrier}, {'_id':0})
#
#            record['flight']
#
#            print("found carrier {}".format(detailed_carrier))
