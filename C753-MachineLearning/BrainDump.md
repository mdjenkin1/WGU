# Machine Learning Final Project

## Brain Storming Session 1

What information is available to us?  
pulled in updated version of explore_enron_data.py  
Dataset contains 21 features across 146 people.
How many of those features are financial? 14
How many of those features are social (email)? 6
The final feature is a boolean for Person of Interest.
What are some natural relationships of those features?
Where are the dataset holes?

The majority/entirety of social data is email based. 35 people do not have email addresses listed in the dataset

```{Python}
In [90]: no_email = set()

In [91]: for x in enron_data:
    ...:     if enron_data[x]['email_address'] == 'NaN' : no_email.add(x)
    ...:

In [92]: no_email
Out[92]:
{'BADUM JAMES P',
 'BAXTER JOHN C',
 'BAZELIDES PHILIP J',
 'BELFER ROBERT',
 'BLAKE JR. NORMAN P',
 'CHAN RONNIE',
 'CLINE KENNETH W',
 'CUMBERLAND MICHAEL S',
 'DUNCAN JOHN H',
 'FUGH JOHN L',
 'GAHN ROBERT S',
 'GATHMANN WILLIAM D',
 'GILLIS JOHN',
 'GRAMM WENDY L',
 'GRAY RODNEY',
 'JAEDICKE ROBERT',
 'LEMAISTRE CHARLES',
 'LOCKHART EUGENE E',
 'LOWRY CHARLES P',
 'MENDELSOHN JOHN',
 'MEYER JEROME J',
 'NOLES JAMES L',
 'PEREIRA PAULO V. FERRAZ',
 'REYNOLDS LAWRENCE',
 'SAVAGE FRANK',
 'SULLIVAN-SHAKLOVITZ COLLEEN',
 'THE TRAVEL AGENCY IN THE PARK',
 'TOTAL',
 'URQUHART JOHN A',
 'WAKEHAM JOHN',
 'WALTERS GARETH W',
 'WHALEY DAVID A',
 'WINOKUR JR. HERBERT S',
 'WROBEL BRUCE',
 'YEAP SOON'}

In [93]: len(no_email)
Out[93]: 35

In [94]:
```

**Financial:** List, US dollars  
> salary  
> deferral_payments  
> total_payments  
> loan_advances  
> bonus  
> restricted_stock_deferred  
> deferred_income  
> total_stock_value  
> expenses  
> exercised_stock_options  
> other  
> long_term_incentive  
> restricted_stock  
> director_fees  

**Email:** List, Number of messages, text strings
> to_messages  
> email_address  
> from_poi_to_this_person  
> from_messages  
> from_this_person_to_poi  
> shared_receipt_with_poi  

## Feature review session

Review of Python scripts updated as part of the course.

### Unchanged

* class_vis.py (./choose_your_own)
* prep_terrain_data.py (./choose_your_own)
* your_algorithm.py (./choose_your_own)
* evaluate_poi_identifier.py (./evaluation)
* poi_email_addresses.py (./final_project)
* startup.py (./tools) environment setup and email dump retrieval

### Updated

* find_signature.py UPDATED: (./feature_selection) Decision Tree classifier.
* explore_enron_data.py UPDATED: (./datasets_questions) data count and investigation
* dt_author_id.py UPDATED: (./decision_tree) Email author identification
* poi_id.py UPDATED: (./final_project) Newer version in project
* tester.py UPDATED: (./final_project) Newer version in project
* nb_author_id.py UPDATED: (./naive_bayes) Naive Bays classifier
* enron_outliers.py UPDATED: (./outliers) Graphical investigation of outliers
* outlier_cleaner.py UPDATED: (./outliers)
* outlier_removal_regression.py UPDATED: (./outliers) Logical Regression to help find outliers
* eigenfaces.py UPDATED: (./pca)
* finance_regression.py UPDATED: (./regression) Linear regression for training
* svm_author_id.py UPDATED: (./svm)
* vectorize_text.py UPDATED: 
* email_preprocess.py UPDATED: (./tools)
* feature_format.py UPDATED: (./tools)
* parse_out_email_text.py UPDATED: (./tools)
* validate_poi.py UPDATED: (./validation)

### Lessons

| Section | Synopsis |
|--|--|
| Naive Bayes | Determine who said/wrote what |
| SVM | Identify email authors : svm_author_id.py </br>tools/email_preprocess.py contains logic for email tokenization |
| Decision Trees |  |
| Choose Your Own |  |
| Datasets and Questions |  |
| Regressions |  |
| Outliers |  |
| Clustering |  |
| Feature Scaling |  |
| Text Learning |  |
| Feature Selection |  |
| PCA |  |
| Validation |  |
| Evaluation |  |
