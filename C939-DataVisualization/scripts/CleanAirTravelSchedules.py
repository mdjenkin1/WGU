""" 
    Scrub flight scheduling data after consumption of raw air travel csv files
"""

import os
import sys
import argparse
import pprint
import math

sys.path.append("./tools/")

from pymongo import MongoClient

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract and prepare historic air travel schedule information')
    #parser.add_argument('--airports', nargs='+', default=["SLC"])
    parser.add_argument('--mongo_host', default='localhost')
    parser.add_argument('--mongo_port', default=27017)
    parser.add_argument('--config_dir', default='./StaticFiles')
    argv = parser.parse_args()