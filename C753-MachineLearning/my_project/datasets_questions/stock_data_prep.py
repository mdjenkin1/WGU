#!/usr/bin/python
import pickle
import pprint
import re

"""
    Finalized data prep.
"""

#####
## Script objects
#####


# Feature groups
##
stock_features = ['poi', 'restricted_stock_deferred', 'total_stock_value', 'exercised_stock_options', 'restricted_stock']

payment_features = ['poi','salary', 'deferral_payments', 'total_payments', 'bonus', 
    'deferred_income', 'expenses', 'loan_advances', 'other', 'long_term_incentive', 'director_fees']


# Dataset load
##
original_ef_data = pickle.load(open("../pickle_jar/final_project_dataset.pkl"))
cleaned_ef_data = {}


# Decision helpers
##
drop_person = set(['THE TRAVEL AGENCY IN THE PARK', 'TOTAL'])   # Static entries to be dropped
impute_zero = lambda x: 0 if x == "NaN" else x                  # Simple imputator of NaN values

#######
## Data Prep
#######

#  First pass: data validation and formating
##
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

    # Make note: drop those with non-sane stock totals
    if impute_zero(original_ef_data[norm_person]['restricted_stock_deferred']) + impute_zero(original_ef_data[norm_person]['restricted_stock']) + impute_zero(original_ef_data[norm_person]['exercised_stock_options']) != impute_zero(original_ef_data[norm_person]['total_stock_value']):
        drop_person.add(norm_person)
        #print("{} does not have sane stock totals.".format(norm_person))
        #for feat in stock_features:
        #    print("{} = {}".format(feat, original_ef_data[norm_person][feat]))

    # Make note: drop those with non-sane payment totals
    calc_total_pay = 0
    for feat in payment_features[1:]:
        if feat != 'total_payments': calc_total_pay += impute_zero(original_ef_data[norm_person][feat]) 
    if impute_zero(original_ef_data[norm_person]['total_payments']) != calc_total_pay:
        drop_person.add(norm_person)
        #print("{} does not have sane payment totals.".format(norm_person))
        #for feat in payment_features:
        #    print("{} = {}".format(feat, original_ef_data[norm_person][feat]))
    


# Data copy, clean and expand
##
for person in original_ef_data:
    if person not in drop_person:
        cleaned_ef_data[person] = {feat:original_ef_data[person][feat] for feat in original_ef_data[person]}

out = open("../pickle_jar/dataset_final_clean.pkl","wb")
pickle.dump(cleaned_ef_data, out)
out.close()

