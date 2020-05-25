#!\usr\bin\python

"""
Load Airport data to mongodb
"""

import os
import csv
import math

from timezonefinder import TimezoneFinder

def consume_airport_csv(file="airports"):
    """ 
        load airport information from csv.
        determine timezones for each airport.
        return a list of dictionaries with the keys: iata, airport, city, state, country, lat, long, timezone
    """

    airports = []
    tf = TimezoneFinder(in_memory=True)

    with open(file, 'r') as inFile:
        reader = csv.DictReader(inFile)
        for row in reader:
            # Determine the timezone of the airport
            timezone = tf.timezone_at(lng=float(row["long"]), lat=float(row["lat"]))

            if not timezone:
                # Timezonefinder does not include the Pacific ocean. This a manual correction.
                # "FAQ","PPG","Z08" : Pacific/Samoa
                # "GRO","GSN","GUM","TNI","TT01" : Pacific/Saipan
                timezone = "Pacific/Samoa" if row["iata"] in ("Z08", "PPG", "FAQ") else "Pacific/Saipan"
            
            airports.append({
                'iata': row['iata'],
                'airport': row['airport'],
                'city' : row['city'],
                'state' : row['state'],
                'country' : row['country'],
                'lat' : float(row['lat']),
                'long' : float(row['long']),
                'timezone' : timezone })
    return airports