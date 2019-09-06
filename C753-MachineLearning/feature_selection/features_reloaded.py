#!/usr/bin/python

import pickle
import pprint
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append("../submission/")
sys.path.append("../tools/")
from data_scrubber import scrubData
from email_feature_creation import addEmailFlowFeatures
from feature_format import featureFormat, targetFeatureSplit

with open("../pickle_jar/final_project_dataset.pkl", "rb") as data_file:
    data_dict = pickle.load(data_file)

all_features = ['poi','salary', 'deferral_payments', 'total_payments', 'bonus', 
    'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 
    'loan_advances', 'exercised_stock_options', 'other', 'long_term_incentive', 
    'restricted_stock', 'director_fees', 'to_messages', 'from_poi_to_this_person', 
    'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi', 'email_address']

fin_features = ['poi','salary', 'deferral_payments', 'total_payments', 'bonus', 
    'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 
    'loan_advances', 'exercised_stock_options', 'other', 'long_term_incentive',
    'restricted_stock', 'director_fees']

email_features = ['poi', 'to_messages', 'from_poi_to_this_person', 'from_messages', 
    'from_this_person_to_poi', 'shared_receipt_with_poi']


dropped, full_dataset = scrubData(data_dict, all_features)

print("These entries were removed from the dataset")
pprint.pprint(dropped)
print("\r")

##
# Dimension the intersection of financial and email data
num_with_email_addr = 0
num_with_email_stats = 0
num_with_fin = 0
num_with_both = 0
poi_with_email = 0
for person in full_dataset:
    full_dataset[person].update({"has_email_statistics" : False})
    full_dataset[person].update({"has_financial" : False})

    if full_dataset[person]['email_address'] != 'NaN':
        num_with_email_addr += 1
        for feature in email_features[2:]:
            if full_dataset[person][feature] != 'NaN':
                num_with_email_stats += 1
                full_dataset[person]["has_email_statistics"] = True
                break

    # has_financial
    for feat in fin_features[1:]:
        if full_dataset[person][feat] != 'NaN': 
            num_with_fin += 1
            full_dataset[person]["has_financial"] = True
            break

    if full_dataset[person]["has_email_statistics"] and full_dataset[person]["has_financial"]: num_with_both += 1
    if full_dataset[person]["has_email_statistics"] and full_dataset[person]["poi"]: poi_with_email += 1

print("Number of people with an email address: {}".format(num_with_email_addr))
print("Number of people with email stats: {}".format(num_with_email_stats))
print("Number of people with financial data: {}".format(num_with_fin))
print("Number of people with both data types: {}".format(num_with_both))
print("Number of poi with email stats: {}".format(poi_with_email))
print("\r")


#data = featureFormat(full_dataset, all_features)
#labels, features = targetFeatureSplit(data)

#print("Full dataset as dataframe")
#pprint.pprint(data)

###
### Email Feature exploration and transformation
###

# double up on 'poi' because of the way the feature splitter works.
sns_email_features = ['poi','poi', 'from_messages', 'from_poi_to_this_person', 
    'shared_receipt_with_poi', 'to_messages', 'from_this_person_to_poi']
#inmail_features = sns_email_features[2:5]
#outmail_features = sns_email_features[5:]

sns_email_data = featureFormat(full_dataset, sns_email_features)
_, sns_email_data_np_arrays = targetFeatureSplit(sns_email_data)
sns_email_data_df = pd.DataFrame(sns_email_data_np_arrays, columns = sns_email_features[1:])


#mail_matrix = sns.pairplot(sns_email_data_df, hue='poi', vars=sns_email_features[2:])
#plt.show()
#plt.savefig("../images/emails_all_pairplot.png")

#inmail_matrix = sns.pairplot(sns_email_data_df, hue='poi', vars=sns_email_features[2:5])
#plt.show()
#plt.savefig("../images/inmail_pairplot.png")

#outmail_matrix = sns.scatterplot(sns_email_data_df['to_messages'], sns_email_data_df['from_this_person_to_poi'], hue=sns_email_data_df['poi'])
#plt.show()
#plt.savefig("../images/outmail_scatter.png")

