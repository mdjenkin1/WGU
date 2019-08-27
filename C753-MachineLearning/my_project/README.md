# Udacity C753 Machine Learning Project

The majority of this project is based on starter code provided by Udacity: [https://github.com/udacity/ud120-projects.git](https://github.com/udacity/ud120-projects.git)  
Only files that are necessary to the project submission are included here.  

## Project Goal

Use principal component analysis to reduce the dimensionality of the financial data and identify people of interest (poi) from the calculated PCA through supervised learning techniques.  

## Contents

### ./

* Enron_Poi_Identifier.md: The long strange journey where scope keeps creeping
* poi_id.py: Analysis for evaluation
* README.md: the thing you are reading
* tester.py: Evaluator of the analysis - only here for transparency

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

Pickled data sources and misc data files.  

* dataset_final_clean.pkl: product of data_prep.py
* data_pairplot.png: pairplot graph of final feature set
* enron61702insiderpay.pdf: financial data source
* final_project_dataset.pkl: original dataset
* final_project_dataset_cleaned.pkl: dataset for investigative cleaning
* final_project_dataset_cleaned_no_loan.pkl: the other dataset for investigative cleaning
* fin_data_pairplot.png: pairplot of manually selected feature set
* poi_names.txt: manual data scrape from UsaToday identifying persons of interest.
* stock_pairplot.png: initial pairplot of stock data
* stock_pairplot_cleaned.png: semi-cleaned version of stock data pairplot
* stock_pairplot_sans_redundant.png: semi-cleaned version of stock data pairplot without total_stock_value

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
