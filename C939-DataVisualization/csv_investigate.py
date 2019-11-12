#! /bin/python

import csv
import os
import pprint
import pickle
import re

import pandas as pd
import datetime as dt

from collections import Counter, namedtuple

#### Ghetto Script Control ####

# original counts and initial processing
getBasicCounts = False
pickleRaws = False

# run shortening for development
shortRun = True
stopAfter = 1

# airport customization
Airport = "SLC"

#### Globals ####

# Basic counts
if getBasicCounts:
    countsOrigin = Counter()
    countsDest = Counter()
    countsLink = {}

# Processed Dataframe
ord_df = pd.DataFrame()
selectedAirports_df = pd.DataFrame()


def InitialBasicCounts(csvFile):
    with open(csvFile) as openfile:
        airport = {}
        reader = csv.reader(openfile)
        header = True
        for row in reader:
            if header:
                fcnt = 0
                for field in row:
                    if field in ("Origin", "Dest"):
                        #print("{} is field {}".format(field, fcnt))
                        airport[field] = fcnt
                    fcnt += 1
                header = False
            else:
                countsOrigin[row[airport["Origin"]]] += 1
                countsDest[row[airport["Dest"]]] += 1
                if row[airport["Origin"]] in countsLink.keys():
                    countsLink[row[airport["Origin"]]][row[airport["Dest"]]] += 1
                else:
                    countsLink[row[airport["Origin"]]] = Counter()
                    countsLink[row[airport["Origin"]]][row[airport["Dest"]]] += 1

def CsvToPickledDataframe(csvFile):
    print("processing: {}".format(os.path.join("./RawData/", csvFile)))
    tmpdf = pd.read_csv(os.path.join("./RawData/", csvFile), encoding="ISO-8859-1")

    basename, _ = os.path.splitext(csvFile)
    outname = basename + "pkl"
    outfile = open(os.path.join("./pickles/", outname),'wb')
    pickle.dump(tmpdf, outfile)
    outfile.close

def IntToTime(intIn):
    try:
        intIn = int(intIn)
        timeMask = re.compile('(\d{2})(\d{2})')
        timeStr = str(intIn).zfill(4)
        timeParts = timeMask.match(timeStr)
        timeOut = dt.time(int(timeParts[1]), int(timeParts[2]))
        return timeOut
    except:
        #pprint.pprint("This can not be cast as an integer: {}".format(intIn))
        pass
    else:
        return "NaN"

def GetNextDay(today):
    tomorrow = today + dt.timedelta(days=1)
    return tomorrow

def IntOrNaN(value):
    try:
        return int(value)
    except:
        pass
    else:
        return "NaN"

def TimedeltaOrNaN(value):
    try:
        return(dt.timedelta(minutes=(int(value))))
    except:
        pass
    else:
        return "NaN"

def PrepForTableau(original_df):

    # Make a copy of the dataframe to ensure we know what's being modified and included
    columnsToCopy = [ 
        ## Datetimes should be date times
        #"Year", "Month", "DayofMonth", 
        #"DepTime", "CRSDepTime", 
        #"ArrTime", "CRSArrTime", 
        
        ## Distances in integer miles
        #"Distance"
        
        ## Minutes are a form of timedelta
        #"TaxiIn", "TaxiOut", 
        #"ActualElapsedTime", "CRSElapsedTime", "AirTime", 
        #"CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay" 
        #"ArrDelay", "DepDelay"

        "DayOfWeek", 
        "Origin", "Dest", 
        "UniqueCarrier", "FlightNum", "TailNum", 
        "Cancelled", "CancellationCode", "Diverted", 
    ]
    preped_df = original_df[columnsToCopy].copy()

    # Calculating dates
    preped_df['DepartDate'] = original_df.apply(lambda row: dt.date(row.Year, row.Month, row.DayofMonth), axis = 1)
    
    # Time is time
    clockTimes = ["DepTime", "CRSDepTime", "ArrTime", "CRSArrTime"]
    for ctime in clockTimes:
        preped_df[ctime] = original_df.apply(lambda row: IntToTime(row[ctime]), axis = 1)

    # Distances are integer miles, not floats
    preped_df['Distance'] = original_df.apply(lambda row: IntOrNaN(row['Distance']), axis = 1)

    # Timedeltas should be timedeltas
    measuredTimes = [
        "TaxiIn", "TaxiOut", "ActualElapsedTime", "CRSElapsedTime", "AirTime", "CarrierDelay", "WeatherDelay", 
        "NASDelay", "SecurityDelay", "LateAircraftDelay", "ArrDelay", "DepDelay" ]
    for mtime in measuredTimes:
        preped_df[mtime] = original_df.apply(lambda row: TimedeltaOrNaN(row[mtime]), axis = 1)


    """
    Work here next
    Calculate Arrival Dates
    """



    # if the arrival time is earlier than the departure time then the arrival date is the day after the departure date
    #nextDayArrivals = original_df['ArrTime'] < original_df['DepTime']

    #preped_df['ArriveTime'] = preped_df.apply(lambda row: print(row)
    #preped_df.apply(lambda row: pprint(row.index))
    
