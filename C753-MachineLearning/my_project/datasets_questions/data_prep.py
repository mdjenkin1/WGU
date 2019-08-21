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

# Dynamic entry dropping
for person in original_ef_data:
    # mise name normalization
    norm_person = re.sub(r'\s\b\w\b| JR|\.','',person).upper()
    original_ef_data[norm_person] = original_ef_data.pop(person)
    # Drop those with no value
    has_value = False
    for feature in original_ef_data[norm_person]:
        if feature != 'poi' and original_ef_data[norm_person][feature] != 'NaN':
            has_value = True
            break
    if not has_value: 
        drop_person.add(norm_person)

#print(drop_person)

# Copy and clean our data
for person in original_ef_data:
    if person not in drop_person:
        cleaned_ef_data[person] = {feat:original_ef_data[person][feat] for feat in original_ef_data[person] if feat!='loan_advances'}
        if original_ef_data[person]['loan_advances'] != 'NaN':
            cleaned_ef_data[person]['total_payments'] = cleaned_ef_data[person]['total_payments'] - original_ef_data[person]['loan_advances']

out = open("../pickle_jar/final_project_dataset_cleaned.pkl","wb")
pickle.dump(cleaned_ef_data, out)
out.close()
