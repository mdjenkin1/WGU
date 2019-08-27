#!/usr/bin/python

import pickle
import pprint
import sys
import pandas as pd
import numpy as np


from sklearn.ensemble import AdaBoostClassifier
from sklearn.datasets import make_classification
from sklearn import model_selection
#from sklearn.cross_validation import KFold
from scipy import stats

sys.path.append("./tools/")
from feature_format import featureFormat, targetFeatureSplit

"""
    Train an adaboost based person of interest classifier on the
    sparse financial features of the Enron dataset.
    https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html
"""

###
### Load Datasets
###

#
# Full Finance Dataset Load
#

infile = open("./pickle_jar/final_project_dataset_cleaned.pkl", "rb")
prepd_data = pickle.load(infile)
infile.close()

fin_features = ['poi','salary', 'deferral_payments', 'total_payments', 'bonus', 
    'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 'loan_advances',
    'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock', 'director_fees']

data_load = featureFormat(prepd_data, fin_features)
poi, data_split = targetFeatureSplit( data_load )
fin_data = pd.DataFrame(data_split, columns = fin_features[1:])

#
# No Loan Dataset 
#

infile = open("./pickle_jar/final_project_dataset_cleaned_no_loan.pkl", "rb")
prepd_no_loan = pickle.load(infile)
infile.close()

no_loan_features = ['poi','salary', 'deferral_payments', 'total_payments', 'bonus', 
    'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses',
    'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock', 'director_fees']

no_loan_load = featureFormat(prepd_no_loan, no_loan_features)
no_loan_poi, no_loan_split = targetFeatureSplit( no_loan_load )
no_loan_data = pd.DataFrame(no_loan_split, columns = no_loan_features[1:])

skip_accuracy = True
###
### Throw away learner accuracy.
###

def get_accuracy(features_train, labels_train, features_test, labels_test):
    clf_stock = AdaBoostClassifier(n_estimators = 100)
    clf_stock.fit(features_train, labels_train)
    return clf_stock.score(features_test, labels_test)

#
# Random splits with loan data set
#

if not skip_accuracy:
    acc_scores_loans = []
    for i in range(100):
        features_train, features_test, labels_train, labels_test = model_selection.train_test_split(fin_data, poi, test_size=0.1, random_state=i)
        acc_scores_loans.append(get_accuracy(features_train, labels_train, features_test, labels_test))
    pprint.pprint(stats.describe(np.array(acc_scores_loans)))

#
# Random splitting No loan data set
#

if not skip_accuracy:
    acc_scores_no_loans = []
    for i in range(100):
        no_loan_features_train, no_loan_features_test, no_loan_labels_train, no_loan_labels_test = model_selection.train_test_split(fin_data, poi, test_size=0.1, random_state=i)
        acc_scores_no_loans.append(get_accuracy(no_loan_features_train, no_loan_labels_train, no_loan_features_test, no_loan_labels_test))
    pprint.pprint(stats.describe(np.array(acc_scores_no_loans)))


#no_loan_features_train, no_loan_features_test, no_loan_labels_train, no_loan_labels_test = model_selection.train_test_split(no_loan_data, no_loan_poi, test_size=0.1, random_state=42)
#no_loan_features_train, no_loan_features_test, no_loan_labels_train, no_loan_labels_test = model_selection.train_test_split(no_loan_data, no_loan_poi, test_size=0.1)

#no_loan_poi_clf_adb_stock = AdaBoostClassifier()
#no_loan_poi_clf_adb_stock.fit(no_loan_features_train, no_loan_labels_train)

#print("Accuracy (No loan): %.3f" % (no_loan_poi_clf_adb_stock.score(no_loan_features_test,no_loan_labels_test)))

esti = 800

features_train, features_test, labels_train, labels_test = model_selection.train_test_split(fin_data, poi, test_size=0.1)
clf = AdaBoostClassifier(n_estimators = esti)
clf.fit(features_train, labels_train)

#pprint.pprint(clf_stock.estimator_errors_)
#pprint.pprint(clf_stock.estimator_weights_)
#pprint.pprint(clf_stock.feature_importances_)

feature_weights = zip(fin_data.columns, clf.feature_importances_)
pprint.pprint(feature_weights)
print("{} estimator accuracy score: {}".format(esti, clf.score(features_test, labels_test)))