#!/usr/bin/python

"""
    Each leaf in the maildir directory is an email.
    Each child of the maildir directory is a collection of a person's emails.
    Each subdirectory is a folder within that person's email box.

    For each person get a list of the words within all emails in their email box.
    Full data presented as a hash where the person is the key and the words are the value
    This hash is then pickled to a file.

    To support Tf ldf, document parses were changed to individual list entries
"""
import os
import pickle
import sys

import pprint

sys.path.append("./udacity_tools/")
from parse_out_email_text import parseOutText

maildir = "maildir\\"
persons = os.listdir(maildir)
#print(persons)

# One entry in the data list is one parsed email body
# Each parsed email is a list of [person, words]
# Involved parties for an email is not included in parse
# The Data will be pickled for later consumption

persons_words = {}

limit_mails = 0
limit_people = 0

for person in persons:
    #print(person)
    persons_words[person] = []
    #limit_people += 1
    if limit_people < 2:
        for root, dir, files in os.walk("{}\\{}".format(maildir, person)):
            for name in files:
                #limit_mails += 1
                if limit_mails < 6:
                    #print(os.path.join(root, name))
                    open_mail = open(os.path.join(root, name))
                    parsed_mail = [person, parseOutText(open_mail)]
                    persons_words[person].append(parsed_mail[1])
                    open_mail.close()

out = open("email_body_dump.pkl","w")
pickle.dump(persons_words, out)
out.close()

#pprint.pprint(persons_words)
#print(type(data[0][0]))
#print(data[0][0])
#for name in data[:2]:
#    print(name[0])