#    if nextDayArrivals.iloc(row.index): GetNextDay(row.DepartDate) else: row.DepartDate, axis = 1)

    #for rowIndex, arrNextDay in nextDayArrivals.iteritems():
    #    if arrNextDay:
    #        preped_df.loc[rowIndex, 'ArriveDate'] = GetNextDay(preped_df.loc[rowIndex, 'DepartDate'])
    #    else:
    #        preped_df.loc[rowIndex, 'ArriveDate'] = preped_df.loc[rowIndex, 'DepartDate']

    ### This is no good
    #preped_df['ArriveDate'] = [ \
    #    GetNextDay(preped_df['DepartDate']) if nextDay \
    #    else preped_df['DepartDate'] \
    #    for nextDay in nextDayArrivals \
    #]



            #print("Next Day Arrival: {} to {}".format(preped_df.loc[rowIndex, 'DepartDate'], GetNextDay(preped_df.loc[rowIndex, 'DepartDate'])))

            #preped_df.iloc[index, 'ArrivalDate'] = preped_df.iloc[index, 'DepartDate'] + dt.timedelta(days=1)
        #if index:
        #    print("Index: {}, arrNextDay: {}".format(index, arrNextDay))
    #preped_df.loc[nextDayArrival, 'ArriveDate'] = original_df.loc[nextDayArrival, ]


    #preped_df.loc[nextDayArrival, 'ArriveDate'] = preped_df.loc[nextDayArrival, 'DepartDate'] + dt.timedelta(days=1)
    #pprint.pprint(nextDayArrival)
    #preped_df.loc[nextDayArrival, 'ArriveDate'] = original_df.loc[nextDayArrivalDepartDate + dt.timedelta(days=1), axis = 1)


    #if original_df.loc['ArrTime'] < original_df.loc['DepTime']:
    #    = original_df.apply(lambda row: row.DepartDate + dt.timedelta(days=1), axis = 1)
    #else: 
    #    original_df['ArriveDate'] = original_df.DepartDate
    
    # Drop the raw date fields
    #original_df.drop(labels=['Year','Month','DayofMonth'])

    # fixing times
    #original_df['DepartTime'] = original_df.apply(lambda row: IntToTime(row['DepTime']), axis = 1)
    #original_df['SchDepartTime'] = original_df.apply(lambda row: IntToTime(row['CRSDepTime']), axis = 1)
    #irport_df['ArriveTime'] = original_df.apply(lambda row: IntToTime(row['ArrTime']), axis = 1)
    #original_df['SchArriveTime'] = original_df.apply(lambda row: IntToTime(row['CRSArrTime']), axis = 1)

    # Drop the raw time fields
    #original_df.drop(labels=['DepTime','CRSDepTime','ArrTime','CRSArrTime'])

    return preped_df

if pickleRaws | getBasicCounts:
    for csvFile in os.listdir("./RawData"):

        if pickleRaws:
            CsvToPickledDataframe(csvFile)
        
        if getBasicCounts:
            InitialBasicCounts(os.path.join("./RawData/", csvFile))
            #pprint.pprint(countsLink)
            #pprint.pprint(countsOrigin.most_common(10))
            #pprint.pprint(countsDest.most_common(10))
            print("Salt Lake City had: {} flights leave.".format(countsOrigin['SLC']))
            print("Salt Lake City had: {} flights arrive.".format(countsDest['SLC']))
            print("ord had: {} flights leave.".format(countsOrigin['ORD']))
            print("ord had: {} flights arrive.".format(countsDest['ORD']))
            print("{} flights from SLC went to ORD".format(countsLink['SLC']['ORD']))
            print("{} flights from ORD went to SLC".format(countsLink['ORD']['SLC']))

for pickled in os.listdir("./pickles"):
    # Orlando specific. Saved for posterity
    if (False):
        print("Processing: {}".format(pickled))
        tmp_df = pd.read_pickle(os.path.join("./pickles/", pickled))
        to_ord = tmp_df['Dest'] == "ORD"
        from_ord = tmp_df['Origin'] == "ORD"
        ord_df = pd.concat([ord_df, tmp_df[to_ord | from_ord]], sort=True)
        
    # Preprocess for selected airports
    if (stopAfter > 0):
        if shortRun: stopAfter -= 1

        print("Processing: {}".format(pickled))

        tmp_df = pd.read_pickle(os.path.join("./pickles/", pickled))
        dest_port = tmp_df['Dest'] == Airport
        from_port = tmp_df['Origin'] == Airport
        processed_df = PrepForTableau(tmp_df.loc[dest_port | from_port].copy())
        #pprint.pprint(processed_df)
        selectedAirports_df = pd.concat([selectedAirports_df, processed_df], sort=True)
    else: break


# Orlando
#pprint.pprint(ord_df)
#pprint.pprint(ord_df.describe())
#ord_df.to_csv("Orlando.csv")

# Selected Airports
#pprint.pprint(selectedAirports_df)
#pprint.pprint(selectedAirports_df.describe())
#selectedAirports_df.to_csv("SelectedAirports.csv")


