#!/usr/bin/python

"""
    vectorize_text.py is the example that leverages get_persons_emails.parseOutText.
    It functions by leveraging a file for each person it will process.
    Each file contains a list of the emails for that person with relative pathing.
    
"""
import os
import pickle
import re
import sys

import pprint

sys.path.append("./udacity_tools/")
from parse_out_email_text import parseOutText


maildir = "maildir\\"
persons = os.listdir(maildir)
#print(persons)

data = []

limit_mails = 0
limit_people = 0

for person in persons:
    #print(person)
    limit_people += 1
    if limit_people < 2:
        for root, dir, files in os.walk("{}\\{}".format(maildir, person)):
            for name in files:
                limit_mails += 1
                if limit_mails < 3:
                    #print(os.path.join(root, name))
                    open_mail = open(os.path.join(root, name))
                    parsed_mail = [person, parseOutText(open_mail)]
                    data.append(parsed_mail)
                    open_mail.close()

pprint.pprint(data[:2])