#!/usr/bin/python

""" Extract and homogenize historical air travel information from RITA """

"""
    Load data to local MongoDB instance
"""

"""
    Original plan
    Data Returned as CSV with the following fields
        * Scheduled Departure Datetime (%Y-%m-%d %H:%M) in UTC
        * Scheduled Arrival Datetime (%Y-%m-%d %H:%M) in UTC
        * Origin Airport IATA code
        * Origin Airport City
        * Origin Airport State
        * Origin Airport Country
        * Destination Airport IATA code
        * Destination Airport City
        * Destination Airport State
        * Destination Airport Country
        * Carrier Code
        * Carrier
        * Distance traveled

        * Flight departed late (if known), How late was it
        * Flight arrived late (if known), How late was it
        * Flight was cancelled, why? (if known)
        * Flight was diverted
"""


import os
import sys
import argparse
import pickle
import csv
import math

import pprint

sys.path.append("./tools/")
import air_journey_describer
import dst_asylum
from timezonefinder import TimezoneFinder

cfgDir = "./StaticFiles"

def generate_airport_info_pickle(file="airports.pkl"):
    """ 
        generate a dictionary of reference airport information
        pickle it so we don't need to keep recreating it

        iata: 
            airport
            city
            state
            country
            lat
            long
            timezone
    """

    airports = {}
    tf = TimezoneFinder(in_memory=True)

    with open(os.path.join(cfgDir, "airports.csv"), 'r') as inFile:
        reader = csv.DictReader(inFile)
        for row in reader:
            # Determine the timezone of the airport
            timezone = tf.timezone_at(lng=float(row["long"]), lat=float(row["lat"]))
            if not timezone:
                # Timezonefinder does not include the Pacific ocean. This a manual correction.
                OlsenTz = "Pacific/Samoa" if row["iata"] in ("Z08", "PPG", "FAQ") else "Pacific/Saipan"
            
            airports.update({
                row["iata"]: {
                    "airport": row["airport"],
                    "city" : row["city"],
                    "state" : row["state"],
                    "country" : row["country"],
                    "lat" : math.radians(float(row["lat"])),
                    "long" : math.radians(float(row["long"])),
                    "timezone" : timezone }
            })
    
    outfile = open(os.path.join(cfgDir, file), 'wb')
    pickle.dump(airports, outfile)
    outfile.close()

def get_airport_schedule(ports):
    print("received airports: {}".format(ports))
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract and prepare historic air travel schedule information')
    parser.add_argument('--airports', nargs='+', default=["SLC"])
    argv = parser.parse_args()

    # load airport definitions
    if not os.path.exists(os.path.join(cfgDir, "airports.pkl")):
        print("Airport definitions file not found. Recreating from csv")
        generate_airport_info_pickle()
    airport_pkl = open(os.path.join(cfgDir, "airports.pkl"), 'rb')
    airport_info = pickle.load(airport_pkl)
    airport_pkl.close()

    get_airport_schedule(argv.airports)