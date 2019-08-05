#!/usr/bin/python

"""
    https://towardsdatascience.com/pca-using-python-scikit-learn-e653f8989e60
    
    Each word stem is a vocabulary feature. The TfIdf weight of that stem directly relates to its weight in the vocabulary.
    
    Construct a panda's dataframe with the following Structure:
    Each column is a stem/feature
    Each row is a person
    Each 


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

# obtain a list of all stems as features. These are the column headers
word_counts = collections.Counter()
for person in persons_vocabs:
    word_counts.update(persons_vocabs[person].get_feature_names())
    stem_weights = {}


cols = word_counts.keys()
vocabs_df = pd.df()


# Standardize the data

# Perform dimensionality reduction by PCA

# Export the resulting dataframe
