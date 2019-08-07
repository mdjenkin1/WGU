#!/usr/bin/python

""" 
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY"]["bonus"] = 5600000
    
"""

import pickle
import pprint
import re
import copy

######
# Variables
######

## Dataset
enron_data = pickle.load(open("../final_project/final_project_dataset.pkl"))
features_count={}
nan_count={}
quant_count={}
poi_names_ds = set()
ds_enron_poi = {}

## Manual Wrangle
name_file = open("../final_project/poi_names.txt", "rb")
person_parse = re.compile(r'^\((\w)\)\s*(.*)$')
poi_names_file = set()

######
# Print out findings
######
def print_report(poi, eds=enron_data, feat=features_count, nds=poi_names_ds, nfile=poi_names_file, nc=nan_count, qc=quant_count):
    print("Features and number of people with that feature")
    pprint.pprint(features_count)
    print("Count of people in dataset: {}".format(len(eds)))
    print("Count of features in dataset: {}".format(len(feat)))
    print("Count of POI from dataset: {}".format(len(nds)))
    print("Count of POI from manual investigation: {}".format(len(nfile)))
    print("Count of all POI: {}".format(len(poi)))
    print("James Prentice's stock holdings: {}".format(eds["PRENTICE JAMES"]['total_stock_value']))
    print("Wesley Colwell's emails to POI: {}".format(eds["COLWELL WESLEY"]['from_this_person_to_poi']))
    print("Jeffery K Skilling's Exercised Stock Options: {}".format(eds["SKILLING JEFFREY K"]['exercised_stock_options']))
    print("Number of people with a quantified salary: {}".format(qc['salary']))
    print("Number of people with an email address: {}".format(qc['email_address']))

######
# Dataset Exploration
######
for key in enron_data:
    for k in enron_data[key]:
        features_count[k] = features_count.get(k, 0) + 1                                    # Add To the list of features
                                                                                            # maintain a count of feature occurrences
        if enron_data[key][k] == 'NaN':
            nan_count[k] = nan_count.get(k, 0) + 1
        else:
            quant_count[k] = quant_count.get(k, 0) + 1

    if (enron_data[key]["poi"]):                                                            # Do we have a person of interest
        #poi_names_ds.add(key)                                                              # Add them to the list (unmodified)
        poi_names_ds.add(re.sub(r'\s\b\w\b| JR','',key).upper())                            # Add them to the list (modified)
                                                                                            # Drop any initial, Remove the "JR" designation, ensure uppercasing
        ds_enron_poi.update({key : enron_data[key]})                                                # slice of dataset where 

######
# Manually Wrangled Data Exploration
######
for line in name_file:
    person_details = person_parse.match(line)                                               # Does the line match the record of a person?
    if person_details:                                                                      # If there is a person
        #poi_names_file.add(person_details.group(2))                                         # add their names to the list (unmodified)
        poi_names_file.add(re.sub('[,]', '', person_details.group(2).upper().strip()))      # add their to the list (modified)
                                                                                            # strip any leading or trailing whitespace characters from their name
                                                                                            # remove any commas, and convert their name to uppercase
######
# Findings Report
######

poi_names_all = poi_names_ds|poi_names_file                                                 # Combine the lists of people of interest
print_report(poi_names_all)

######
# Of the top executives, who had the highest payment?
######
top_execs = ('LAY KENNETH L','SKILLING JEFFREY K','FASTOW ANDREW S')                        # Define the top executives
execs = {name:enron_data[name] for name in top_execs}                                       # Slice out dict values of only the top executives
winner = max(execs, key=(lambda n: execs[n]['total_payments']))                             # Determine who made the most money
print("{} had the largest payments at {}".format(winner,execs[winner]['total_payments']))   # Report findings

print("****END OF THE BEGINNING****")
print("****BEGINNING OF THE END****")

######
# NaN Financials
######

def add_features(person):
    return {
        'poi' : True,
        'bonus': 'NaN',
        'deferral_payments': 'NaN',
        'deferred_income': 'NaN',
        'director_fees': 'NaN',
        'email_address': 'NaN',
        'exercised_stock_options': 'NaN',
        'expenses': 'NaN',
        'from_messages': 'NaN',
        'from_poi_to_this_person': 'NaN',
        'from_this_person_to_poi': 'NaN',
        'loan_advances': 'NaN',
        'long_term_incentive': 'NaN',
        'other': 'NaN',
        'restricted_stock': 'NaN',
        'restricted_stock_deferred': 'NaN',
        'salary': 'NaN',
        'shared_receipt_with_poi': 'NaN',
        'to_messages': 'NaN',
        'total_payments': 'NaN',
        'total_stock_value': 'NaN'
    }

# Add NaN features and true POI to the list of people in the POI file
file_data = {}
for name in poi_names_all: file_data.update({name:add_features(name)})

#pprint.pprint(file_data)

# Make a dict of all people by updating a copy of the enron_data dict
#all_persons = copy.deepcopy(file_data)
#print(len(all_persons))
#all_persons.update(enron_data)
#print(len(all_persons))

#pprint.pprint(all_persons)

#count_nan_tpay = 0
#for name in all_persons: 
#    if all_persons[name]['total_payments'] == 'NaN':
#        count_nan_tpay += 1

count_nan_tpay = 0
for name in enron_data: 
    if enron_data[name]['total_payments'] == 'NaN':
        count_nan_tpay += 1

count_poi_nan_tpay = 0
for name in ds_enron_poi: 
    if ds_enron_poi[name]['total_payments'] == 'NaN':
        count_poi_nan_tpay += 1

print("Count of people without total_payment: {}".format(count_nan_tpay))
print("Percent of people without total_payment: {}%".format(100*count_nan_tpay/len(enron_data)))

print("Count of people of interest without total_payment: {}".format(count_poi_nan_tpay))
print("Percent of people of interest without total_payment: {}%".format(100*count_poi_nan_tpay/len(ds_enron_poi)))

#print("DataSet People of Interest")
#pprint.pprint(poi_names_ds)

#print("Manual People of Interest")
#pprint.pprint(poi_names_file)

#print("All People of Interest")
#pprint.pprint(poi_names_all)