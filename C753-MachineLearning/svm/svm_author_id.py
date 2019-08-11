#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 2 (SVM) mini-project.

    Use a SVM to identify emails from the Enron corpus by their authors:    
    Sara has label 0
    Chris has label 1
"""
    
import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()

#########################################################
### your code goes here ###

from sklearn import svm
from sklearn.metrics import accuracy_score
import numpy

## Smaller Training Set - 0.8845 accuracy
#features_train = features_train[:len(features_train)/100] 
#labels_train = labels_train[:len(labels_train)/100] 

t0 = time()
#clf = svm.SVC(kernel='linear', gamma='auto') # original kernel training

#clf = svm.SVC(kernel='rbf', gamma='auto') # rbf - Small set accuracy: 0.616
#clf = svm.SVC(kernel='rbf', gamma='auto', C=10.0) # rbf C=10.0 - Small set accuracy: 0.616
#clf = svm.SVC(kernel='rbf', gamma='auto', C=100.0) # rbf C=100.0 - Small set accuracy:  0.616
#clf = svm.SVC(kernel='rbf', gamma='auto', C=1000.0) # rbf C=1000.0 - Small set accuracy: 0.8214
clf = svm.SVC(kernel='rbf', gamma='auto', C=10000.0) # rbf C=10000.0 - Small set accuracy: 0.8925; Full set accuracy: 0.9909

clf.fit(features_train,labels_train)
print "Training time:", round(time()-t0, 3), "s" # 137.687s

t0 = time()
pred = clf.predict(features_test)
print "Prediction time:", round(time()-t0, 3), "s" # 14.452s

## Small Training set, what is prediction of Nth element (0 or 1)?
for N in (10,26,50):
    print("{}th element predicted: {}".format(N,pred[N])) # 1
    #: pred[10] = 1
    #: pred[26] = 0
    #: pred[50] = 1

## Full training set, how many are predicted to be Chris (1)
unique,counts = numpy.unique(pred, return_counts=True)
uniqueCounts = dict(zip(unique,counts))
print("{} elements predicted as Chris.".format(uniqueCounts[1]))

accuracy = accuracy_score(labels_test, pred)
print("classifier accuracy: {}".format(accuracy)) # 0.984
#########################################################
