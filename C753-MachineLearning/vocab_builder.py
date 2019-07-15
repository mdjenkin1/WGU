#!/usr/bin/python

"""
Import pickled data created by get_persons_emails.
For each person, use Tf ldf to determine that person's vocabulary.

Reminder:
A TfidfVectorizer object consists of a count matrix and a list of feature names.
The count matrix is documents by row and words by column with counts of the word in that document.
Feature names are the words for each column. Accessible by get_feature_names()
"""

import os
import sys
import pickle

from sklearn import TfidfVectorizer

import pprint

persons_emails = pickle.load("email_body_dump.pkl")
persons_vocab = {}

limit_persons = 0

for person in persons_emails:
    if limit_persons < 2:
        limit_persons += 1
        vectorizer = TfidfVectorizer(stop_words='english')
        vectorizer.fit_transform(persons_emails[person])
        persons_vocab[person] = vectorizer
    pprint.pprint(persons_vocab[person].get_feature_names)

pickle.dump(persons_words, open("vocab_for_persons.pkl", "w"))

