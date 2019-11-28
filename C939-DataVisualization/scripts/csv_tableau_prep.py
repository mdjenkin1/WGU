#!/usr/bin/python

import csv
import re
import sys
import os
import pprint
import math

import datetime as dt
import time
import pytz

from pytz import timezone
from timezonefinder import TimezoneFinder

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
    degBearing = round(math.atan2(v1, v2) * 180 / math.pi)
    #if degBearing < 0: degBearing += 360 

    direction = GetDirection(degBearing)

    oTz = tf.timezone_at(lng=oLong, lat=oLat)
    dTz = tf.timezone_at(lng=dLong, lat=dLat)

    outDict = {
        origin + "-" + dest : {
            "CalculatedDistance": calcDist,
            "Bearing": degBearing,
            "DirectionOfTravel": direction,
            "EstTimeZonesCrossed": 24
        }
    }

    return outDict

def NextDayArrival(departDt, arriveDt, estTzCrossed, bearing, estTime):
    # Guestimate how many timezones we're going to cross
    # simple trig on 

    return False

#rawDir = ("../RawData")
rawDir = ("../TestData")
cfgDir = ("./StaticFiles")
selectAirports = ['SLC']
processedData = []

dtOutString = "%Y-%m-%d %H:%M"

outDir = ("../PreprocessedData")
airportsStr = "_".join(selectAirports)
csvOut = "preparedFlightData" + airportsStr

fieldsToCopy = [
            # Day of the Week as ISO number.
            #"DayOfWeek", 

            ### Flight Descriptors
            "Dest", "Origin", "Distance",
            "FlightNum", "TailNum", 
            #"UniqueCarrier", 
            
            ### In Minutes
            # Delays
            "CarrierDelay", "WeatherDelay", "NASDelay", 
            "SecurityDelay", "LateAircraftDelay",
            # Travel time
            #"ActualElapsedTime", "AirTime", "CRSArrTime"

            ### Modified flight plan
            #"CancellationCode", "Cancelled",
            #"Diverted"
]
fieldsToWrite = set()

cancelCodes = {
    "A" : "Carrier", 
    "B" : "Weather", 
    "C" : "NAS", 
    "D" : "Security"
}

cancelledOrDiverted = []


flightTimeNames = {
    "Arr": "ActualArrive", 
    "Dep": "ActualDepart", 
    "CRSArr": "SchedArrive", 
    "CRSDep": "SchedDepart" 
}


carriers = {}
# carriers.csv file obtained from http://stat-computing.org/dataexpo/2009/carriers.csv
with open(os.path.join(cfgDir, "carriers.csv"), 'r') as inFile:
    reader = csv.DictReader(inFile)
    for row in reader:
        if "Code" in row and "Description" in row:
            carriers.update({row["Code"]: row["Description"]})
        else:
            raise Exception("Unknown format: carriers.csv")

airports = {}
airportTimeZones = {}
airportTimeZoneNames = set(["Pacific/Samoa", "Pacific/Saipan"])
# airports.csv file obtained from http://stat-computing.org/dataexpo/2009/airports.csv
with open(os.path.join(cfgDir, "airports.csv"), 'r') as inFile:
    
    # Data validation construct
    unknownCarriers = {}

    tf = TimezoneFinder(in_memory=True)
    reader = csv.DictReader(inFile)
    for row in reader:
        if "iata" in row \
        and "airport" in row\
        and "city" in row\
        and "state" in row\
        and "country" in row\
        and "lat" in row\
        and "long" in row:

            OlsenTz = tf.timezone_at(lng=float(row["long"]), lat=float(row["lat"]))

            # Timezonefinder does not include the Pacific ocean. This a manual correction.
            if not OlsenTz: 
                #print("Null timezone at airport {} Long: {} Lat: {}".format(row["iata"], row["long"], row["lat"]))
                OlsenTz = "Pacific/Samoa" if row["iata"] in ("Z08", "PPG", "FAQ") else "Pacific/Saipan"

            #airportTimeZoneNames.update([OlsenTz])

            airports.update({
                row["iata"]: {
                    "airport": row["airport"],
                    "city" : row["city"],
                    "state" : row["state"],
                    "country" : row["country"],
                    "lat" : math.radians(float(row["lat"])),
                    "long" : math.radians(float(row["long"])),
                    "OlsenTz" : OlsenTz
                }
            })
        else:
            raise Exception("Unknown format: airport.csv")

# take a sample of our airport dictionary for visual inspection
if False:
    for key in list(airports.keys())[53:57]: pprint.pprint(airports[key]) 
else: print("airports loaded")

utc = pytz.utc

# There is no reason to recalculate the journey from one airport to another more than once
legs = {}

