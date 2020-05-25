#!\usr\bin\python

"""
Load Airport data to mongodb
"""

import csv

def consume_carriers_csv(file):
    """ 
        Carrier codes and Carrier names
    """

    carriers = []

    with open(file, 'r') as inFile:
        reader = csv.DictReader(inFile)
        for row in reader:
            carriers.append({
                'code': row['Code'],
                'name': row['Description']})

    return carriers