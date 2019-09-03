# Udacity C753 Machine Learning Project

This project started with the starter code provided by Udacity for the introduction to machine learning portion of their data analytics nano degree: [https://github.com/udacity/ud120-projects.git](https://github.com/udacity/ud120-projects.git)  

## Contents

### ./

* Enron_Poi_Identifier.md: The long strange journey where scope keeps creeping
* README.md: the thing you are reading

### ./classifier_selection

Playgrounds for classifier selection

* clf_select.py

### ./datasets_questions

Initial investigations into the provided dataset  

* data_prep.py: streamlined data cleaning and preparation.
* explore_enron_data.py: initial dataset exploration.
* explore_feature_detail.py: second stage feature exploration in conjunction with data_prep.py
* explore_stock_data.py: feature selection based on manual data investigation and lasso_validation.py
* investigative_data_prep.py: Initial dataset cleaning, mostly partially investigative.

### ./feature_selection

Scripts used for feature selection  

* financial_adaboost_weighing.py: using adaboost to manually gauge feature relevance.
* lasso_validation.py: feature selection done smarter.

### ./pickle_jar

Pickled data sources, images and misc data files.  

* data_pairplot.png: unscaled final feature set pairplot
* dataset_final_clean.pkl: product of data_prep.py
* enron61702insiderpay.pdf: financial data source
* fin_data_pairplot.png: pairplot of manually selected feature set
* final_project_dataset_cleaned_no_loan.pkl: the other dataset for investigative cleaning
* final_project_dataset_cleaned.pkl: dataset for investigative cleaning
* final_project_dataset.pkl: original dataset
* poi_names.txt: manual data scrape from UsaToday identifying persons of interest.
* preped_data_pairplot.png: scaled final feature set pairplot
* stock_pairplot_cleaned.png: semi-cleaned version of stock data pairplot
* stock_pairplot_sans_redundant.png: semi-cleaned version of stock data pairplot without total_stock_value
* stock_pairplot.png: initial pairplot of stock data

### ./submission

Files required for project completion. If you're grading, these are the files for you.

* data_scrubber.py: consolidation of pertinent data exploration into one data set cleaner
* final_project_dataset.pkl: original provided dataset.
* my_classifier.pkl: straight up classifier
* my_dataset.pkl: scrubbed dataset. dict of dicts
* my_feature_list.pkl: list of features used by classifier
* poi_id.py: file that generates the three pkl files
* tester.py: udacity provided script to test the my*pkl files

### ./tools ./submission/tools

Udacity provided scripts with helper functions for the provided data structures.  

* feature_format.py: Tool for converting the provided dictionary of person : features to a processable format
  * featureFormat(dictionary, features, remove_NaN, remove_all_zeros, sort_keys)
    * return np.array(return_list)
    * return_list are only the requested feature from provided dictionary
  * targetFeatureSplit(data): make a feature a target
    * return target, features
    * target = data[item][0]
    * features = data[item][1:]
