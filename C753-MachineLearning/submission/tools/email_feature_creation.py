#!\usr\bin\python


def has_features(data, person, features):
    has_features = True
    for feat in features:
        if data[person][feat] == 0 or data[person][feat] == 'NaN':
            has_features = False
            break
    return has_features


def addEmailFlowFeatures(dataset):
    inmail_features = ['from_messages', 'from_poi_to_this_person', 'shared_receipt_with_poi']
    outmail_features = ['to_messages', 'from_this_person_to_poi']
    for person in dataset:
        has_inmail_stats = True
        has_outmail_stats = True

        if(has_features(dataset, person, inmail_features)):
            dataset[person].update({
                "percent_email_flow_from_poi" : 
                    dataset[person]["from_poi_to_this_person"]/dataset[person]["from_messages"],
                "percent_email_flow_shared_receipt" : 
                    dataset[person]["shared_receipt_with_poi"]/dataset[person]["from_messages"]
            })
        else:
            dataset[person].update({
                "percent_email_flow_from_poi" : 'NaN',
                "percent_email_flow_shared_receipt" : 'NaN'
            })

        if(has_features(dataset, person, outmail_features)):
            dataset[person].update({
                "percent_email_flow_to_poi" : 
                    dataset[person]["from_this_person_to_poi"]/dataset[person]["to_messages"]
            })
        else:
            dataset[person].update({
                "percent_email_flow_to_poi" : 'NaN'
            })
    return dataset
