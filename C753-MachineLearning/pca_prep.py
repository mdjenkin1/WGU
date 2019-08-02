#!/usr/bin/python

"""
    https://towardsdatascience.com/pca-using-python-scikit-learn-e653f8989e60
    
    Each word stem is a vocabulary feature. The importance of that stem to the person's vocabulary is determined by TfIdf weights
    This gives each vocabulary a huge amount of dimensionality that needs to be reduced.
    The goal here is to restructure the vocabularies we have such they can be fed into a PCA algorithm to determine the most common vocabulary identifiers.
"""