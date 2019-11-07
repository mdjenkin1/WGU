#! /bin/python

import csv
import os
import pprint
import pickle
import re

import pandas as pd
import datetime as dt

from collections import Counter

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
    timeMask = re.compile('(\d{2})(\d{2})')
    timeStr = str(int(intIn)).zfill(4)
    timeParts = timeMask.match(timeStr)
    timeOut = datetime.time(timeParts[1], timeParts[2]) 
    return timeOut

def PrepForTableau(airport_df):
    # Making Dates
    airport_df['Depart Date'] = dt.date(airport_df['Year'], airport_df['Month'], airport_df['DayofMonth'])
    
    # if the arrival time is earlier than the departure time then the arrival date is the day after the departure date
    #if airport_df['ArrTime'] < airport_df['DepTime']:
    #    airport_df['Arrive Date'] = airport_df['Depart Date'] + dt.timedelta(days=1)
    #else: airport_df['Arrive Date'] = airport_df['Depart Date']
    
    # Drop the raw date fields
    airport_df.drop(labels=['Year','Month','DayofMonth'])

    # fixing times
    #airport_df['DepartTime'] = IntToTime(airport_df['DepTime'])
    #airport_df['SchDepartTime'] = IntToTime(airport_df['CRSDepTime'])
    #airport_df['ArriveTime'] = IntToTime(airport_df['ArrTime'])
    #airport_df['SchArriveTime'] = IntToTime(airport_df['CRSArrTime'])

    # Drop the raw time fields
    airport_df.drop(labels=['DepTime','CRSDepTime','ArrTime','CRSArrTime'])

    return airport_df

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


for pickled in os.listdir("./pickles"):
    #print("Processing: {}".format(pickled))
    tmp_df = pd.read_pickle(os.path.join("./pickles/", pickled))
    
    # Orlando
    to_ord = tmp_df['Dest'] == "ORD"
    from_ord = tmp_df['Origin'] == "ORD"
    ord_df = pd.concat([ord_df, tmp_df[to_ord | from_ord]])
    
    # Salt Lake City
    to_slc = tmp_df['Dest'] == "SLC"
    from_slc = tmp_df['Origin'] == "SLC"
    slc_df = pd.concat([slc_df, tmp_df[to_slc | from_slc]])
    slc_df = PrepForTableau(slc_df)

# Orlando
#pprint.pprint(ord_df)
#pprint.pprint(ord_df.describe())
#ord_df.to_csv("Orlando.csv")

# Salt Lake City
#pprint.pprint(slc_df)
#pprint.pprint(slc_df.describe())
#slc_df.to_csv("SaltLake.csv")


