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
            "FlightNum", "TailNum", "UniqueCarrier", 
            "Dest", "Origin", "Distance", 

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

carriers = {}

# carriers.csv file obtained from http://stat-computing.org/dataexpo/2009/carriers.csv
with open(os.path.join(cfgDir, "carriers.csv"), 'r') as inFile:
    reader = csv.DictReader(inFile)
    for row in reader:
        if "Code" in row and "Description" in row:
            carriers.update(row["Code"], row["Description"])
        else:
            raise Exception("Unknown format: carriers.csv")

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
                    cancelledOrDiverted.append(i)
                    #print("Diverted {}".format(row["CancellationCode"]))
                    processedFields.update({"Diverted" : True})
                else: processedFields.update({"Diverted" : False})

                if row["TailNum"] == "NA":
                    processedFields.update({"TailNum": "Unknown"})
                else processedFields.update({"TailNum": row["TailNum"]})

                #processedData.append(row)
                processedData.append(processedFields)
                i +=1

for i in cancelledOrDiverted:
    pprint.pprint(processedData[i])
    print("\n")