###
### flow of emails to and from poi as a percent of email volume
###

new_dataset = addEmailFlowFeatures(full_dataset)
#print("Full Dataset with new features")
#pprint.pprint(new_dataset)

# double up on 'poi' because of the way the feature splitter works.
#"percent_email_flow_shared_receipt" is broken because of buggy source feature
new_email_features = ['poi', 'poi', #'percent_email_flow_shared_receipt', 
    'percent_email_flow_from_poi', 'percent_email_flow_to_poi']

new_email_data = featureFormat(new_dataset, new_email_features)
_, new_email_data_np_arrays = targetFeatureSplit(new_email_data)
new_email_data_df = pd.DataFrame(new_email_data_np_arrays, columns = new_email_features[1:])

#email_flow_boxplot = sns.boxplot(data=new_email_data_df)
#plt.show()
#plt.savefig("../images/broken_feature.png")
#plt.savefig("../images/still_broken_feature.png")

persons_with_more_from_poi = 0
persons_with_more_shared_poi = 0
persons_with_more_to_poi = 0
for person in new_dataset:
    if new_dataset[person]['from_messages'] != 'NaN':
        #if new_dataset[person]['from_messages'] <= new_dataset[person]['from_poi_to_this_person']:
        if new_dataset[person]['to_messages'] <= new_dataset[person]['from_poi_to_this_person']:
            persons_with_more_from_poi += 1
            print("{} recieved {} messages from poi but only had {} messages in their inbox.".format(person, new_dataset[person]['from_poi_to_this_person'], new_dataset[person]['from_messages']))
            print("{} recieved {} messages from poi and had {} messages in their outbox.".format(person, new_dataset[person]['from_poi_to_this_person'], new_dataset[person]['to_messages']))
        #if new_dataset[person]['from_messages'] <= new_dataset[person]['shared_receipt_with_poi']:
        if new_dataset[person]['to_messages'] <= new_dataset[person]['shared_receipt_with_poi']:
            persons_with_more_shared_poi += 1
            print("{} was on {} messages with poi but only had {} messages in their inbox.".format(person, new_dataset[person]['shared_receipt_with_poi'], new_dataset[person]['from_messages']))
            print("{} was on {} messages with poi and had {} messages in their outbox.".format(person, new_dataset[person]['shared_receipt_with_poi'], new_dataset[person]['to_messages']))
            
    if new_dataset[person]['to_messages'] != 'NaN':
        #if new_dataset[person]['to_messages'] <= new_dataset[person]['from_this_person_to_poi']:
        if new_dataset[person]['from_messages'] <= new_dataset[person]['from_this_person_to_poi']:
            print("{} recieved {} messages from poi but only had {} messages in their outbox.".format(person, new_dataset[person]['from_this_person_to_poi'], new_dataset[person]['to_messages']))
            print("{} recieved {} messages from poi and had {} messages in their inbox.".format(person, new_dataset[person]['from_this_person_to_poi'], new_dataset[person]['from_messages']))
            persons_with_more_to_poi += 1

print("There are {} people with more mail from poi than mail in their inbox".format(persons_with_more_from_poi))
print("There are {} people with more mail shared with poi than mail in their inbox".format(persons_with_more_shared_poi))
print("There are {} people that sent more mail to poi than mail in their outbox".format(persons_with_more_to_poi))

outmail_features = ['poi', 'poi', 'percent_email_flow_to_poi']

outmail_data = featureFormat(new_dataset, outmail_features)
_, outmail_data_np_arrays = targetFeatureSplit(outmail_data)
outmail_data_df = pd.DataFrame(outmail_data_np_arrays, columns = outmail_features[1:])

outmail_boxplot = sns.boxplot(x='poi', y='percent_email_flow_to_poi', data=outmail_data_df)
#plt.show()
plt.savefig("../images/outmail_compare.png")

kept_features = ['poi','salary', 'deferral_payments', 'bonus', 'restricted_stock_deferred', 
    'deferred_income', 'expenses', 'exercised_stock_options', 'other', 'long_term_incentive', 
    'restricted_stock', 'director_fees', 'to_messages', 'from_this_person_to_poi', 'percent_email_flow_to_poi']