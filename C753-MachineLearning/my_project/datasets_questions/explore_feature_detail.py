#!/usr/bin/python
import pickle
import pprint
import sys
import pandas as pd

sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit

"""
    Get feature details from cleaned dataset.
"""

######
# Feature detail exploration
######

cleaned_data = pickle.load(open("../pickle_jar/final_project_dataset_cleaned.pkl"))

### 
### Basic statistics

# Feature grouping
fin_features = ['poi','salary', 'deferral_payments', 'total_payments', 'bonus', 
    'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 
    'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock', 'director_fees']

email_features = ['poi', 'to_messages', 'from_poi_to_this_person', 'from_messages', 
    'from_this_person_to_poi', 'shared_receipt_with_poi'] 

#fin_data = featureFormat(cleaned_data, fin_features)
fin_data = featureFormat(cleaned_data, fin_features, remove_NaN=False)
_, fin_data_np_arrays = targetFeatureSplit( fin_data )
fin_data_df = pd.DataFrame(fin_data_np_arrays, columns = fin_features[1:])

#email_data = featureFormat(cleaned_data, email_features)
email_data = featureFormat(cleaned_data, email_features, remove_NaN=False)
_, email_data_np_arrays = targetFeatureSplit( email_data )
email_data_df = pd.DataFrame(email_data_np_arrays, columns = email_features[1:])

pd.set_option('precision',2)
pd.set_option('display.float_format', '{:.2f}'.format)

pprint.pprint(fin_data_df.describe())
pprint.pprint(email_data_df.describe())
print('\r')

###
### email addresses

# How many data points have an email address and no email statistics?
email_addr_count = 0
email_stat_counts = {}
for person in cleaned_data:
    if cleaned_data[person]['email_address'] != 'NaN':
        stat_count = 0
        email_addr_count += 1
        for feature in email_features[1:]:
            if cleaned_data[person][feature] != 'NaN': stat_count += 1
        email_stat_counts.update({person:stat_count})
        #print(cleaned_data[person]['email_address'])

print("{} email addresses counted".format(email_addr_count))
print("***Number of email stats for persons with email addresses***")
pprint.pprint(email_stat_counts)
print('\r')

financial_only = set()
email_stats_only = set()
financial_and_emails = set()
elephant_in_cairo = set()

# has_email_statistics and has_financial feature creation has been moved to data_prep.py
#for person in cleaned_data:
#    # populate has_email_statistics
#    if person in email_stat_counts.keys() and email_stat_counts[person] > 0:
#        cleaned_data[person].update({"has_email_statistics" : True})
#    else:
#        cleaned_data[person].update({"has_email_statistics" : False})
#    
#    # populate has_financials. assume no, change if yes.
#    cleaned_data[person].update({"has_financial" : False})
#    for feat in fin_features[1:]:
#        if cleaned_data[person][feat] != 'NaN': 
#            cleaned_data[person]["has_financial"] = True
#            break

# Inspect has_email_statistics and has_financial
for person in cleaned_data:
    if (cleaned_data[person]["has_email_statistics"] and cleaned_data[person]["has_financial"]):
        financial_and_emails.add(person)
    elif (cleaned_data[person]["has_email_statistics"]):
        email_stats_only.add(person)
    elif (cleaned_data[person]["has_financial"]):
        financial_only.add(person)
    else:
        elephant_in_cairo.add(person)


print("***Persons with both Financial and Email data***")
pprint.pprint(financial_and_emails)
print("\r")
print("***Persons with only Email data***")
pprint.pprint(email_stats_only)
print("\r")
print("***Persons with only Financial data***")
pprint.pprint(financial_only)
print("\r")
print("***No elephants should be in cairo***")
print("***Elephants have no values***")
pprint.pprint(elephant_in_cairo)
print("\r")


