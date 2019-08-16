#!/usr/bin/python

""" 
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY"]["bonus"] = 5600000
    
"""

import pickle
import pprint
import re
import copy

######
# Data Prep
######

## Load original dataset
enron_data = pickle.load(open("../pickle_jar/final_project_dataset.pkl"))

## Load manually wrangled poi data
name_file = open("../pickle_jar/poi_names.txt", "rb")
person_parser = re.compile(r'^\((\w)\)\s*(.*)$')                                            # Regex to scrape names from manually wrangled poi data
poi_names_file = set()                                                                      # Data structure for manually wrangled poi

## Variables for answering questions
features_count={}                                                                           # Running count of feature occurrence
nan_count={}                                                                                # Running count of features with NaN value
quant_count={}                                                                              # Running count of features with value
poi_names_ds = set()                                                                        # Data structure for originally flagged poi

cleaned_ds = {}                                                                             # Prepared data ready for deeper learning
no_nan = {}                                                                                 # Special version of dataset with no 'NaN' values

######
# Manually wrangled data
######
for line in name_file:
    person_details = person_parser.match(line)                                               # match and tokenize poi name
    if person_details:                                                                      
        poi_names_file.add(re.sub('[,]', '', person_details.group(2).upper().strip()))      # add the name to the set of poi in the manually wrangled
                                                                                            # strip any commas, leading or trailing whitespace characters
                                                                                            # and convert their name to uppercase

######
# Helper Functions
######

#def CountFeature(feature, dataset, value):
#    running_count = 0
#    for key in dataset:
#        if dataset[key][feature] =
#    return running_count

######
# Initial Exploration and Scrubbing
######

for person in enron_data:
    # normalize the entry key (LASTNAME FIRSTNAME).
    norm_person = re.sub(r'\s\b\w\b| JR|\.','',person).upper()
    enron_data[norm_person] = enron_data.pop(person)

    # Feature counts and new dataset no_nan
    person_features = {}
    for feature in enron_data[norm_person]:
        features_count[feature] = features_count.get(feature, 0) + 1        # Running count of feature occurrence
        if enron_data[norm_person][feature] == 'NaN':
            nan_count[feature] = nan_count.get(feature, 0) + 1              # Running count of feature with NaN value
        else:
            quant_count[feature] = quant_count.get(feature, 0) + 1          # Running count of feature with value
            person_features[feature] = enron_data[norm_person][feature]     # Add {feature : value} to individual person's no_nan dataset
    no_nan[norm_person] = person_features                                   # Add person_features to no_nan dataset

    if (enron_data[norm_person]["poi"]):
        poi_names_ds.add(norm_person)                                       # populate set of poi in original dataset
        #ds_enron_poi.update({norm_person : enron_data[norm_person]})

persons_ds = set(enron_data.keys())                                         # All people in dataset
all_poi = poi_names_ds | poi_names_file                                     # All identified poi
poi_not_in_ds = poi_names_file - persons_ds                                 # Identified poi not in dataset
not_labeled_poi = (poi_names_file - poi_not_in_ds) - poi_names_ds           # Identified poi in dataset but not labelled

# Are there any features with counts less than the number of people?
shorted_features = set()
for feature in features_count:
    if features_count[feature] < len(enron_data):
        shorted_features.add(feature)

######
# Initial Count Report
######

print("***Initial Findings***")
#pprint.pprint(persons_ds)
print("Count of entries in dataset: {}".format(len(enron_data)))
print("Count of features in dataset: {}".format(len(features_count)))
print("Number of features not assigned to everyone: {}".format(len(shorted_features)))
print("Number of POI already labeled in dataset: {}".format(len(poi_names_ds)))
print("Number of POI identified in manual scrape: {}".format(len(poi_names_file)))
print("Number of POI from all sources: {}".format(len(all_poi)))
print("Number of POI not in dataset: {}".format(len(poi_not_in_ds)))
print("Number of POI in dataset and not labeled: {}".format(len(not_labeled_poi)))
print("\r")

