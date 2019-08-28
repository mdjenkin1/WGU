#!/usr/bin/python

import sys
import pickle
import pprint
import pandas as pd

sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from data_scrubber import scrub_data


### Task 1: Select what features you'll use.

# Reference ..\feature_selection\lasso_validation.py
features_list = ['poi', 'exercised_stock_options', 'bonus', 'expenses', 'salary']

# Raw dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

# Preprocess dataset
scrubs, scrubbed_data = scrub_data(data_dict, features_list)
#print("These are the people scrubbed from our dataset")
#pprint.pprint(scrubs)
#print("\r")
#print("These are the good values from the dataset")
#pprint.pprint(data_set)

# Save the preprocessed dataset
with open("selected_features_dataset.pkl", "w") as data_file:
    pickle.dump(data_set, data_file)

# Load data, ready for processing
data_set = featureFormat(scrubbed_data, features_list)
poi, data_np_arrays = targetFeatureSplit(data_set)
data_df = pd.DataFrame(data_np_arrays, columns = features_list[1:])

### Task 2: Remove outliers


### Task 3: Create new feature(s)
### Task 4: Try a variety of classifiers
### Task 5: Tune your classifier to achieve better than .3 precision 
### Task 6: Dump your classifier, dataset, and features_list 
