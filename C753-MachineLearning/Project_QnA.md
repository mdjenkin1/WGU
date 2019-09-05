# Questions and Answers

## Summarize for us the goal of this project and how machine learning is useful in trying to accomplish it. As part of your answer, give some background on the dataset and how it can be used to answer the project question. Were there any outliers in the data when you got it, and how did you handle those?  [relevant rubric items: “data exploration”, “outlier investigation”]

The stated goal of this project is to create a person of interest classifier with a dataset scraped together from the Enron scandal. The actual goal of the project is to demonstrate an ability to apply statistical learning techniques to a toy dataset. The dataset has 3 primary sources of information. A manually scraped news article provides labels for our people of interest. A financial reporting spreadsheet provided the most populated data. Third, a partially parsed email dump.  

This mismatch of data sources resulted in an oddly shaped dataset. After removing the 5 problem entries, 141 entries remained. The removed entries are: "Total" and "The Travel Agency in the Park" for not being people; "Robert Belfer" and "Sanjay Bhatnagar" for values that are not sane; and "Eugene Lockhart" for no values.

To assist in data exploration, I added two booleans to each entry. One to state if email data existed for the entry and another if financial data existed. These booleans were used to identify the intersection of the email and financial data sources.

### Email Data Population

Number of people with an email address: 110  
Number of people with email stats: 85  
Number of people with financial data: 141  
Number of people with both data types: 85  
Number of poi with both email stats: 14  

All of the remaining entries have some type of financial data.  
Twenty-five entries have an email address and no email statistics.  
Just under two-thirds of our entries have email statistics. Of those that do have email statistics, all email statistics are populated.  
With 18 persons of interest identified in our dataset, it's worth noting that 4 do not have any email statistics.

### Financial Data Population

On the financial data side, all observations have some amount of the 14 financial features populated. However, the financial data is more sparsely populated than the email statistics. The loan_advances field is especially of note. There's only 3 entries with something for loan_advances.  

#### Financial Feature Percent Populated

loan_advances               0.02
director_fees               0.11
restricted_stock_deferred   0.12
deferral_payments           0.27
deferred_income             0.34
long_term_incentive         0.45
bonus                       0.57
other                       0.64
salary                      0.66
expenses                    0.66
exercised_stock_options     0.71
restricted_stock            0.76
total_payments              0.86
total_stock_value           0.87

## What features did you end up using in your POI identifier, and what selection process did you use to pick them? Did you have to do any scaling? Why or why not? As part of the assignment, you should attempt to engineer your own feature that does not come ready-made in the dataset -- explain what feature you tried to make, and the rationale behind it. (You do not necessarily have to use it in the final analysis, only engineer and test it.) In your feature selection step, if you used an algorithm like a decision tree, please also give the feature importances of the features that you use, and if you used an automated feature selection function like SelectKBest, please report the feature scores and reasons for your choice of parameter values.  [relevant rubric items: “create new features”, “intelligently select features”, “properly scale features”]

Feature selection started as a result of manual data investigation with extension into some statistical techniques. Based on my original dataset investigation, all email data was rejected as not all entries had email data. The remaining financial data was then further thinned by leveraging some unsupervised learning techniques to weight each feature. The most relevant features were selected from those results. The results of this feature selection have since been rejected.  

On this feature selection redo, a few features have been manually dropped. The only information gained from having email addresses is knowing who has emails but doesn't have email statistics. That raises more questions than it answers. The field will be dropped. The booleans added during investigation have been exhausted of their usefulness. Those too will be dropped. On the financial side, total_payments and total_stock_value are calculated fields. They corelate highly with other fields due to the redundancy they contain. No reason to weigh things twice. Finally, loan_advances will be dropped. With only three observations, two of which are persons of interest, the information this extremely sparse field could offer is warping or negligible. Based on earlier tests with boosted weak learners, it's mostly the later.  

To complete the feature selection process this go around, I took some advice and integrated SelectKBest into the pipelines I'll be feeding into GridSearchCV to select the algorithm. Included in each classifier pipeline is a StandardScalar. This will ensure the all features are scaled and classified according to the best parameters a brute can force.  

## What algorithm did you end up using? What other one(s) did you try? How did model performance differ between algorithms?  [relevant rubric item: “pick an algorithm”]

When it came to algorithm selection, I decided to compare K-Nearest Neighbors and Support Vector Classifiers. Both of these are known for their ability to classify smaller datasets under supervised learning. Deciding between them came to which gave the best precision. Some consideration was given to linear regression for classification. Given the plotted structure of the data and poor initial testing, this model was dropped.  

Between K-Nearest Neighbors and Support Vector Classifiers, the stock SVC configuration had slightly better accuracy. Some tuning was done for both algorithms before I focused on tuning the SVC classifier. That was all before I revisited how I was handling feature selection.  

After reintroducing the email data, precision of both SVC and KNN classifiers greatly improved. The KNN classifier improved so well that it is now performing better than SVC. The best precision for KNN reached 40% where as SVC only reached 35%.  

## What does it mean to tune the parameters of an algorithm, and what can happen if you don’t do this well?  How did you tune the parameters of your particular algorithm? What parameters did you tune? (Some algorithms do not have parameters that you need to tune -- if this is the case for the one you picked, identify and briefly explain how you would have done it for the model that was not your final choice or a different model that does utilize parameter tuning, e.g. a decision tree classifier).  [relevant rubric items: “discuss parameter tuning”, “tune the algorithm”]

Algorithm parameter tuning is a method of adjusting algorithm performance by manipulating constants within the algorithm. Performance adjustments can be made for algorithm speed or accuracy. In this case, performance in classifier precision was the target of the adjustments. Improper algorithm tuning can result in poor algorithm performance.  

I took a brute force approach to classifier tuning. GridsearchCV allowed me to setup multiple parameter sets for an algorithm. It then runs through the parameter sets and returns the best parameter set based on the specified metric. This allowed me to try many different parameters for the SVC algorithm. In the initial pass, where I compared SVC to K-NN, I limited my parameter tuning to kernel type and penalty parameter for SVC and number of neighbors and weight functions for K-NN.  

## What is validation, and what’s a classic mistake you can make if you do it wrong? How did you validate your analysis?  [relevant rubric items: “discuss validation”, “validation strategy”]

Validation is the process of ensuring any decision made doesn't improperly impact the algorithm. For instance, different training and testing splits in the dataset can have wildly different results in algorithm training. Another common issue for validation is balancing the bias, variance dilemma. Validation helps to ensure balance between overfitting and under fitting the data.  

My validation strategy included cross validation through 10-fold data partitioning. This provided a wide sampling of data splits to avoid overfit and underfit scenarios.  

## Give at least 2 evaluation metrics and your average performance for each of them.  Explain an interpretation of your metrics that says something human-understandable about your algorithm’s performance. [relevant rubric item: “usage of evaluation metrics”]

There were two evaluation metrics that I gave the most consideration. Accuracy was the first. Accuracy was problematic for the dataset in use because of the sparse nature of the persons of interest. Accuracy only states how many people were classified correctly. Classifying no one as a person of interest results in a 86% accuracy score.  

The poor measure offered by accuracy pointed me to precision as the metric to judge the classifier. Precision tells how accurate the classification is. A classifier might claim a group of 10 birds are all ducks. In actuality, that group of 10 bird might have 7 geese and only 3 ducks. This would mean a precision of 30%. There may be more birds than the 10 originally accused of being ducks. Precision only cares about the ones that were classified as ducks. Accuracy takes into account all the other birds not labeled as ducks.

Our interest is in who is classified as a poi. Are those classified as poi actually a person of interest? Precision best describes this interest.
