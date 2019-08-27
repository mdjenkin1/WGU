#!/usr/bin/python
import pickle
import pprint
import sys
import pandas as pd

from sklearn import linear_model
from sklearn import model_selection

sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit

# Load Data
##

fin_features = ['poi','salary', 'deferral_payments', 'total_payments', 'bonus', 
    'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 'loan_advances',
    'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock', 'director_fees']

cleaned_data = pickle.load(open("../pickle_jar/final_project_dataset_cleaned.pkl"))

fin_data = featureFormat(cleaned_data, fin_features)
poi, data_np_arrays = targetFeatureSplit(fin_data)
data_df = pd.DataFrame(data_np_arrays, columns = fin_features[1:])

# Train it up
##
features_train, features_test, labels_train, labels_test = model_selection.train_test_split(fin_data, poi, test_size=0.0)

clf = linear_model.Lasso(alpha=5, tol=1)
clf.fit(features_train, labels_train)
feature_weights = {}

for i in range(len(fin_features[1:])):
    feature_weights.update({fin_features[i+1] : clf.coef_[i+1]})
sorted_val = sorted(feature_weights.values())
sorted_key = sorted(feature_weights, key=feature_weights.get)
pprint.pprint(zip(sorted_key,sorted_val))
