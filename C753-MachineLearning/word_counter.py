#!/usr/bin/python

"""
    Take a rough count of the words found in each vocabulary.
"""

import os
import pickle
import sys
import pprint
import collections

infile = open("preprocessed_email_dump_funsize.pkl","rb")
persons_vocabs = pickle.load(infile)
infile.close()

#pprint.pprint(data)

word_counts = collections.Counter()
for person in persons_vocabs:
    word_counts.update(persons_vocabs[person].get_feature_names())

# For each word we have a count of how many corpora it appears in
# Now, let's get a count of how many words appear in the same number of corpora.
# e.g. if 2 words appear in 7 corpora then count_of_counts[7] == 2
count_of_counts = collections.Counter()
for word in word_counts:
    count_of_counts.update(str(word_counts[word]))

print("{} words in total".format(len(word_counts)))

for count in sorted(count_of_counts):
    print("{} words appear in {} corpora".format(count_of_counts[count], count))
