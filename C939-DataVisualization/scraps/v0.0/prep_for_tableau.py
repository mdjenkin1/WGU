import csv
import os
import sys
import pprint
import pickle
import re

import pandas as pd
import datetime as dt

from collections import Counter, namedtuple

selectAirports = ["SLC"]

rawsPath = "./RawData"
picklePath = "./pickles"

inprocessDf = "inprocessDf"

raw_df = pd.DataFrame()

def DataFramePickler(gherkin_df, outFile, pklPath=picklePath):
    basename, _ = os.path.splitext(outFile)
    outname = basename + ".pkl"
    outfile = open(os.path.join(pklPath, outname),'wb')
    pickle.dump(gherkin_df, outfile)
    outfile.close

def SplitTime(intIn):
    timeMask = re.compile('(\d{2})(\d{2})')
    try:
        timeStr = str(int(intIn)).zfill(4)
        timeParts = timeMask.match(timeStr)

        return [int(timeParts.group(1)),int(timeParts.group(2))]
    except:
        return [0,0]
    else:
        return [0,0]

def GetNextDay(today):
    tomorrow = today + dt.timedelta(days=1)
    return tomorrow

def ArrivedNextDay(departDt, arriveDt):
    if departDt > arriveDt:
        arriveDt = arriveDt + dt.timedelta(days=1)
    return arriveDt

# load the raw CSVs to a dataframe, extract only the airports of interest
print("Loading raw csv files")
for csvFile in os.listdir(rawsPath):
    currentRaw = os.path.join(rawsPath, csvFile)
    print("processing: {}".format(currentRaw))
    tmpdf = pd.read_csv(currentRaw, encoding="ISO-8859-1", low_memory=False)
    dest_port = tmpdf['Dest'].isin(selectAirports)
    from_port = tmpdf['Origin'].isin(selectAirports)
    raw_df = pd.concat([raw_df, tmpdf[dest_port | from_port]], sort=True)

intermediatePkl = os.path.join(picklePath, inprocessDf + ".pkl")
print("Saving selected airport records as intermediate pickled dataframe: {}".format(intermediatePkl))
DataFramePickler(raw_df, inprocessDf)

# Columns to be copied without modification, Tableau should be able to handle these
columnsToCopy = [
            # Day of the Week as ISO number.
            "DayOfWeek", 

            ### Flight Descriptors
            "FlightNum", "TailNum", "UniqueCarrier", 
            "Dest", "Origin", "Distance", 

            ### Modified flight plan
            "CancellationCode", "Cancelled", "Diverted",
]

#print("Copying {} to working dataframe".format(columnsToCopy))
#working_df = raw_df[columnsToCopy].copy()



# Time is time
#clockTimes = ["Dep", "CRSDep", "Arr", "CRSArr"]
#for ctime in clockTimes:
#    print("Preparing {}".format(ctime + "Time"))
#    raw_df[[ctime + "Hour", ctime + "Min"]] = pd.DataFrame(raw_df.apply(lambda row: SplitTime(row[ctime + "Time"]), axis = 1).values.tolist())#
#
#    print("Calculating {} datetime".format(ctime + "DateTime"))
#    working_df[ctime + "DateTime"] = pd.to_datetime({
#        'year': raw_df['Year'],
#        'month': raw_df['Month'],
#        'day': raw_df['DayofMonth'],
#        'hour': raw_df[ctime+ "Hour"],
#        'minute': raw_df[ctime + "Min"]
#    })

#print("Preparing arrival time")
#raw_df['ArrHour'], raw_df['ArrMin'] = raw_df.apply(SplitTime(raw_df['ArrTime']))
#print("Preparing departure time")
#raw_df['DepHour', 'DepMin'] = raw_df.apply(SplitTime(raw_df['ArrTime']))

#print("Determining which flights arrived the next day")


pprint.pprint(raw_df)
pprint.pprint(working_df)