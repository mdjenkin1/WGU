#! /bin/python

import csv
import os
import pprint
import pickle
import re

import pandas as pd
import numpy as np
import datetime as dt

from collections import Counter, namedtuple

cntsOrigin = Counter()
cntsDest = Counter()
cntsLink = {}

# dataframe out
ord_df = pd.DataFrame()
slc_df = pd.DataFrame()

def BasicCounts(csvfile):
    with open(csvfile) as openfile:
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
                cntsOrigin[row[airport["Origin"]]] += 1
                cntsDest[row[airport["Dest"]]] += 1
                if row[airport["Origin"]] in cntsLink.keys():
                    cntsLink[row[airport["Origin"]]][row[airport["Dest"]]] += 1
                else:
                    cntsLink[row[airport["Origin"]]] = Counter()
                    cntsLink[row[airport["Origin"]]][row[airport["Dest"]]] += 1

def PickleFile(csvfile):
    print("processing: {}".format(os.path.join("./RawData/", csvfile)))
    tmpdf = pd.read_csv(os.path.join("./RawData/", csvfile), encoding="ISO-8859-1")

    basename, _ = os.path.splitext(csvfile)
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

for csvfile in os.listdir("./RawData"):

    if(False):
        PickleFile(csvfile)
    
    if(False):
        BasicCounts(os.path.join("./RawData/", csvfile))
        #pprint.pprint(cntsLink)
        #pprint.pprint(cntsOrigin.most_common(10))
        #pprint.pprint(cntsDest.most_common(10))
        print("Salt Lake City had: {} flights leave.".format(cntsOrigin['SLC']))
        print("Salt Lake City had: {} flights arrive.".format(cntsDest['SLC']))
        print("ord had: {} flights leave.".format(cntsOrigin['ORD']))
        print("ord had: {} flights arrive.".format(cntsDest['ORD']))
        print("{} flights from SLC went to ORD".format(cntsLink['SLC']['ORD']))
        print("{} flights from ORD went to SLC".format(cntsLink['ORD']['SLC']))

stopAfter = 1
for pickled in os.listdir("./pickles"):
    
        # Orlando
    if (False):
        print("Processing: {}".format(pickled))
        tmp_df = pd.read_pickle(os.path.join("./pickles/", pickled))
        to_ord = tmp_df['Dest'] == "ORD"
        from_ord = tmp_df['Origin'] == "ORD"
        ord_df = pd.concat([ord_df, tmp_df[to_ord | from_ord]], sort=True)
        
        # Salt Lake City
    if (stopAfter > 0):
        stopAfter -= 1
        print(stopAfter)
        print("Processing: {}".format(pickled))

        tmp_df = pd.read_pickle(os.path.join("./pickles/", pickled))
        to_slc = tmp_df['Dest'] == "SLC"
        from_slc = tmp_df['Origin'] == "SLC"
        processed_df = PrepForTableau(tmp_df.loc[to_slc | from_slc].copy())
        pprint.pprint(processed_df)
        slc_df = pd.concat([slc_df, processed_df], sort=True)
    else: break


# Orlando
#pprint.pprint(ord_df)
#pprint.pprint(ord_df.describe())
#ord_df.to_csv("Orlando.csv")

# Salt Lake City
#pprint.pprint(slc_df)
#pprint.pprint(slc_df.describe())
#slc_df.to_csv("SaltLake.csv")


