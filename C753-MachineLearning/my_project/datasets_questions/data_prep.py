#!/usr/bin/python
import pickle
import pprint
import re

"""
    Clean the provided dataset based on findings made in explore_enron_data.py
"""

original_ef_data = pickle.load(open("../pickle_jar/final_project_dataset.pkl"))
cleaned_ef_data = {}

# Static entries for dropping
drop_person = set(['THE TRAVEL AGENCY IN THE PARK', 'TOTAL'])

# Copy and clean our data
for person in original_ef_data:
    norm_person = re.sub(r'\s\b\w\b| JR|\.','',person).upper()
    if norm_person not in drop_person or len(original_ef_data[person].keys()) <= 1:
        cleaned_ef_data[norm_person] = {feat:original_ef_data[person][feat] for feat in original_ef_data[person] if feat!='loan_advances'}
        if original_ef_data[person]['loan_advances'] != 'NaN':
            cleaned_ef_data[norm_person]['total_payments'] = cleaned_ef_data[norm_person]['total_payments'] - original_ef_data[person]['loan_advances']

out = open("../pickle_jar/final_project_dataset_cleaned.pkl","wb")
pickle.dump(cleaned_ef_data, out)
out.close()
