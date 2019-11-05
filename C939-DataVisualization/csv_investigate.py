#! /bin/python

import csv
import os
import pprint
from collections import Counter

cntsOrigin = Counter()
cntsDest = Counter()
cntsLink = {}


for csvfile in os.listdir("./RawData"):
    print("processing: {}".format(os.path.join("./RawData/", csvfile)))
    with open(os.path.join("./RawData/", csvfile)) as openfile:
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

#pprint.pprint(cntsLink)
#pprint.pprint(cntsOrigin.most_common(10))
#pprint.pprint(cntsDest.most_common(10))

print("Salt Lake City had: {} flights leave.".format(cntsOrigin['SLC']))
print("Salt Lake City had: {} flights arrive.".format(cntsDest['SLC']))

print("Orlando had: {} flights leave.".format(cntsOrigin['ORD']))
print("Orlando had: {} flights arrive.".format(cntsDest['ORD']))

print("{} flights from SLC went to ORD".format(cntsLink['SLC']['ORD']))
print("{} flights from ORD went to SLC".format(cntsLink['ORD']['SLC']))

