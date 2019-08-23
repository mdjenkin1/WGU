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
# Feature grouping
fin_features = ['poi','salary', 'deferral_payments', 'total_payments', 'bonus', 
    'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 
    'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock', 'director_fees']

email_features = ['poi', 'to_messages', 'from_poi_to_this_person', 'from_messages', 
    'from_this_person_to_poi', 'shared_receipt_with_poi'] 

##
# Datasets 
original_ef_data = pickle.load(open("../pickle_jar/final_project_dataset.pkl"))
cleaned_ef_data = {}

##
# Decision helpers
has_email_and_stats = set()                                     # persons with email addresses and email statistics
drop_person = set(['THE TRAVEL AGENCY IN THE PARK', 'TOTAL'])   # Entries to be dropped with static values
drop_loan_advances = False

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

    # list of persons with email address and email statistics
    if original_ef_data[norm_person]['email_address'] != 'NaN':
        has_stats = False
        for feature in email_features[1:]:
            if original_ef_data[norm_person][feature] != 'NaN':
                has_stats = True
                break
        if has_stats: has_email_and_stats.add(norm_person)

#print(drop_person)

##
# Data copy, clean and expand
for person in original_ef_data:
    if person not in drop_person:
        cleaned_ef_data[person] = {feat:original_ef_data[person][feat] for feat in original_ef_data[person] if feat!='loan_advances'}
        if original_ef_data[person]['loan_advances'] != 'NaN' and drop_loan_advances:
            cleaned_ef_data[person]['total_payments'] = cleaned_ef_data[person]['total_payments'] - original_ef_data[person]['loan_advances']
        
        ##
        # Delineate the intersection of financial and email data

        # has_email_statistics
        if person in has_email_and_stats:
            cleaned_ef_data[person].update({"has_email_statistics" : True})
        else:
            cleaned_ef_data[person].update({"has_email_statistics" : False})

        # has_financial
        cleaned_ef_data[person].update({"has_financial" : False})
        for feat in fin_features[1:]:
            if cleaned_ef_data[person][feat] != 'NaN': 
                cleaned_ef_data[person]["has_financial"] = True
                break

if drop_loan_advances:
    out = open("../pickle_jar/final_project_dataset_cleaned_no_loan.pkl","wb")
else:
    out = open("../pickle_jar/final_project_dataset_cleaned.pkl","wb")
pickle.dump(cleaned_ef_data, out)
out.close()

