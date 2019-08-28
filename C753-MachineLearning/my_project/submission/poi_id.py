#!/usr/bin/python

import sys
import pickle
import pprint
import pandas as pd

from sklearn.preprocessing import StandardScaler

sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from data_scrubber import scrub_data


### Task 1: Select what features you'll use.

# Load Raw dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

# features determined from data exploration
features_list = ['poi', 'exercised_stock_options', 'bonus', 'expenses', 'salary']

# Save features_list
with open("my_feature_list.pkl", "w") as data_file:
    pickle.dump(features_list, data_file)

# Scrub dataset
_, scrubbed_data = scrub_data(data_dict, features_list)

# Pickle scrubbed_data
with open("my_scrubbed_data.pkl", "w") as data_file:
    pickle.dump(scrubbed_data, data_file)

# Preprocessing, split and scale features. Load to dataframe
data_set = featureFormat(scrubbed_data, features_list)
poi, data_np_arrays = targetFeatureSplit(data_set)

scaler = StandardScaler()
scaled_array_data = scaler.fit_transform(data_np_arrays)
preped_data = pd.DataFrame(scaled_array_data, columns = features_list[1:])

# Pickle the preprocessed dataset
with open("my_dataset.pkl", "w") as data_file:
    pickle.dump(preped_data, data_file)

# Pickle the scaler
with open("my_data_scaler.pkl", "w") as data_file:
    pickle.dump(scaler, data_file)


### Task 2: Remove outliers


### Task 3: Create new feature(s)
### Task 4: Try a variety of classifiers
### Task 5: Tune your classifier to achieve better than .3 precision 
### Task 6: Dump your classifier, dataset, and features_list 
