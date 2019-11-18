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

intermediatePkl = "selectedAirports"

raw_df = pd.DataFrame()
working_df = pd.DataFrame()

def DataFramePickler(gherkin_df, outFile, pklPath=picklePath):
    basename, _ = os.path.splitext(outFile)
    outname = basename + ".pkl"
    outfile = open(os.path.join(pklPath, outname),'wb')
    pickle.dump(gherkin_df, outfile)
    outfile.close

# load the raw CSVs to a dataframe, extract only the airports of interest
print("Loading raw csv files")
for csvFile in os.listdir(rawsPath):
    currentRaw = os.path.join(rawsPath, csvFile)
    print("processing: {}".format(currentRaw))
    tmpdf = pd.read_csv(currentRaw, encoding="ISO-8859-1", low_memory=False)
    dest_port = tmpdf['Dest'].isin(selectAirports)
    from_port = tmpdf['Origin'].isin(selectAirports)
    raw_df = pd.concat([raw_df, tmpdf[dest_port | from_port]], sort=True)

intermediatePkl = os.path.join(picklePath, intermediatePkl + ".pkl")
print("Saving selected airport records as intermediate pickled dataframe: {}".format(intermediatePkl))
DataFramePickler(raw_df, intermediatePkl)