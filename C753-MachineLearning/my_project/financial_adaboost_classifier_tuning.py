#!/usr/bin/python

import pickle
import pprint
import sys
import pandas as pd

from sklearn.ensemble import AdaBoostClassifier
from sklearn.datasets import make_classification
from sklearn import model_selection

sys.path.append("./tools/")
from feature_format import featureFormat, targetFeatureSplit

"""
    Train an adaboost based person of interest classifier on the
    sparse financial features of the Enron dataset.
    https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html
"""

###
### Load Dataset

infile = open("./pickle_jar/final_project_dataset_cleaned.pkl", "rb")
prepd_data = pickle.load(infile)
infile.close()

fin_features = ['poi','salary', 'deferral_payments', 'total_payments', 'bonus', 
    'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 'loan_advances',
    'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock', 'director_fees']

data_load = featureFormat(prepd_data, fin_features)
poi, data_split = targetFeatureSplit( data_load )
fin_data = pd.DataFrame(data_split, columns = fin_features[1:])

features_train, features_test, labels_train, labels_test = model_selection.train_test_split(fin_data, poi, test_size=0.1, random_state=42)

poi_clf_adb_stock = AdaBoostClassifier()
poi_clf_adb_stock.fit(features_train, labels_train)

print("***Accuracy (stock): {}***".format(poi_clf_adb_stock.score(features_test,labels_test)))

###


###
### Determine the happy spot.
