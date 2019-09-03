#!/usr/bin/python

import sys
import pickle
#import pprint
import pandas as pd

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import precision_score
from sklearn.model_selection import train_test_split

sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from data_scrubber import scrub_data

# Load Raw dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 1: Select what features you'll use.
features_list = ['poi', 'exercised_stock_options', 'bonus', 'expenses', 'salary']

# Save features_list
with open("my_feature_list.pkl", "w") as data_file:
    pickle.dump(features_list, data_file)

### Task 2: Remove outliers
### Task 3: Create new feature(s)
# Scrub dataset
_, my_dataset = scrub_data(data_dict, features_list)

# Pickle scrubbed_data
with open("my_dataset.pkl", "w") as data_file:
    pickle.dump(my_dataset, data_file)

### Task 4: Try a variety of classifiers
# Dataset loading, scaling has been moved to pipelines
### Task 5: Tune your classifier to achieve better than .3 precision 

svc_params = {'svc__kernel':('linear','rbf','sigmoid','poly'), 'svc__C': range(1,10)}
svc = SVC(gamma='scale')
svc_pipe = make_pipeline(StandardScaler(), svc)
svc_clf = GridSearchCV(svc_pipe, svc_params, cv=10, scoring=make_scorer(precision_score))
svc_clf.fit(features,labels)

knn_params = {'kneighborsclassifier__n_neighbors': range(1,10), 'kneighborsclassifier__weights': ['uniform', 'distance']}
knn = KNeighborsClassifier()
knn_pipe = make_pipeline(StandardScaler(), knn)
knn_clf = GridSearchCV(knn_pipe, knn_params, cv=10, scoring=make_scorer(precision_score))
knn_clf.fit(features,labels)

clf = svc_clf if svc_clf.best_score_ > knn_clf.best_score_ else knn_clf

### Task 6: Dump your classifier, dataset, and features_list 
