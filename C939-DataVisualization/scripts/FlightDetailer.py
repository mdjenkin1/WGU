""" 
    Scrub flight scheduling data after consumption of raw air travel csv files
    Pre-existing Collections:
        > db.airports.findOne()
        {
            "_id" : ObjectId("5e9c9bba6018921f596f83db"),
            "iata" : "00M",
            "airport" : "Thigpen ",
            "city" : "Bay Springs",
            "state" : "MS",
            "country" : "USA",
            "lat" : 0.557698402771604,
            "long" : -1.5574359137504208,
            "timezone" : "America/Chicago"
        }

        > db.raw_schedules.findOne()
        {
            "_id" : ObjectId("5e9d1d5609199fdc472129f0"),
            "origin_date" : ISODate("1987-10-14T00:00:00Z"),
            "sched_depart_local_time" : "730",
            "sched_arrive_local_time" : "849",
            "sched_travel_time" : "79",
            "actual_depart_local_time" : "741",
            "actual_arrive_local_time" : "912",
            "actual_travel_time" : "91",
            "carrier" : "PS",
            "flight_num" : "1451",
            "tail_num" : "NA",
            "origin" : "SAN",
            "destination" : "SFO",
            "taxi_time_in" : "NA",
            "taxi_time_out" : "NA",
            "cancelled" : "0",
            "cancel_code" : "NA",
            "diverted" : "0",
            "distance" : "447",
            "time_delay_arrival" : "23",
            "time_delay_depart" : "11",
            "time_delay_carrier" : "NA",
            "time_delay_weather" : "NA",
            "time_delay_nas" : "NA",
            "time_delay_security" : "NA",
            "time_delay_aircraft" : "NA"
        }

        > db.routes.findOne()
        {
            "_id" : ObjectId("5e9d2d9a09199fdc477e2869"),
            "destination" : "RDU",
            "origin" : "PIT",
            "distance_calculated" : 328,
            "bearing" : 166,
            "direction" : "South"
        }

    Target Collection schema
        > db.flights.findOne()
        {
            "carrier"
            "flight_num"
            "tail_num"
            "sched_depart_utc"
            "sched_arrive_utc"
            "actual_depart_utc"
            "actual_arrive_utc"
            "travel_time" : {
                "scheduled"
                "actual"
                "taxi_in"
                "in_air"
                "taxi_out"
            }
            "route" : {
                "origin" : {
                    "iata"
                    "airport"
                    "city"
                    "state"
                    "country"
                    "latitude"
                    "longitude"
                    "timezone"
                }
                "destination" : {
                    "iata"
                    "airport"
                    "city"
                    "state"
                    "country"
                    "latitude"
                    "longitude"
                    "timezone"
                }
                "bearing"
                "direction"
                "distance"
            }
            "schedule_skew" : {
                "arrival_minutes"
                "depart_minutes"
            }
            "aborted" : {
                "cancelled"
                "diverted"
                "cancel_code"
            }
            "attributed_delays" : {
                "carrier"
                "weather"
                "nas"
                "security"
                "late_aircraft"
            }
        }
"""

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
    parser.add_argument('--test_set', action = 'store_true')
    parser.add_argument('--full', action = 'store_true')
    parser.add_argument("--skip_records", default=0)
    parser.add_argument('--detailed_routes', action = 'store_true')
    parser.add_argument('--detailed_flights', action = 'store_true')
    parser.add_argument('--refresh', action = 'store_true')
    parser.add_argument('--restart', action = 'store_true')
    argv = parser.parse_args()
    
    if argv.test_set:
        rawsDir = "../TestData" 
        rawCollection = "raw_test_set"
    else:
        rawsDir = "../Raws" 
        rawCollection = "raw_schedules"

    mongo_client = MongoClient(argv.mongo_host, argv.mongo_port)

    with mongo_client:

        db = mongo_client['air_travel']

        #raw_schedules = [doc for doc in db[rawCollection].find().limit(5000)]
        #print("Found {} distinct airtravel routes".format(len(raw_routes)))


        ### Embed Airports to Routes
        #portEmbeddedRoutes = []
        if argv.detailed_routes or argv.full:
            db['detailed_routes'].drop_indexes()
            db['detailed_routes'].drop()
            db['detailed_routes'].create_index("route", unique = True)
            raw_routes = [doc for doc in db['routes'].find()] 
            for route in raw_routes:
                tmpRoute = {}
                if db['airports'].count_documents({"iata" : route['origin']}) == 1:
                    orgPort = db['airports'].find_one({"iata" : route['origin']})
                else:
                    print("Found {} airports for {}".format(db['airports'].count_documents({"iata" : route['origin']}), route['origin']))
                
                if db['airports'].count_documents({"iata" : route['destination']}) == 1:
                    destPort = db['airports'].find_one({"iata" : route['destination']})
                else:
                    print("Found {} airports for {}".format(db['airports'].count_documents({"iata" : route['destination']}), route['destination']))
                
                tmpRoute['origin_airport'] = orgPort
                tmpRoute['destination_airport'] = destPort
                tmpRoute['route'] = route['origin'] + "-" + route['destination']
                tmpRoute['bearing'] = route['bearing']
                tmpRoute['direction'] = route['direction']
                tmpRoute['distance_calculated'] = route['distance_calculated']

                #pprint.pprint(tmpRoute)
                db['detailed_routes'].insert_one(tmpRoute)


        #### Detail flights
        #
        #
        #

        if argv.detailed_flights or argv.full:
            
            if argv.refresh:
                db['detailed_flights'].drop()

            if argv.restart:
                offset = db['detailed_flights'].count_documents({})
                print("restarting at offset: {}".format(offset))
            else:
                offset = argv.skip_records

            flights = db['detailed_flights']
            #raw_schedules = [doc for doc in db[rawCollection].find({}, batch_size = 10000)]
            raw_schedules = db[rawCollection].find({}, batch_size=10000).skip(offset)
            #raw_schedules = db[rawCollection].find({"metadata" : {"dst_sane" : {"sched_arrive" : False}}}, batch_size=10000)
            #raw_schedules = db[rawCollection].find_one()
            #pprint.pprint(raw_schedules)
            for schedule in raw_schedules:
                route = "{}-{}".format(schedule['origin'], schedule['destination'])
                #print("Route: {}".format(route))
                flight = {
                    "carrier" : schedule['carrier'],
                    "flight_num" : schedule['flight_num'],
                    "tail_num" : schedule['tail_num'],
                    "route" : db.detailed_routes.find_one({'route': route})
                }

                flight['route']['distance_recorded'] = schedule['distance']

                oTZ = flight['route']['origin_airport']['timezone']
                dTZ = flight['route']['destination_airport']['timezone']

                flight_times,metadata = GetFlightTimeData(schedule, oTZ, dTZ)
                flight_statistics,stat_meta = GetFlightStats(schedule, flight_times)

                metadata['missing'].update(stat_meta)

                record = {
                    'flight' : flight,
                    'times' : flight_times,
                    'statistics' : flight_statistics,
                    'metadata' : metadata
                }

                flights.insert_one(record)
                #pprint.pprint(record)
