#!/usr/bin/python

import csv
import re
import sys
import os
import pprint
import math

import datetime as dt

#rawDir = ("../processedData")
rawDir = ("../TestData")
cfgDir = ("./StaticFiles")
selectAirports = ['SLC']
processedData = []

fieldsToCopy = [
            # Day of the Week as ISO number.
            "DayOfWeek", 

            ### Flight Descriptors
            "Dest", "Origin", "Distance",
            "FlightNum", "TailNum", 
            #"UniqueCarrier", 
            

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
unknownCarriers = {}
distDiffs = {}

carriers = {}
airports = {}
legs = {}

flightTimes = {
    "Arr": "ActualArrive", 
    "Dep": "ActualDepart", 
    "CRSArr": "SchedArrive", 
    "CRSDep": "SchedDepart" 
}

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
                    "lat" : math.radians(float(row["lat"])),
                    "long" : math.radians(float(row["long"]))
                }
            })
        else:
            raise Exception("Unknown format: airport.csv")

#
def GetDirection(degree):
    compassPoints = (
        "North", "NorthEast",
        "East", "SouthEast",
        "South", "SouthWest",
        "West", "NorthWest"
    )
    dirIndex = round(degree * len(compassPoints) / 360) % len(compassPoints)
    return compassPoints[dirIndex]

# Use the Haversine formula to determine the distance and direction of travel
# https://www.movable-type.co.uk/scripts/latlong.html
def DescribeLeg(origin, dest):
    if origin not in airports or dest not in airports:
        raise Exception("Unknown airport. Cannot determine direction of travel.")

    # Radius of the earth in miles
    Radius = 3959

    # Origin longitude and latitude in radians
    oLat = airports[origin]["lat"]
    oLong = airports[origin]["long"]

    # Destination longitude and latitude in radians
    dLat = airports[dest]["lat"]
    dLong = airports[dest]["long"]
    
    # Delta longitude and latitude in radians
    deltaLat = dLat - oLat
    deltaLong = dLong - oLong

    # Haversine formula to calculate distance
    a = (math.sin(deltaLat/2))**2 + math.cos(oLat) * math.cos(dLat) * (math.sin(deltaLong/2))**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    calcDist = round(Radius * c)

    # Direction
    v1 = math.sin(deltaLong) * math.cos(dLat)
    v2 = math.cos(oLat) * math.sin(dLat) - math.sin(oLat) * math.cos(dLat) * math.cos(deltaLong)
    degHeading = round(math.atan2(v1, v2) * 180 / math.pi)
    #if degHeading < 0: degHeading += 360 

    direction = GetDirection(degHeading)

    outDict = {
        origin + "-" + dest : {
            "CalculatedDistance": calcDist,
            "Heading": degHeading,
            "DirectionOfTravel": direction
        }
    }

    return outDict

def SplitTime(timeInt):
    """Convert an integer representation of a 24hr time to a dictionary of hour and minute"""
     
    # Pad the integer as a 4 character string for the most predictable behavior
    timeMask = re.compile(r'(\d{2})(\d{2})')
    try:
        timeStr = str(int(timeInt)).zfill(4)
        timeParts = timeMask.match(timeStr)
        #print("Split {} into hour {} and min {} ".format(timeInt, timeParts[1], timeParts[2]))
    except:
        return {"Hour": "00", "Min": "00"}
    else:
        return {"Hour": timeParts[1], "Min": timeParts[2]}

def GetFlightStageDateTime(record, flightStage):
    #try:
    try:
        tmp_date = dt.datetime.strptime(record[flightStage[0]],"%Y-%m-%d")
        #pprint.pprint("Converted {} to date {}".format(record[flightStage[0]], tmp_date))
    except:
        tmp_date = dt.datetime()

    try:
        tmp_time = dt.datetime.strptime(str(record[flightStage[1]]), "%H:%M:%S").time()
        #pprint.pprint("Converted {} to time {}".format(record[flightStage[1]], tmp_time))
    except:
        tmp_time = dt.time()

    return dt.datetime.combine(tmp_date, tmp_time)   
    #return tmp_date
    #return tmp_time
    #except:
    #    return "NaN"
    #    pass
    #    print(sys.exc_info()[0])
    #else:
    #    return "NaN"
    #record[flightStage[0]], record[flightStage[1]])


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

                ## Leveraging airport codes
                if row["Origin"] not in airports.keys():
                    unknownCarriers.update({row["Origin"]: True})
                if row["Dest"] not in airports.keys():
                    unknownCarriers.update({row["Dest"]: True})

                # Ensure the source to destination journey leg has a description
                journeyLeg = row["Origin"] + "-" + row["Dest"]
                if journeyLeg not in legs:
                    legs.update(DescribeLeg(row["Origin"], row["Dest"]))
                # Add the journey leg description to our processed fields
                for field in legs[journeyLeg]:
                    processedFields.update({
                        field: legs[journeyLeg][field]
                    })

                # Compare the supplied distance to the calculated distance
                reportedDist = processedFields["Distance"]
                calculatedDist = processedFields["CalculatedDistance"]
                diffDist = abs(int(reportedDist) - int(calculatedDist))
                #print("There's {} miles difference between calculated and reported distance for {}".format(diffDist, journeyLeg))
                distDiffs.update({diffDist : True})

                tmpTime = {}
                for stage in flightTimes.keys():
                    tmpTime.update(SplitTime(row[stage+"Time"]))
                    if tmpTime["Hour"] == "24": tmpTime["Hour"] = 0
                    stageDateTime = dt.datetime(
                        year = int(row["Year"]), month = int(row["Month"]), day = int(row["DayofMonth"]),
                        hour = int(tmpTime["Hour"]), minute = int(tmpTime["Min"])
                    )
                    processedFields.update({ flightTimes[stage]: stageDateTime })

                if processedFields["ActualArrive"] < processedFields["ActualDepart"]:
                    processedFields.update({"ActualArrive": processedFields["ActualArrive"] + dt.timedelta(days=1)})

                if processedFields["SchedArrive"] < processedFields["SchedDepart"]:
                    processedFields.update({"SchedArrive": processedFields["SchedArrive"] + dt.timedelta(days=1)})

                processedData.append(processedFields)
                i += 1



                

for i in cancelledOrDiverted:
    pprint.pprint(processedData[i])
    print("\n")

for i in unknownCarriers:
    pprint.pprint(processedData[i])
    print("\n")

#pprint.pprint(distDiffs)

#pprint.pprint(legs)

pprint.pprint(processedData[385:389])