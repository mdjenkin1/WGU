#!/usr/bin/python
import sys
import pickle
import pprint
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit

# scrubbed dataset
with open("../submission/my_scrubbed_data.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

# feature set
with open("../submission/my_feature_list.pkl", "r") as data_file:
    feature_set = pickle.load(data_file)

# preprocessed data
with open("../submission/my_dataset.pkl", "r") as data_file:
    preped_data = pickle.load(data_file)

# data scaler
with open("../submission/my_data_scaler.pkl", "r") as data_file:
    data_scaler = pickle.load(data_file)

data_matrix = sns.pairplot(preped_data)
#plt.show()
plt.savefig("../pickle_jar/preped_data_pairplot.png")

# regresion fit our data points