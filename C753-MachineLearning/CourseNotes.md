# C753 - Introduction to Machine Learning 

## Project - Enron Emails

Build an algorithm to identify Enron employees that may have committed fraud.  

### Project Goals (From Project Overview)

* Deal with an imperfect, real-world dataset
* Validate a machine learning result using test data
* Evaluate a machine learning result using quantitative metrics
* Create, select and transform features
* Compare the performance of machine learning algorithms
* Tune machine learning algorithms for maximum performance
* Communicate your machine learning algorithm results clearly

### Resources

* Python 2.7 
  * Note: Scikit is dropping support for Python 2.7 and Python 3.4
* sklearn [https://scikit-learn.org/stable/](https://scikit-learn.org/stable/)
* Starter code: git clone [https://github.com/udacity/ud120-projects.git](https://github.com/udacity/ud120-projects.git)
* poi_id.py: POI Identifier. This is where the analysis goes.
* final_project_dataset.pkl: project dataset
* tester.py: code used by the evaluator to test results

### Structure of Provided Data

* Dictionary of people by name
* Each person has a dictionary of features
* The three features are financial \(dict\), email \(dict)and a POI \(boolean\)

| Financial Field (US Dollars)  | Description |
|-------------------------------|--------------
| salary                        |  |
| deferral_payments             |  |
| total_payments                |  |
| loan_advances                 |  |
| bonus                         |  |
| restricted_stock_deferred     |  |
| deferred_income               |  |
| total_stock_value             |  |
| expenses                      |  |
| exercised_stock_options       |  |
| other                         |  |
| long_term_incentive           |  |
| restricted_stock              |  |
| director_fees                 |  |

| Email Field             | Description |
|-------------------------|-------------|
| to_messages             |  |
| email_address           |  |
| from_poi_to_this_person |  |
| from_messages           |  |
| from_this_person_to_poi |  |
| shared_receipt_with_poi |  |

### Free-Response Questions

1. Summarize project goal [“data exploration”, “outlier investigation”]
   1. Provide dataset background
   1. Were there any outliers?
1. What features of the dataset did you use? [“create new features”, “intelligently select features”, “properly scale features”]
   1. How were they chosen? 
   1. Why/Why did you use scaling?
   1. What feature did you create and why?
1. What algorithm did you use in the end?
   1. How did that algorithm perform differently from the others? [“pick an algorithm”]
   1. Which algorithms did you try?
1. Describe algorithm parameter tuning [“discuss parameter tuning”, “tune the algorithm”]
   1. How did you do it?
   1. Why do you need to get it right?
   1. Which parameters did you tune?
1. What is Validation? [“discuss validation”, “validation strategy”]
   1. What is the classic mistake?
   1. How was your analysis validated?
1. Provide at least 2 evaluation metrics.  [“usage of evaluation metrics”]
   1. What were the average performance for each?
   1. Explain the interpretation in human-understandable terms.