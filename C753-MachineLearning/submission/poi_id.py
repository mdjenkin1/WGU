#!/usr/bin/python

import sys
import pickle
import pprint
import pandas as pd
import warnings

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import precision_score, make_scorer, f1_score
from sklearn.feature_selection import SelectKBest

sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from data_scrubber import scrubData
from email_feature_creation import addEmailFlowFeatures

warnings.filterwarnings("ignore")

# Load Raw dataset
with open("final_project_dataset.pkl", "rb") as data_file:
    data_dict = pickle.load(data_file)

### Task 1: Select what features you'll use.
all_features = ['poi','salary', 'deferral_payments', 'total_payments', 'bonus', 
    'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 
    'loan_advances', 'exercised_stock_options', 'other', 'long_term_incentive', 
    'restricted_stock', 'director_fees', 'to_messages', 'from_poi_to_this_person', 
    'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi', 'email_address']

features_list = ['poi','salary', 'deferral_payments', 'bonus', 'restricted_stock_deferred', 
    'deferred_income', 'expenses', 'exercised_stock_options', 'other', 'long_term_incentive', 
    'restricted_stock', 'director_fees']


### Task 2: Remove outliers
### Task 3: Create new feature(s)
# Scrub dataset
_, full_dataset = scrubData(data_dict, all_features)

my_dataset = addEmailFlowFeatures(full_dataset)

data = featureFormat(my_dataset, features_list)
labels, features = targetFeatureSplit(data)
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.3, random_state=42)

### Task 4: Try a variety of classifiers
### Task 5: Tune your classifier to achieve better than .3 precision 

svc_params = {'selectkbest__k':range(1,12), 
    'svc__kernel':('linear','rbf','sigmoid','poly'), 
    'svc__C': range(1,10)}
svc = SVC(gamma='scale')
svc_pipe = make_pipeline(SelectKBest(), StandardScaler(), svc)
svc_clf = GridSearchCV(svc_pipe, svc_params, cv=10, scoring='f1')
svc_clf.fit(features,labels)
print("SVC Best Score: {}".format(svc_clf.best_score_))
#print("SVC CV Results")
#pprint.pprint(svc_clf.cv_results_['rank_test_score'])

knn_params = {'selectkbest__k':range(1,12), 
    'kneighborsclassifier__n_neighbors': range(1,10), 
    'kneighborsclassifier__weights': ['uniform', 'distance']}
knn = KNeighborsClassifier()
knn_pipe = make_pipeline(SelectKBest(), StandardScaler(), knn)
knn_clf = GridSearchCV(knn_pipe, knn_params, cv=10, scoring='f1')
knn_clf.fit(features,labels)
print("KNN Best Score: {}".format(knn_clf.best_score_))
#print("KNN CV Results")
#pprint.pprint(knn_clf.cv_results_['rank_test_score'])

clf = svc_clf.best_estimator_ if svc_clf.best_score_ > knn_clf.best_score_ else knn_clf.best_estimator_
print("Best Classifier")
pprint.pprint(clf)

### Task 6: Dump your classifier, dataset, and features_list 

dump_classifier_and_data(clf, my_dataset, features_list)
