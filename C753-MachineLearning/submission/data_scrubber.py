#!/usr/bin/python
import re

"""
    Finalized data prep. 
    raw_data is expecting a dictionary of dictionaries.
        observed persons are keys in the parent dict
        features are the keys in the child dict
        values in the child dict are the measurements
    target_features is the list of feature you want to investigate.
        For my project that list is: ['poi', 'exercised_stock_options', 'bonus', 'expenses', 'salary']
    
    returns: skipped_persons, processed_data
"""

def scrub_data(raw_data, target_features):

    ##
    ## Helpers
    processed_data = {}                                                 # return structure
    skipped_persons = set(['THE TRAVEL AGENCY IN THE PARK', 'TOTAL'])   # Static entries to be dropped
    impute_zero = lambda x: 0 if x == "NaN" else x                      # Simple imputator of NaN values
    
    # These feature lists have calculated values to validate
    stock_features = ['restricted_stock_deferred', 'exercised_stock_options', 'restricted_stock']
    payment_features = ['salary', 'deferral_payments', 'bonus', 'deferred_income', 'expenses', 
                        'loan_advances', 'other', 'long_term_incentive', 'director_fees']

    ##
    ## Data Clean and Prep
    for person in raw_data:
        
        # Name Normalization
        norm_person = re.sub(r'\s\b\w\b| JR|\.','',person).upper()
        
        # if this is a predetermined entry to drop then drop
        if norm_person in skipped_persons: continue

        ##
        ## Determine if this is an entry that should be skipped
        # Skip anyone without values in our target feature set
        has_value = False       
        for feature in target_features:
            if feature != 'poi' and raw_data[person][feature] != 'NaN':
                has_value = True
                break
        if not has_value:
            skipped_persons.add(norm_person)  # Add them to the skipped set so we can report it
            #print("skipping {} for no value".format(person))
            continue

        # Skip anyone with an incorrect stock total
        calc_total_stock = 0    
        for feature in stock_features: calc_total_stock += impute_zero(raw_data[person][feature])
        if calc_total_stock != impute_zero(raw_data[person]['total_stock_value']):
            skipped_persons.add(norm_person)  # Add them to the skipped set so we can report it
            #print("skipping {} for bad stock".format(person))
            continue

        # Skip anyone with an incorrect payment total
        calc_total_pay = 0
        for feature in payment_features: calc_total_pay += impute_zero(raw_data[person][feature]) 
        if calc_total_pay != impute_zero(raw_data[person]['total_payments']):
            skipped_persons.add(norm_person)  # Add them to the skipped set so we can report it
            #print("skipping {} for bad pay".format(person))
            continue    

        ##
        ## If they made it this far, add them to the processed dataset
        processed_data[norm_person] = {feature : raw_data[person][feature] for feature in target_features}
    
    ##
    ## Return the processed data and the set of people we skipped
    return skipped_persons, processed_data