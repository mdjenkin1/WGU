#!/usr/bin/python

import pickle
import numpy
numpy.random.seed(42)


### The words (features) and authors (labels), already largely processed.
### These files should have been created from the previous (Lesson 10)
### mini-project.
words_file = "../text_learning/your_word_data.pkl" 
authors_file = "../text_learning/your_email_authors.pkl"
word_data = pickle.load( open(words_file, "r"))
authors = pickle.load( open(authors_file, "r") )



### test_size is the percentage of events assigned to the test set (the
### remainder go into training)
### feature matrices changed to dense representations for compatibility with
### classifier functions in versions 0.15.2 and earlier
#from sklearn import cross_validation
#features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(word_data, authors, test_size=0.1, random_state=42)
from sklearn import model_selection
features_train, features_test, labels_train, labels_test = model_selection.train_test_split(word_data, authors, test_size=0.1, random_state=42)

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,
                             stop_words='english')
features_train = vectorizer.fit_transform(features_train)
features_test  = vectorizer.transform(features_test).toarray()


### a classic way to overfit is to use a small number
### of data points and a large number of features;
### train on only 150 events to put ourselves in this regime
features_train = features_train[:150].toarray()
labels_train   = labels_train[:150]



### your code goes here

######
# Decision Tree
######
from sklearn import tree
from sklearn.metrics import accuracy_score
dt_clf = tree.DecisionTreeClassifier()
dt_clf = dt_clf.fit(features_train, labels_train)
dt_pred = dt_clf.predict(features_test)

print("number of training points: {}".format(len(features_train)))
print("Decision tree accuracy: {}".format(accuracy_score(labels_test, dt_pred)))

best_feats = []
max_feat = 0.0
for index, feat_imp in enumerate(dt_clf.feature_importances_):
    if feat_imp > 0.2:
        best_feats.append({"index" : index, "feat_imp" : feat_imp})
        if feat_imp >= max_feat:
            max_feat_index = index
            max_feat = feat_imp

print("Decision tree's most important feature importance: {}".format(max_feat))
print("Index of most important feature: {}".format(max_feat_index))
print("Best features: {}".format(best_feats))

print("Number of words: {}".format(len(vectorizer.get_feature_names())))
print("Word {}: {}".format(max_feat_index, vectorizer.get_feature_names()[max_feat_index]))


