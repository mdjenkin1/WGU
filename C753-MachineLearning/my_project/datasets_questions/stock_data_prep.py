#!/usr/bin/python
import pickle
import pprint
import re

"""
    Clean the provided dataset based on findings made in: 
        explore_enron_data.py
        explore_feature_detail.py
"""

######
# Script objects
######

##
# Feature 
stock_features = ['poi', 'restricted_stock_deferred', 'total_stock_value', 'exercised_stock_options', 'restricted_stock']

##
# Datasets 
original_ef_data = pickle.load(open("../pickle_jar/final_project_dataset.pkl"))
cleaned_ef_data = {}

##
# Decision helpers
drop_person = set(['THE TRAVEL AGENCY IN THE PARK', 'TOTAL'])   # Entries to be dropped with static values

######
# Data Preparation
######

##
#  First pass: data validation and formating
for person in original_ef_data:
    
    # Mise: name normalization
    norm_person = re.sub(r'\s\b\w\b| JR|\.','',person).upper()
    original_ef_data[norm_person] = original_ef_data.pop(person)

    # Make note: drop those with no value
    has_value = False
    for feature in original_ef_data[norm_person]:
        if feature != 'poi' and original_ef_data[norm_person][feature] != 'NaN':
            has_value = True
            break
    if not has_value: 
        drop_person.add(norm_person)

    # Make note: drop those with not sane stock totals
    impute_zero = lambda x: 0 if x == "NaN" else x
    if impute_zero(original_ef_data[norm_person]['restricted_stock_deferred']) + impute_zero(original_ef_data[norm_person]['restricted_stock']) + impute_zero(original_ef_data[norm_person]['exercised_stock_options']) != impute_zero(original_ef_data[norm_person]['total_stock_value']):
        drop_person.add(norm_person)
        #print("{} does not have sane stock totals.".format(norm_person))
        #for feat in stock_features:
        #    print("{} = {}".format(feat, original_ef_data[norm_person][feat]))

##
# Data copy, clean and expand
for person in original_ef_data:
    if person not in drop_person:
        cleaned_ef_data[person] = {feat:original_ef_data[person][feat] for feat in original_ef_data[person]}

out = open("../pickle_jar/dataset_final_clean.pkl","wb")
pickle.dump(cleaned_ef_data, out)
out.close()

