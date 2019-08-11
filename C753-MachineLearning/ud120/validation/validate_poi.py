#!/usr/bin/python


"""
    Starter code for the validation mini-project.
    The first step toward building your POI identifier!

    Start by loading/formatting the data

    After that, it's not our code anymore--it's yours!
"""

import pickle
import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit

data_dict = pickle.load(open("../final_project/final_project_dataset.pkl", "r") )

### first element is our labels, any added elements are predictor
### features. Keep this the same for the mini-project, but you'll
### have a different feature list when you do the final project.
features_list = ["poi", "salary"]

data = featureFormat(data_dict, features_list)      # numpy.ndarray of numpy.ndarrays
labels, features = targetFeatureSplit(data)         # lists

#print(type(data[1]))
#print(type(labels))
#print(labels)
#print(type(features))

### it's all yours from here forward!  

from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import accuracy_score

clf_full = tree.DecisionTreeClassifier()
clf_full = clf_full.fit(features, labels)
pred_full = clf_full.predict(features)
acc_full = accuracy_score(labels, pred_full)

print("Overfit all data accuracy: %.3f" % acc_full)

features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size = 0.3, random_state = 42)
clf = tree.DecisionTreeClassifier()
clf = clf.fit(features_train, labels_train)
pred = clf.predict(features_test)
acc = accuracy_score(labels_test, pred)

hit_cnt = 0
for x in pred:
    if x == 1: hit_cnt += 1 

print("Test data accuracy: %.3f" % acc)
print("Number of predicted POI: {}".format(hit_cnt))
print("Number of predicted people: {}".format(len(pred)))

#print("visually compare")
#print(zip(pred,labels_test))
tree_hit = 0
for pos, lab in zip(pred,labels_test):
    if pos == lab and lab == 1:
        tree_hit += 1

print("Count of true positives: {}".format(tree_hit))

from sklearn.metrics import precision_score,recall_score

p_score = precision_score(labels_test, pred)
r_score = recall_score(labels_test, pred)

print("precision_score: %.3f" % p_score)
print("recall_score: %.3f" % r_score)

test_pred = [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1] 
test_labels = [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0]

test_tpos = 0
test_tneg = 0
test_fpos = 0
test_fneg = 0

for tp, tl in zip(test_pred,test_labels):
    if tp == tl == 1:            #True Positives
        test_tpos += 1
    elif tp == tl == 0:          #True Negatives
        test_tneg += 1
    elif tp == 1 and tl == 0:           #False Positives
        test_fpos += 1
    elif tp == 0 and tl == 1:           #False Negatives
        test_fneg += 1

print("test set true positives: {}".format(test_tpos))
print("test set true negatives: {}".format(test_tneg))
print("test set false positives: {}".format(test_fpos))
print("test set false negatives: {}".format(test_fneg))

test_p_score = precision_score(test_labels, test_pred)
test_r_score = recall_score(test_labels, test_pred)

print("test set precision_score: %.3f" % test_p_score)
print("test set recall_score: %.3f" % test_r_score)