######
# Is every entry a person
######

print("***Entries With More Than Two Names***")
for person in no_nan:
    if len(person.split()) > 2: 
        print(person)
        pprint.pprint(no_nan[person])
print("\r")

print("***Entries With Two or Fewer Features***")
for person in no_nan:
    if len(no_nan[person].keys())-1 <= 2:
        print("\r")
        print(person)
        pprint.pprint(no_nan[person])
print("\r")

######
# Dropping Entries
######

pop_person = ['THE TRAVEL AGENCY IN THE PARK']      # Build a list of entries to drop.
                                                    # Explicitly drop "The Travel Agency in the Park"

for person in enron_data:                           # Identify non-NaN features for each entry in our dataset
    if len(no_nan[person].keys()) <= 1:             # If the entry has no features, add it to the list to be dropped
        pop_person.append(person)

print("***These entries will be dropped***")
pprint.pprint(pop_person)
print("\r")


######
# Features, closer look
######

feature_types = {}                                                              # List the types used for each feature
no_nan_features_count = {}                                                      # Running count of no_nan feature occurrence
persons_with_loan_advances = set()
for person in no_nan:
    for feature in no_nan[person]:
        if feature == 'loan_advances': persons_with_loan_advances.add(person)
        no_nan_features_count[feature] = no_nan_features_count.get(feature, 0) + 1     # Running count of no_nan feature occurrence
        f_type = type(no_nan[person][feature]).__name__
        feature_types[feature] = feature_types.get(feature, set([f_type]))

pop_person.append("TOTAL")     

print("***Types in use for features***")
pprint.pprint(feature_types)
print("\r")

print("***Number of entries with valued feature***")
pprint.pprint(no_nan_features_count)
print("\r")

print("***Entries with loan_advances***")
pprint.pprint(persons_with_loan_advances)
print("\r")

### Remove loan_advances











        #if feature_types.has_key(feature):
            #feature_types[feature].update(type(no_nan[person][feature]))
        #    print(type(no_nan[person][feature]))
        #else:
        #    tmp = type(no_nan[person][feature])
        #    print(tmp)
            #feature_types[feature] = set(tmp)



# Feature counts
#    for k in enron_data[norm_person]:
#        features_count[k] = features_count.get(k, 0) + 1                                    # Running count of feature occurrence
#        if enron_data[norm_person][k] == 'NaN':
#            nan_count[k] = nan_count.get(k, 0) + 1                                          # Running count of feature with NaN value
#        else:
#            quant_count[k] = quant_count.get(k, 0) + 1                                      # Running count of feature with value
    
#    if (enron_data[norm_person]["poi"]):
#        poi_names_ds.add(norm_person)                                                          # populate set of poi in original dataset
        #ds_enron_poi.update({norm_person : enron_data[norm_person]})



######
# Second Counts
######




#        poi_not_in_ds = poi_names_file - set(enron_data.keys())
#        print(len(poi_not_in_ds))
#        pprint.pprint(poi_not_in_ds)
#        pprint.pprint(enron_data.keys())

######
# Findings Report
######

#poi_names_union = poi_names_ds|poi_names_file                                                 # Combine the lists of people of interest
#print_report()

######
# Print out findings
######
#def print_report(eds=enron_data, feat=features_count, poi_names_ds=poi_names_ds, poi_names_file=poi_names_file, poi_names_union = poi_names_union, nan_count=nan_count, quant_count=quant_count):
    #print("Features and number of people with that feature")
    #pprint.pprint(features_count)
