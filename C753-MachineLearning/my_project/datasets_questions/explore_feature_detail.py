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

#pprint.pprint(cleaned_data)

fin_features = ['poi','salary', 'deferral_payments', 'total_payments', 'bonus', 
    'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 
    'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock', 'director_fees']

email_features = ['poi', 'to_messages', 'from_poi_to_this_person', 'from_messages', 
    'from_this_person_to_poi', 'shared_receipt_with_poi'] 

fin_data = featureFormat(cleaned_data, fin_features)
_, fin_data_np_arrays = targetFeatureSplit( fin_data )
fin_data_df = pd.DataFrame(fin_data_np_arrays, columns = fin_features[1:])

email_data = featureFormat(cleaned_data, email_features)
_, email_data_np_arrays = targetFeatureSplit( email_data )
email_data_df = pd.DataFrame(email_data_np_arrays, columns = email_features[1:])

#pprint.pprint(type(fin_data))
#pprint.pprint(type(fin_data_np_arrays))
#pprint.pprint(fin_data_np_arrays)
#pprint.pprint(fin_data_np_arrays)
#pprint.pprint(fin_data_df)
#pprint.pprint(email_data_df)

#print(type(fin_data_df))
#print(type(email_data_df))

pd.set_option('precision',2)

pprint.pprint(fin_data_df.describe())
pprint.pprint(email_data_df.describe())
