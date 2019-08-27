#!/usr/bin/python
import pickle
import pprint
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit

"""
    Get feature details from cleaned dataset.
"""

######
# Feature detail exploration
######

cleaned_data_no_loan = pickle.load(open("../pickle_jar/final_project_dataset_cleaned_no_loan.pkl"))
cleaned_data = pickle.load(open("../pickle_jar/final_project_dataset_cleaned.pkl"))

### 
### Basic statistics

# Feature grouping
fin_features_no_loan = ['poi','salary', 'deferral_payments', 'total_payments', 'bonus', 
    'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 
    'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock', 'director_fees']

fin_features = ['poi','salary', 'deferral_payments', 'total_payments', 'bonus', 
    'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 'loan_advances',
    'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock', 'director_fees']

email_features = ['poi', 'to_messages', 'from_poi_to_this_person', 'from_messages', 
    'from_this_person_to_poi', 'shared_receipt_with_poi'] 

fin_data_no_loan = featureFormat(cleaned_data_no_loan, fin_features_no_loan)
_, fin_data_no_loan_np_arrays = targetFeatureSplit( fin_data_no_loan )
fin_data_no_loan_df = pd.DataFrame(fin_data_no_loan_np_arrays, columns = fin_features_no_loan[1:])

fin_data_no_loan_nulls = featureFormat(cleaned_data_no_loan, fin_features_no_loan, remove_NaN=False)
_, fin_data_no_loan_nulls_np_arrays = targetFeatureSplit( fin_data_no_loan_nulls )
fin_data_no_loan_nulls_df = pd.DataFrame(fin_data_no_loan_nulls_np_arrays, columns = fin_features_no_loan[1:])

fin_data = featureFormat(cleaned_data, fin_features)
_, fin_data_np_arrays = targetFeatureSplit( fin_data )
fin_data_df = pd.DataFrame(fin_data_np_arrays, columns = fin_features[1:])

fin_data_nulls = featureFormat(cleaned_data, fin_features, remove_NaN=False)
_, fin_data_np_arrays_nulls = targetFeatureSplit( fin_data_nulls )
fin_data_nulls_df = pd.DataFrame(fin_data_np_arrays_nulls, columns = fin_features[1:])


#email_data = featureFormat(cleaned_data, email_features)
email_data = featureFormat(cleaned_data, email_features, remove_NaN=False)
_, email_data_np_arrays = targetFeatureSplit( email_data )
email_data_df = pd.DataFrame(email_data_np_arrays, columns = email_features[1:])

pd.set_option('precision',2)
pd.set_option('display.float_format', '{:.2f}'.format)

print("***Financial Data Summary, including null as zeros***")
pprint.pprint(fin_data_no_loan_df.describe())
print("\r")
print("***Financial Data Summary, excluding nulls***")
pprint.pprint(fin_data_no_loan_nulls_df.describe())
print("\r")
print("***Email Statistics***")
pprint.pprint(email_data_df.describe())
print('\r')

###
### email addresses

# How many data points have an email address and no email statistics?
email_addr_count = 0
email_stat_counts = {}
for person in cleaned_data_no_loan:
    if cleaned_data_no_loan[person]['email_address'] != 'NaN':
        stat_count = 0
        email_addr_count += 1
        for feature in email_features[1:]:
            if cleaned_data_no_loan[person][feature] != 'NaN': stat_count += 1
        email_stat_counts.update({person:stat_count})
        #print(cleaned_data_no_loan[person]['email_address'])

print("{} email addresses counted".format(email_addr_count))
print("***Number of email stats for persons with email addresses***")
pprint.pprint(email_stat_counts)
print('\r')

financial_only = set()
email_stats_only = set()
financial_and_emails = set()
elephant_in_cairo = set()

# has_email_statistics and has_financial feature creation has been moved to data_prep.py
#for person in cleaned_data_no_loan:
#    # populate has_email_statistics
#    if person in email_stat_counts.keys() and email_stat_counts[person] > 0:
#        cleaned_data_no_loan[person].update({"has_email_statistics" : True})
#    else:
#        cleaned_data_no_loan[person].update({"has_email_statistics" : False})
#    
#    # populate has_financials. assume no, change if yes.
#    cleaned_data_no_loan[person].update({"has_financial" : False})
#    for feat in fin_features_no_loan[1:]:
#        if cleaned_data_no_loan[person][feat] != 'NaN': 
#            cleaned_data_no_loan[person]["has_financial"] = True
#            break

# Inspect has_email_statistics and has_financial
for person in cleaned_data_no_loan:
    if (cleaned_data_no_loan[person]["has_email_statistics"] and cleaned_data_no_loan[person]["has_financial"]):
        financial_and_emails.add(person)
    elif (cleaned_data_no_loan[person]["has_email_statistics"]):
        email_stats_only.add(person)
    elif (cleaned_data_no_loan[person]["has_financial"]):
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

###
### Financial Data scaling
 
print("***Financial Data Summary, including null as zeros***")
pprint.pprint(fin_data_no_loan_df.describe())
print("\r")
print("***Financial Data Summary, excluding nulls***")
pprint.pprint(fin_data_no_loan_nulls_df.describe())
print("\r")

#print(fin_data_no_loan_nulls_df.describe().index)
#print(fin_data_no_loan_nulls_df.describe().loc['count'])

bool_fin_no_loan = fin_data_no_loan_nulls_df.describe().loc['count'] / fin_data_no_loan_df.describe().loc['count']

print("*** Observations % Populated : {}***".format(bool_fin_no_loan.size))
pprint.pprint(bool_fin_no_loan)
print("\r")

print("*** Observations > 50% Populated : {}***".format(bool_fin_no_loan[bool_fin_no_loan >= 0.50].size))
pprint.pprint(bool_fin_no_loan[bool_fin_no_loan >= 0.5])
print("\r")

print("*** Observations > 66% Populated : {}***".format(bool_fin_no_loan[bool_fin_no_loan >= 0.66].size))
pprint.pprint(bool_fin_no_loan[bool_fin_no_loan >= 0.66])
print("\r")

print("*** Observations > 75% Populated : {}***".format(bool_fin_no_loan[bool_fin_no_loan >= 0.75].size))
pprint.pprint(bool_fin_no_loan[bool_fin_no_loan >= 0.75])
print("\r")

print("*** Observations < 30% Populated : {}***".format(bool_fin_no_loan[bool_fin_no_loan >= 0.25].size))
pprint.pprint(bool_fin_no_loan[bool_fin_no_loan <= 0.30])
print("\r")

###
### Replaced loan_advance
bool_fin = fin_data_nulls_df.describe().loc['count'] / fin_data_df.describe().loc['count']

print("*************************")
print("***Feature Populations***")
print("****With Loan Advance****")
print("*************************")

print("*** Observations % Populated : {}***".format(bool_fin.size))
pprint.pprint(bool_fin)
print("\r")

print("*** Observations > 50% Populated : {}***".format(bool_fin[bool_fin >= 0.50].size))
pprint.pprint(bool_fin[bool_fin >= 0.5])
print("\r")

print("*** Observations > 66% Populated : {}***".format(bool_fin[bool_fin >= 0.66].size))
pprint.pprint(bool_fin[bool_fin >= 0.66])
print("\r")

print("*** Observations > 75% Populated : {}***".format(bool_fin[bool_fin >= 0.75].size))
pprint.pprint(bool_fin[bool_fin >= 0.75])
print("\r")

print("*** Observations < 30% Populated : {}***".format(bool_fin[bool_fin >= 0.25].size))
pprint.pprint(bool_fin[bool_fin <= 0.30])
print("\r")