#print("Count of people in dataset: {}".format(len(enron_data)))
#print("Count of features in dataset: {}".format(len(features_count)))
#print("Count of POI in dataset: {}".format(len(poi_names_ds)))
#print("Count of POI in manual scrape: {}".format(len(poi_names_file)))
#print("Count of POI from all sources: {}".format(len(poi_names_union)))
#print("James Prentice's stock holdings: {}".format(eds["PRENTICE JAMES"]['total_stock_value']))
#print("Wesley Colwell's emails to POI: {}".format(eds["COLWELL WESLEY"]['from_this_person_to_poi']))
#print("Jeffery K Skilling's Exercised Stock Options: {}".format(eds["SKILLING JEFFREY K"]['exercised_stock_options']))
#print("Number of people with a quantified salary: {}".format(quant_count['salary']))
#print("Number of people with an email address: {}".format(quant_count['email_address']))
#type(nan_count)

######
# Of the top executives, who had the highest payment?
######
#top_execs = ('LAY KENNETH','SKILLING JEFFREY','FASTOW ANDREW')                              # Define the top executives
#execs = {name:enron_data[name] for name in top_execs}                                       # Slice out dict values of only the top executives
#winner = max(execs, key=(lambda n: execs[n]['total_payments']))                             # Determine who made the most money
#print("{} had the largest payments at {}".format(winner,execs[winner]['total_payments']))  # Report findings

#print("****END OF THE BEGINNING****")
#print("****BEGINNING OF THE END****")

#count_nan_tpay = 0
#for name in enron_data: 
#    if enron_data[name]['total_payments'] == 'NaN':
#        count_nan_tpay += 1

#count_poi_nan_tpay = 0
#for name in ds_enron_poi: 
#    if ds_enron_poi[name]['total_payments'] == 'NaN':
#        count_poi_nan_tpay += 1

#print("Count of people without total_payment: {}".format(count_nan_tpay))
#print("Percent of people without total_payment: {}%".format(100*count_nan_tpay/len(enron_data)))

#print("Count of people of interest without total_payment: {}".format(count_poi_nan_tpay))
#print("Percent of people of interest without total_payment: {}%".format(100*count_poi_nan_tpay/len(ds_enron_poi)))

######
# NaN Financials
######

#def add_features(person):
#    return {
#        'poi' : True,
#        'bonus': 'NaN',
#        'deferral_payments': 'NaN',
#        'deferred_income': 'NaN',
#        'director_fees': 'NaN',
#        'email_address': 'NaN',
#        'exercised_stock_options': 'NaN',
#        'expenses': 'NaN',
#        'from_messages': 'NaN',
#        'from_poi_to_this_person': 'NaN',
#        'from_this_person_to_poi': 'NaN',
#        'loan_advances': 'NaN',
#        'long_term_incentive': 'NaN',
#        'other': 'NaN',
#        'restricted_stock': 'NaN',
#        'restricted_stock_deferred': 'NaN',
#        'salary': 'NaN',
#        'shared_receipt_with_poi': 'NaN',
#        'to_messages': 'NaN',
#        'total_payments': 'NaN',
#        'total_stock_value': 'NaN'
#    }

# Add NaN features and true POI to the list of people in the POI file
#file_data = {}
#for name in poi_names_all: file_data.update({name:add_features(name)})


#data_types = {}
#for name in enron_data:
#    for feature in enron_data[name]:
#        if enron_data[name][feature] != 'NaN':
#            print(name[feature])
            #if data_types[feature]:
            #    print("existing non-null feature")
                # data_types[feature].update(type(enron_data[name][feature]))
            #else:
            #    print("new non-null feature")
                #data_types[feature].set(type(enron_data[name][feature]))


#pprint.pprint(file_data)

# Make a dict of all people by updating a copy of the enron_data dict
#all_persons = copy.deepcopy(file_data)
#print(len(all_persons))
#all_persons.update(enron_data)
#print(len(all_persons))

#pprint.pprint(all_persons)

#count_nan_tpay = 0
#for name in all_persons: 
#    if all_persons[name]['total_payments'] == 'NaN':
#        count_nan_tpay += 1

#pprint(data_types)

#print("DataSet People of Interest")
#pprint.pprint(poi_names_ds)

#print("Manual People of Interest")
#pprint.pprint(poi_names_file)

#print("All People of Interest")
#pprint.pprint(poi_names_all)