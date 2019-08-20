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

###
### email addresses

# How many data points have an email address and no email statistics?