for csvFile in os.listdir(rawDir):
    print("processing {}".format(csvFile))
    with open(os.path.join(rawDir, csvFile), 'r') as inFile:
        reader = csv.DictReader(inFile)
        i = 0
        distDiffs = set()
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
                try:
                    reportedDist = int(processedFields["Distance"])
                    calculatedDist = int(processedFields["CalculatedDistance"])
                    diffDist = abs(reportedDist - calculatedDist)
                    #print("There's {} miles difference between calculated and reported distance for {}".format(diffDist, journeyLeg))
                    distDiffs.add(diffDist)
                except ValueError:
                    pass
                
                ### Datetime calculations
                #print("Flying from {} to {}".format(row['Origin'],row['Dest']))
                tmpDT = {}
                
                # Provided date is assumed scheduled depart date
                tmpDT['RawDate'] = dt.datetime(year = int(row["Year"]), month = int(row["Month"]), day = int(row["DayofMonth"]))
                tmpDT['schDepTm'] = dt.datetime.strptime(row['CRSDepTime'].zfill(4),"%H%M").time()
                tmpDT['naiveSchDep'] = dt.datetime.combine(tmpDT['RawDate'], tmpDT['schDepTm'])
                tmpDT['depTz'] = pytz.timezone(airports[row['Origin']]['OlsenTz'])
                tmpDT['SchDep'] = tmpDT['depTz'].localize(tmpDT['naiveSchDep'])
                tmpDT['SchedDepart'] = tmpDT['SchDep'].astimezone(utc)

                # Are scheduled arrival time and elapsed time sane
                tmpDT['schArrTm'] = dt.datetime.strptime(row['CRSArrTime'].zfill(4),"%H%M").time()
                tmpDT['naiveSchArr'] = dt.datetime.combine(tmpDT['RawDate'], tmpDT['schArrTm'])
                tmpDT['SchTime'] = dt.timedelta(minutes=int(row['CRSElapsedTime']))
                
                # Determine next day arrival before localizing the arrival datetime.
                while (NextDayArrival(tmpDT['naiveSchDep'], tmpDT['naiveSchArr'], legs[journeyLeg]['EstTimeZonesCrossed'], legs[journeyLeg]['Bearing'], tmpDT['SchTime'])):
                    tmpDT['naiveSchArr'] = tmpDT['naiveSchArr'] + dt.timedelta(days=1)

                tmpDT['arrTz'] = pytz.timezone(airports[row['Dest']]['OlsenTz'])
                tmpDT['SchArr'] = tmpDT['arrTz'].localize(tmpDT['naiveSchArr'])
                tmpDT['SchedArrive'] = tmpDT['SchArr'].astimezone(utc)
                
                tmpDT['CalcSchTime'] = tmpDT['SchedArrive'] - tmpDT['SchedDepart']



                #print("Scheduled depart at {} local {} UTC".format(tmpDT['SchDep'], tmpDT['SchedDepart']))
                #print("Scheduled arrive at {} local {} UTC".format(tmpDT['SchArr'], tmpDT['SchedArrive']))

                # If it thinks we traveled backwards in time, add one day.
                # This is because the clock restarts at midnight.
                while (tmpDT['CalcSchTime'] < dt.timedelta()):
                    tmpDT['SchedArrive'] = tmpDT['SchedArrive'] + dt.timedelta(days=1)
                    tmpDT['CalcSchTime'] = tmpDT['SchedArrive'] - tmpDT['SchedDepart']
                    #print("Added a day to arrival for sanity {}".format(tmpDT['SchedArrive']))
                
                # 2003 DST dates, logic check
                dstStart = dt.datetime(year=2003,month=4,day=6,hour=3)
                dstEnd = dt.datetime(year=2003,month=10,day=26,hour=1)
                # Set date ranges around daylight savings time
                dstRng = tmpDT['SchTime'] + dt.timedelta(hours=1)
                dstStartTop = dstStart + dstRng
                dstStartBottom = dstStart - dstRng
                dstEndTop = dstEnd + dstRng
                dstEndBottom = dstEnd - dstRng
                # if the local arrival or departure datetime is within 1 hour + the scheduled elapsed time of dst end/start times, show me
                if tmpDT['depTz'].localize(dstStartBottom) < tmpDT['SchDep'] < tmpDT['depTz'].localize(dstStartTop) or tmpDT['arrTz'].localize(dstStartBottom) < tmpDT['SchArr'] < tmpDT['arrTz'].localize(dstStartTop):
                    print("Nearing daylight savings")
                    print("Flying from {} to {}".format(row['Origin'], row['Dest']))
                    print("local depart time: {} Timezone: {}".format(tmpDT['SchDep'], tmpDT['SchDep'].tzinfo))
                    print("local arrive time: {} Timezone: {}".format(tmpDT['SchArr'], tmpDT['SchArr'].tzinfo))
                    print("depart time UTC: {}".format(tmpDT['SchedDepart']))
                    print("arrive time UTC: {}".format(tmpDT['SchedArrive']))
                    print("Calculated scheduled elapsed time: {}".format(tmpDT['CalcSchTime']))
                    print("Provided scheduled elapsed time: {}".format(tmpDT['SchTime']))
                    print("")
                if tmpDT['depTz'].localize(dstEndBottom) < tmpDT['SchDep'] < tmpDT['depTz'].localize(dstEndTop) or tmpDT['arrTz'].localize(dstEndBottom) < tmpDT['SchArr'] < tmpDT['arrTz'].localize(dstEndTop):
                    print("Ending daylight savings")
                    print("Flying from {} to {}".format(row['Origin'], row['Dest']))
                    print("local depart time: {} Timezone: {}".format(tmpDT['SchDep'], tmpDT['SchDep'].tzinfo))
                    print("local arrive time: {} Timezone: {}".format(tmpDT['SchArr'], tmpDT['SchArr'].tzinfo))
                    print("depart time UTC: {}".format(tmpDT['SchedDepart']))
                    print("arrive time UTC: {}".format(tmpDT['SchedArrive']))
                    print("Calculated scheduled elapsed time: {}".format(tmpDT['CalcSchTime']))
                    print("Provided scheduled elapsed time: {}".format(tmpDT['SchTime']))
                    print("")

                #print("Calculated scheduled elapsed time: {}".format(tmpDT['CalcSchTime']))
                #print("Provided scheduled elapsed time: {}".format(tmpDT['SchTime']))
                #print("")

                #pprint.pprint(tmpDT)

                #print("Depart local: {}".format(tmpDT['SchDep']))
                #print("Depart utc: {}".format(processedFields['SchedDepart']))

                # If only we had good time data to start with
                #for stage in flightTimes.keys():
                #    tmpTime = {}
                #    if row[stage+"Time"] != "NA":
                #        try:
                #            rawTime = int(row[stage+"Time"])
                #            tmpTime.update(SplitTime(rawTime))
                #            if tmpTime["Hour"] == 24: tmpTime.update({"Hour": 00})
                #            stageDateTime = dt.datetime(
                #                year = int(row["Year"]), month = int(row["Month"]), day = int(row["DayofMonth"]),
                #                hour = tmpTime["Hour"], minute = tmpTime["Min"]
                #            )
                #        except:
                #            print("row: {}\nTimeField: {}\nrawTime: {}\ntmpTime: {}\n".format(i, stage+"Time", rawTime, tmpTime))
                #            pprint.pprint(row)
                #            pprint.pprint(processedFields)
                #        else:
                #            processedFields.update({flightTimes[stage]: stageDateTime})
                #            processedFields.update({flightTimes[stage]+"Time": tmpTime["Hour"]*100 + tmpTime["Min"]})
                #    else:
                #        stageDateTime = dt.datetime(
                #            year = int(row["Year"]), month = int(row["Month"]), day = int(row["DayofMonth"])
                #        )
                #        processedFields.update({flightTimes[stage]: stageDateTime})
                #        processedFields.update({flightTimes[stage]+"Time": "NA"})

                #if processedFields["ActualArrive"] < processedFields["ActualDepart"]:
                #    processedFields.update({"ActualArrive": processedFields["ActualArrive"] + dt.timedelta(days=1)})

                #if processedFields["SchedArrive"] < processedFields["SchedDepart"]:
                #    processedFields.update({"SchedArrive": processedFields["SchedArrive"] + dt.timedelta(days=1)})

                #for stage in flightTimes.keys():
                #    processedFields.update({
                #        flightTimes[stage]: processedFields[flightTimes[stage]].strftime(dtOutString)
                #    })

                processedData.append(processedFields)
                #i += 1
                fieldsToWrite.update(list(processedFields.keys()))
            i += 1
        print("Differences in distances")
        pprint.pprint(distDiffs)

print("writing preprocessed data to csv")
#pprint.pprint(fieldsToWrite)
with open(os.path.join(outDir, csvOut)+".csv", 'w', newline='') as csvfile:
    print("fieldnames: {}".format(fieldsToWrite))
    writer = csv.DictWriter(csvfile, fieldnames = fieldsToWrite)
    
    writer.writeheader()
    for row in processedData:
        writer.writerow(row)

#for i in cancelledOrDiverted:
#    pprint.pprint(processedData[i])
#    print("\n")

#for i in unknownCarriers:
#    pprint.pprint(processedData[i])
#    print("\n")

#pprint.pprint(distDiffs)

#pprint.pprint(legs)

#pprint.pprint(processedData[385:389])