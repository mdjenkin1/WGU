# Udacity C753 Machine Learning Project

The majority of this project is based on starter code provided by Udacity: [https://github.com/udacity/ud120-projects.git](https://github.com/udacity/ud120-projects.git)  
Only files that are necessary to the project submission are included here.  

## Project Goal

Use principal component analysis to reduce the dimensionality of the financial data and identify people of interest (poi) from the calculated PCA through supervised learning techniques.  

## Contents

### ./

* poi_id.py: Analysis for evaluation
* final_project_dataset.pkl:
* tester.py: Evaluator of the analysis - only here for transparency

### ./tools

Primarily Udacity provided scripts with helper functions for the provided data structures.

* feature_format.py: Tool for converting the provided dictionary of person : features to a processable format
  * featureFormat(dictionary, features, remove_NaN, remove_all_zeros, sort_keys)
    * return np.array(return_list)
    * return_list are only the requested feature from provided dictionary
  * targetFeatureSplit(data): make a feature a target
    * return target, features
    * target = data[item][0]
    * features = data[item][1:]
