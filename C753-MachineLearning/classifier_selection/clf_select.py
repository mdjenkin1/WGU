#!/usr/bin/python

import sys
import pickle
import pprint
import pandas as pd

from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.decomposition import PCA
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold
from sklearn.metrics import precision_score, recall_score, make_scorer, f1_score, accuracy_score
from sklearn.metrics import classification_report

from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings("ignore")

sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit

with open("../pickle_jar/my_dataset.pkl", "r") as data_file:
    my_dataset = pickle.load(data_file)

with open("../pickle_jar/my_feature_list.pkl", "r") as data_file:
    features_list = pickle.load(data_file)

data = featureFormat(my_dataset, features_list)
labels, features = targetFeatureSplit(data)
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.3, random_state=42)

svc_params = {'svc__kernel':('linear','rbf','sigmoid','poly'), 'svc__C': range(1,10)}
svc = SVC(gamma='scale')
svc_pipe = make_pipeline(StandardScaler(), svc)

knn_params = {'kneighborsclassifier__n_neighbors': range(1,10), 'kneighborsclassifier__weights': ['uniform', 'distance']}
knn = KNeighborsClassifier()
knn_pipe = make_pipeline(StandardScaler(), knn)

clf_pipes = [[svc, svc_params], [knn, knn_params]]

svc_clf = GridSearchCV(svc_pipe, svc_params, cv=10, scoring=make_scorer(precision_score))
svc_clf.fit(features,labels)
pprint.pprint("Support Vector Classifier's best precision is: {0:.3f}".format(svc_clf.best_score_))

knn_clf = GridSearchCV(knn_pipe, knn_params, cv=10, scoring=make_scorer(precision_score))
knn_clf.fit(features,labels)
pprint.pprint("K-Nearest Neighbors best precision is: {0:.3f}".format(knn_clf.best_score_))

clf = svc_clf if svc_clf.best_score_ > knn_clf.best_score_ else knn_clf
pprint.pprint(clf)

#score_types = [f1_score, precision_score, recall_score, accuracy_score]
#for pipe, params in clf_pipes:
#    print("{} with parameters: {}".format(pipe, params))
#    for scorer in score_types:
#        print scorer
#        clf = GridSearchCV(pipe, params, cv=10, scoring=make_scorer(scorer))
#        clf.fit(features, labels)

        #pprint.pprint(svc_clf.cv_results_)
        #print("These are the best parameters for {} scored by {}".format(pipe, scorer))
        #pprint.pprint(clf.best_estimator_)
        #pprint.pprint(clf.best_score_)


####
#### Below are the remains of my start at manually building a brute force classifier selector.
#### Also includes my initial runs at classifier selection and tuning. This remains only for posterity.

def get_clf_accuracy(clf, features, labels, cv=10):
    clf_cv_accuracy = cross_val_score(clf, features, labels, cv=cv)
    return clf_cv_accuracy

def get_clf_scores(labels, predictions):
    p_score = precision_score(labels, predictions)
    r_score = recall_score(labels, predictions)
    return p_score, r_score

###
### KNN
###
knn_clf = KNeighborsClassifier()
knn_pipe = make_pipeline(StandardScaler(), knn_clf)
knn_pipe.fit(features_train, labels_train)
knn_score = knn_pipe.score(features_test, labels_test)
print("Stock configuration K-NN mean accuracy: {}".format(knn_score))
print("\r")

###
### SVM
###
svm_clf = SVC()
svm_pipe = make_pipeline(StandardScaler(), svm_clf)
svm_pipe.fit(features_train, labels_train)
svm_score = svm_pipe.score(features_test, labels_test)
print("Stock configuration SVM mean accuracy: {}".format(svm_score))
print("SVM default ")
print("\r")

###
### Linear Regression
###
clf_lr = make_pipeline(StandardScaler(), LinearRegression())
clf_lr.fit(features_train, labels_train)
lr_score_0 = clf_lr.score(features_test, labels_test)
print("Stock configuration linear coefficient of determination: {}".format(lr_score_0))

clf_pca_lr = make_pipeline(StandardScaler(), PCA(n_components=2), LinearRegression())
clf_pca_lr.fit(features_train, labels_train)
lr_pca_score_0 = clf_lr.score(features_test, labels_test)
print("Stock configuration linear coefficient of determination with PCA(2): {}".format(lr_pca_score_0))
print("\r")


##
## Cross Validation
##
knn_pipe = make_pipeline(StandardScaler(), KNeighborsClassifier())
knn_cv_scores = cross_val_score(knn_pipe, features, labels, cv=10)
print("stock knn cross validation scores")
print(knn_cv_scores)
print("stock knn accuracy: {:.2f} (+/- {:.2f})".format(knn_cv_scores.mean(), knn_cv_scores.std()*2))
print("stock knn accuracy: {:.2f} (+/- {:.2f})".format(knn_cv_scores.mean(), knn_cv_scores.std()*2))
print("stock knn accuracy: {:.2f} (+/- {:.2f})".format(knn_cv_scores.mean(), knn_cv_scores.std()*2))
print("\r")

svm_pipe = make_pipeline(StandardScaler(), SVC())
svm_cv_scores = cross_val_score(svm_pipe, features, labels, cv=10)
print("stock svm cross validation scores")
print(svm_cv_scores)
print("stock svm accuracy: {:.2f} (+/- {:.2f})".format(svm_cv_scores.mean(), svm_cv_scores.std()*2))
print("stock svm accuracy: {:.2f} (+/- {:.2f})".format(svm_cv_scores.mean(), svm_cv_scores.std()*2))
print("stock svm accuracy: {:.2f} (+/- {:.2f})".format(svm_cv_scores.mean(), svm_cv_scores.std()*2))
print("\r")

clf = svm_pipe


# Which kernel

#svm_kernels = ['linear', 'poly', 'rbf', 'sigmoid']

#svm_clf.set_params(kernel='rbf')
#print("***SVM Kernal Testing***")
#for kern in svm_kernels:
#    svm_clf.set_params(kernel = kern)
#    clf_cv_scores = get_clf_accuracy(clf, features, labels)
#    print(clf_cv_scores)
#    p_score, r_score = get_clf_scores(labels_test, clf.predict(features_test))
#    print("{} accuracy: {:.2f} (+/- {:.2f})".format(kern, clf_cv_scores.mean(), clf_cv_scores.std()*2))
#    print("{} precision_score: {:.3f}".format(kern, p_score))
#    print("{} recall_score: {:.3f}".format(kern, r_score))
#    print("\r")
