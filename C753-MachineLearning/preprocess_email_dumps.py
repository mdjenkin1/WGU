#!/usr/bin/python

"""
Import pickled data created by dump_emails.py.
pre-process the emails

Reminder:
A TfidfVectorizer object consists of a count matrix and a list of feature names.
The count matrix is documents by row and words by column with counts of the word in that document.
Feature names are the words for each column. Accessible by get_feature_names()
"""

import os
import sys
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.snowball import SnowballStemmer

import pprint

inFile = open("email_body_dump.pkl")
persons_emails = pickle.load(inFile)
inFile.close()

persons_vocab = {}
limit_persons = 0

vectorizer = TfidfVectorizer(stop_words='english')
tokenizer = RegexpTokenizer(r'\w+')
stemmer = SnowballStemmer()

def token_stemmer(token, stemmer):
    stem = stemmer(token)
    return stem

for person, emails in persons_emails.items():
    if limit_persons < 3:
        #limit_persons += 1
        toked_emails = []
        for email in emails:
            toked_email = []
            tokens = tokenizer.tokenize(email)
            for token in tokens:
                toked_email token_stemmer(token,stemmer)

        vectorizer.fit_transform(persons_emails[person])
        persons_vocab[person] = vectorizer
        #pprint.pprint("{} has {} emails".format(person, len(persons_emails[person])))
        #pprint.pprint("{} has {} words".format(person,len(persons_vocab[person].get_feature_names())))

out = open("tf-idf_weighted_persons_vocab.pkl", "wb")
pickle.dump(persons_vocab, out)
out.close()