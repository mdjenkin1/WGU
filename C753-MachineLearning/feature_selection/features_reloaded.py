#!/usr/bin/python

import pickle
import pprint
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append("../submission/")
sys.path.append("../tools/")
from data_scrubber import scrub_data
from feature_format import featureFormat, targetFeatureSplit

with open("../pickle_jar/final_project_dataset.pkl", "rb") as data_file:
    data_dict = pickle.load(data_file)

all_features = ['poi','salary', 'deferral_payments', 'total_payments', 'bonus', 
    'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 
    'loan_advances', 'exercised_stock_options', 'other', 'long_term_incentive', 
    'restricted_stock', 'director_fees', 'to_messages', 'from_poi_to_this_person', 
    'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi', 'email_address']


kept_features = ['poi','salary', 'deferral_payments', 'total_payments', 'bonus', 
    'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 
    'loan_advances', 'exercised_stock_options', 'other', 'long_term_incentive', 
    'restricted_stock', 'director_fees', 'to_messages', 'from_poi_to_this_person', 
    'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi']

fin_features = ['poi','salary', 'deferral_payments', 'total_payments', 'bonus', 
    'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 
    'loan_advances', 'exercised_stock_options', 'other', 'long_term_incentive',
    'restricted_stock', 'director_fees']

email_features = ['poi', 'to_messages', 'from_poi_to_this_person', 'from_messages', 
    'from_this_person_to_poi', 'shared_receipt_with_poi']


dropped, full_dataset = scrub_data(data_dict, all_features)

print("These entries were removed from the dataset")
pprint.pprint(dropped)
print("\r")

##
# Dimension the intersection of financial and email data
num_with_email_addr = 0
num_with_email_stats = 0
num_with_fin = 0
num_with_both = 0
poi_with_email = 0
for person in full_dataset:
    full_dataset[person].update({"has_email_statistics" : False})
    full_dataset[person].update({"has_financial" : False})

    if full_dataset[person]['email_address'] != 'NaN':
        num_with_email_addr += 1
        for feature in email_features[2:]:
            if full_dataset[person][feature] != 'NaN':
                num_with_email_stats += 1
                full_dataset[person]["has_email_statistics"] = True
                break

    # has_financial
    for feat in fin_features[1:]:
        if full_dataset[person][feat] != 'NaN': 
            num_with_fin += 1
            full_dataset[person]["has_financial"] = True
            break

    if full_dataset[person]["has_email_statistics"] and full_dataset[person]["has_financial"]: num_with_both += 1
    if full_dataset[person]["has_email_statistics"] and full_dataset[person]["poi"]: poi_with_email += 1

print("Number of people with an email address: {}".format(num_with_email_addr))
print("Number of people with email stats: {}".format(num_with_email_stats))
print("Number of people with financial data: {}".format(num_with_fin))
print("Number of people with both data types: {}".format(num_with_both))
print("Number of poi with email stats: {}".format(poi_with_email))


#data = featureFormat(full_dataset, all_features)
#labels, features = targetFeatureSplit(data)

#print("Full dataset as dataframe")
#pprint.pprint(data)