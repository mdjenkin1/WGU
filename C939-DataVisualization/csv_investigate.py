#! /bin/python

import csv
import os
import pprint
import pickle

import pandas as pd

from collections import Counter

cntsOrigin = Counter()
cntsDest = Counter()
cntsLink = {}
ord_df = pd.DataFrame()

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
    to_ord = tmp_df['Dest'] == "ORD"
    from_ord = tmp_df['Origin'] == "ORD"
    ord_df = pd.concat([ord_df, tmp_df[to_ord | from_ord]])

pprint.pprint(ord_df)
pprint.pprint(ord_df.describe())


