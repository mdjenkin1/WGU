#!/usr/bin/python

"""
    https://towardsdatascience.com/pca-using-python-scikit-learn-e653f8989e60
    
    Each word stem is a vocabulary feature. The TfIdf weight of that stem directly relates to its weight in the vocabulary.
    Each vocabulary will be a 


"""

import sys
import os
import pickle
import pandas as pd


person_vocabs = pickle.load(open('.\preprocessed_email_dump_funsize.pkl','rb'))
#person_vocabs = pickle.load(open('.\preprocessed_email_dump.pkl','rb'))

# Load the data to a pandas dataframe

# Standardize the data

# Perform dimensionality reduction by PCA

# Export the resulting dataframe
