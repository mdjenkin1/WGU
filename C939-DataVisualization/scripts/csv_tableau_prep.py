#!/usr/bin/python

import csv
import re
import sys
import os
import pprint

#rawDir = ("../processedData")
rawDir = ("../TestData")
cfgDir = ("./StaticFiles")
selectAirports = ['SLC']
processedData = []

fieldsToCopy = [
            # Day of the Week as ISO number.
            "DayOfWeek", 

            ### Flight Descriptors
            #"Dest", "Origin",
            #"TailNum", "UniqueCarrier", 
            "FlightNum", "Distance"
            

            ### Modified flight plan
            #"CancellationCode", "Cancelled",
            #"Diverted"
]

cancelCodes = {
    "A" : "Carrier", 
    "B" : "Weather", 
    "C" : "NAS", 
    "D" : "Security"
}

cancelledOrDiverted = []
unknownCarriers = []

carriers = {}
airports = {}

# carriers.csv file obtained from http://stat-computing.org/dataexpo/2009/carriers.csv
with open(os.path.join(cfgDir, "carriers.csv"), 'r') as inFile:
    reader = csv.DictReader(inFile)
    for row in reader:
        if "Code" in row and "Description" in row:
            carriers.update({row["Code"]: row["Description"]})
        else:
            raise Exception("Unknown format: carriers.csv")

# airports.csv file obtained from http://stat-computing.org/dataexpo/2009/airports.csv
with open(os.path.join(cfgDir, "airports.csv"), 'r') as inFile:
    reader = csv.DictReader(inFile)
    for row in reader:
        if "iata" in row \
        and "airport" in row\
        and "city" in row\
        and "state" in row\
        and "country" in row\
        and "lat" in row\
        and "long" in row:
            airports.update({
                row["iata"]: {
                    "airport": row["airport"],
                    "city" : row["city"],
                    "state" : row["state"],
                    "country" : row["country"],
                    "lat" : row["lat"],
                    "long" : row["long"]
                }
            })
        else:
            raise Exception("Unknown format: airport.csv")

# Use the Haversine formula to determine the distance and direction of travel
# https://www.movable-type.co.uk/scripts/latlong.html
def GetDirectionOfTravel(origin, dest):
    if origin not in airports or dest not in airports:
        raise Exception("Unknown airport. Cannot determine direction of travel.")

    airports[origin]["lat"]
    airports[origin]["long"]
    airports[dest]["lat"]
    airports[dest]["long"]
    return "North"

for csvFile in os.listdir(rawDir):
    print("processing {}".format(csvFile))
    with open(os.path.join(rawDir, csvFile), 'r') as inFile:
        reader = csv.DictReader(inFile)
        i = 0
        for row in reader:
            processedFields = {}
            if row["Origin"] in selectAirports or row["Dest"] in selectAirports:
                processedFields.update({field: row[field] for field in fieldsToCopy if field in row})
                
                # Replace cancelled codes with cancelled verbiage if available
                if row["Cancelled"] == "1":
                    #cancelledOrDiverted.append(i)
                    #print("Cancelled {}".format(row["CancellationCode"]))
                    if "CancellationCode" in row and row["CancellationCode"] in cancelCodes:
                        #cancelledOrDiverted.append(i)
                        #print("Cancelled {}".format(row["Cancelled"]))
                        processedFields.update({"Cancelled" : cancelCodes[row["CancellationCode"]]})
                    else: 
                        processedFields.update({"Cancelled": True})
                else: processedFields.update({"Cancelled" : False})

                # Diverted as boolean
                if row["Diverted"] == "1":
                    #cancelledOrDiverted.append(i)
                    #print("Diverted {}".format(row["CancellationCode"]))
                    processedFields.update({"Diverted" : True})
                else: processedFields.update({"Diverted" : False})

                # Tail Numbers, NA is Unknown
                if row["TailNum"] == "NA":
                    processedFields.update({"TailNum": "Unknown"})
                else: processedFields.update({"TailNum": row["TailNum"]})

                # Carriers and their codes
                if row["UniqueCarrier"] not in carriers:
                    print("Unknown carrier code: {}".format(row["UniqueCarrier"]))
                    processedFields.update({
                        "CarrierCode" : row["UniqueCarrier"],
                        "Carrier" : "Unknown"
                    })
                else:
                    processedFields.update({
                        "CarrierCode" : row["UniqueCarrier"],
                        "Carrier" : carriers[row["UniqueCarrier"]]
                    })

                # Managing airports codes

                #processedData.append(row)
                processedData.append(processedFields)
                i += 1

for i in cancelledOrDiverted:
    pprint.pprint(processedData[i])
    print("\n")

for i in unknownCarriers:
    pprint.pprint(processedData[i])
    print("\n")


pprint.pprint(processedData[66])