#!/usr/bin/python

"""
    Each leaf in the maildir directory is an email.
    Each child of the maildir directory is a collection of a person's emails.
    Each subdirectory is a folder within that person's email box.

    For each person get a list of the words within all emails in their email box.
    Full data presented as a hash where the person is the key and the words are the value
    This hash is then pickled to a file.

    To support Tf ldf, document parses were changed to individual list entries

    Reminder:
    A TfidfVectorizer object consists of a count matrix and a list of feature names.
    The count matrix has documents by row and words by column with counts of the word in that document.
    Feature names are the words for each column. Accessible by get_feature_names()
"""
import os
import pickle
import sys
import pprint

sys.path.append("./udacity_tools/")
from parse_out_email_text import parseOutText
from sklearn.feature_extraction.text import TfidfVectorizer

# Structure and tool prep
maildir = "maildir\\"
persons = os.listdir(maildir)
persons_vocab = {}

#processing control
limit_mails = 0
limit_people = 0

# pre-process email by person
for person in persons:
    #zlimit_people += 1
    if limit_people < 2:
        corpus = []
        for root, dir, files in os.walk("{}\\{}".format(maildir, person)):
            # build the corpus, one email at a time
            for file in files:
                #limit_mails += 1
                if limit_mails < 6:
                    open_mail = open(os.path.join(root, file))
                    parsed_mail = [parseOutText(open_mail)]
                    corpus.append(parsed_mail[0])
                    open_mail.close()
        # Weigh words within the person's corpus to generate a vocabulary
        vectorizer = TfidfVectorizer(stop_words='english')
        vectorizer.fit_transform(corpus)
        persons_vocab[person] = vectorizer

out = open("preprocessed_email_dump.pkl","wb")
pickle.dump(persons_vocab, out)
out.close()