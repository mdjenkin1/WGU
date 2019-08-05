#!/usr/bin/python

"""
    https://towardsdatascience.com/pca-using-python-scikit-learn-e653f8989e60
    https://stackoverflow.com/questions/34449127/sklearn-tfidf-transformer-how-to-get-tf-idf-values-of-given-words-in-documen
    
    Each word stem is a vocabulary feature. The TfIdf weight of that stem directly relates to its weight in the vocabulary.
    persons_vocab[person] = {"term_matrix": term_matrix, "tfidfvec": vectorizer}

    Construct a panda's dataframe with the following Structure:
    Each column is a stem/feature
    Each row is a person
    Each cell is the word weight for that person

    Each person's vocabulary will be an observation in the dataframe


"""

import sys
import os
import pickle
import pandas as pd
import numpy as np

persons_vocabs = pickle.load(open('.\preprocessed_email_dump_funsize.pkl','rb'))
#person_vocabs = pickle.load(open('.\preprocessed_email_dump.pkl','rb'))

### Structure the data to be loaded to a pandas dataframe

## One creation option. Computation overhead is huge
# Dataframe created by orient='index' with columns=word_counts.keys()
# A running list of stems as features. These are the column headers for the monolith
# word_counts = collections.Counter()

# first pass
for person in persons_vocabs:
    word_counts.update(persons_vocabs[person]['tfidfvec'].get_feature_names())
    persons_term_weights = {}
    for doc in persons_vocabs['term_matrix']:


#cols = word_counts.keys()
vocabs_df = pd.df()


# Standardize the data

# Perform dimensionality reduction by PCA

# Export the resulting dataframe
