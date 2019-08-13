#!/usr/bin/python

import sys
import pickle
sys.path.append("./tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data


### Task 1: Select what features you'll use.

### Task 2: Remove outliers
### Task 3: Create new feature(s)
### Task 4: Try a variety of classifiers
### Task 5: Tune your classifier to achieve better than .3 precision 
### Task 6: Dump your classifier, dataset, and features_list 
