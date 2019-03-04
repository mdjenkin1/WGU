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
| salary                        | |
| deferral_payments             | |
| total_payments                | |
| loan_advances                 | |
| bonus                         | |
| restricted_stock_deferred     | |
| deferred_income               | |
| total_stock_value             | |
| expenses                      | |
| exercised_stock_options       | |
| other                         | |
| long_term_incentive           | |
| restricted_stock              | |
| director_fees                 | |

| Email Field             | Description |
|-------------------------|-------------|
| to_messages             | |
| email_address           | |
| from_poi_to_this_person | |
| from_messages           | |
| from_this_person_to_poi | |
| shared_receipt_with_poi | |

## Free-Response Questions