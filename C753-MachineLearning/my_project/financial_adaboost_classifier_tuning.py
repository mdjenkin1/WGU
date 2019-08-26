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

###
### train and test split bias?

## poi distribution
print("Total number of poi: {}".format(poi.count(1)))
print("Number of poi in train set: {}".format(labels_train.count(1)))
print("Number of poi in test set: {}".format(labels_test.count(1)))

## distribution of sparse features
#deferral_payments           0.27
#restricted_stock_deferred   0.12
#loan_advances               0.02
#director_fees               0.11

isPop = lambda x: False if x == 0 else True
print(features_train['deferral_payments'].apply(isPop).count())
print(features_train['restricted_stock_deferred'].apply(isPop).count())
print(features_train['loan_advances'].apply(isPop).count())

#print("Total number of actual deferral_payments: {}".format())
#print("Number of actual deferral_payments in train set: {}".format(features_train['deferral_payments'].count(isPop)))
#print("Number of actual deferral_payments in test set: {}".format(features_test['deferral_payments'].count(isPop)))




###
### stock algorithm
#poi_clf_adb_stock = AdaBoostClassifier()
#poi_clf_adb_stock.fit(features_train, labels_train)

#print("***Accuracy (stock): {}***".format(poi_clf_adb_stock.score(features_test,labels_test)))



###
### Determine the happy spot.
