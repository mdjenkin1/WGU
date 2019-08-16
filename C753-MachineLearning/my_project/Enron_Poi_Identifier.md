# Person of Interest Identification Through Machine Learning

The dataset resulting from the bankruptcy of Enron presents an opportunity for supervised machine learning. We know who the persons of interest are in this dataset. Having labels for the feature sets allows us to gauge the accuracy of any classifier we train. By comparing the number of accurately identified feature sets between classifier configurations we can determine techniques for classifier creation. These techniques can then be adapted to scenarios where we are less lucky and do not have labels for our feature sets. That is the goal of this project, building some technique for accurate classifier training through supervised machine learning.  

## Initial Data Investigation

As with any investigation, we'll start with some high level understanding of the dataset we have and the features it contains.  

The data we're beginning with has been provided as the file final_project_dataset.py. It contains a serialized dictionary of dictionaries. The keys in the parent dictionary refer to a person. The child dictionary returned for each person contains the features of interest. A little bit of scripting with explore_enron_data.py will help us get a better handle on some of the detail of this dataset.

Also provided was a manual data scrape of a USA Today article providing names of people of interest. Comparing that list with the source article uncovers some questionable names. Christopher Loehr does not appear in the article. His absence from the article makes his inclusion questionable. A search shows he had some involvement but turned state's evidence, so his inclusion as a poi is warranted. There's also names in source article missing from the list. David Duncan and Arthur Andersen both destroyed evidence and had charges that were removed due to lack of criminal intent. There's argument for each of these names to be labeled as poi or not. With Loehr having involvement, he should be labeled as a poi despite his absence from the article. Andersen and Duncan's exclusion will also stand as it is not clear their roles in the fraud fit the definition of poi.

A little scripting gets us some deeper insight to the data.

```{python}
Count of entries in dataset: 146
Count of features in dataset: 21
Number of features not assigned to everyone: 0
Number of POI already labeled in dataset: 18
Number of POI identified in manual scrape: 35
Number of POI from all sources: 35
Number of POI not in dataset: 17
Number of POI in dataset and not labeled: 0
```

All 146 people in the dataset have a key for each of the 21 unique features in the dataset.
All identified people of interest in the dataset have been labeled as poi.
Not all identified poi are in the dataset.

On this initial pass of data investigation, some name cleaning was applied. Single characters (initials), periods and the specific title JR were removed. On a closer inspection, there's some names that don't make sense. Some additional cleaning may be in order.  

```{python}
***Entries With More Than Two Names***

PEREIRA PAULO FERRAZ
{'deferred_income': -101250,
 'director_fees': 101250,
 'expenses': 27942,
 'poi': False,
 'total_payments': 27942}

THE TRAVEL AGENCY IN THE PARK
{'other': 362096, 'poi': False, 'total_payments': 362096}
```

Both of these entries are very curious.

Paulo Ferraz Pereira raises the question of deferred income. Movement of funds from deferred compensation accounts to limited partnerships prior to the bankruptcy was one of the more scandalous behaviors. The practice resulted in a new law, Section 409A of the Internal Revenue Code. The provided pdf is the source of the financial data. It defines deferred_income as: "Reflects voluntary executive deferrals of salary, annual cash incentives, and long-term cash incentives as well as cash fees deferred by non-employee directors under a deferred compensation arrangement.  May also reflect deferrals under a stock option or phantom stock unit in lieu of cash arrangement." With this definition and the need for more regulation, deferred payments seem to have been common enough practice. Having more than 2 names doesn't disqualify the entry from inclusion.

Travel Agency in the Park is a different animal. Despite the court decision of Citizen's United, it is not a person. It even has it's own footnote on the financial dataset. "Payments were made by Enron employees on account of business-related travel to The Travel Agency in the Park (later Alliance Worldwide), which was coowned by the sister of Enron's former Chairman.  Payments made by the Debtor to reimburse employees for these expenses have not been included." Aside from having more than two names, it also only has 2 non-NaN features (the poi field is a label). Who else in the dataset can be described by this?  

```
***Entries With Two or Fewer Features***

WHALEY DAVID
{'exercised_stock_options': 98718, 'poi': False, 'total_stock_value': 98718}

WROBEL BRUCE
{'exercised_stock_options': 139130, 'poi': False, 'total_stock_value': 139130}

LOCKHART EUGENE
{'poi': False}

GRAMM WENDY
{'director_fees': 119292, 'poi': False, 'total_payments': 119292}

THE TRAVEL AGENCY IN THE PARK
{'other': 362096, 'poi': False, 'total_payments': 362096}
```

Of those with 2 or fewer features, only Eugene Lockhart stands out as an oddity. There doesn't appear to be an email dump associated with him. He doesn't appear in the financial spreadsheet. There's no apparent reason for him to exist in this dataset. Some research into who is Eugene Lockhart suggests he's the CEO of a failed energy startup in the energy supply market; "New Power Company". That seems more plausible than a former Dallas Cowboy linebacker. "The New Power Company" may have some involvement in the Enron scandal, but that data doesn't seem to be included in our dataset.  

Based on these findings, there's two entries that can be completely dropped from dataset. "The Travel Agency in the Park" by name and "Eugene Lockhart" by lacking features. For the remaining data points, their features could use a bit more scrutiny.  

## Deeper Data exploration

```{python}
***Types in use for features***
{'bonus': set(['int']),
 'deferral_payments': set(['int']),
 'deferred_income': set(['int']),
 'director_fees': set(['int']),
 'email_address': set(['str']),
 'exercised_stock_options': set(['int']),
 'expenses': set(['int']),
 'from_messages': set(['int']),
 'from_poi_to_this_person': set(['int']),
 'from_this_person_to_poi': set(['int']),
 'loan_advances': set(['int']),
 'long_term_incentive': set(['int']),
 'other': set(['int']),
 'poi': set(['bool']),
 'restricted_stock': set(['int']),
 'restricted_stock_deferred': set(['int']),
 'salary': set(['int']),
 'shared_receipt_with_poi': set(['int']),
 'to_messages': set(['int']),
 'total_payments': set(['int']),
 'total_stock_value': set(['int'])}
```

At the least, the dataset is consistent in its use of stored data. Aside from the poi boolean and email_address string, everything is numerical. There's also no mixing of numerical types. If it's not the poi label or email address, it is an integer.  

```{python}
***Number of entries with valued feature***
{'bonus': 82,
 'deferral_payments': 39,
 'deferred_income': 49,
 'director_fees': 17,
 'email_address': 111,
 'exercised_stock_options': 102,
 'expenses': 95,
 'from_messages': 86,
 'from_poi_to_this_person': 86,
 'from_this_person_to_poi': 86,
 'loan_advances': 4,
 'long_term_incentive': 66,
 'other': 93,
 'poi': 146,
 'restricted_stock': 110,
 'restricted_stock_deferred': 18,
 'salary': 95,
 'shared_receipt_with_poi': 86,
 'to_messages': 86,
 'total_payments': 125,
 'total_stock_value': 126}
```

The inclusion of loan_advances is questionable. With only 4 data points, there's a good chance this data would only skew results. Looking at the financial data source, Kenneth Lay utilized these loan advances to dump his stock holdings back on the company. It also explains why his total payment is astronomical compared to everyone else. The other entries with loan advances are Mark Frevert and Mark Pickering. Between the three of them, Frevert and Lay are known POI. The loan_advances feature just doesn't provide enough information. On its own, it is biased towards classifying a person as of interest and with this data set, it would do so at 66.7% accuracy. Also consider, there's 18 flagged poi in the dataset. At least 15 poi do not have a value for loan_advancement to flag them as a poi. The field "loan_advances" will be removed due to this extreme bias and total_payments field adjusted.  

What about the fourth entry with loan_advances?  

```{python}
***Entries with loan_advances***
set(['FREVERT MARK', 'LAY KENNETH', 'PICKERING MARK', 'TOTAL'])
```

Seems there's an additional entry that needs to be dropped. More than two names and 2 or less features would not catch someone with one name and all financial features. The "TOTAL" entry will also be added to the entries that need to be dropped.  

Finally, there's the question of feature classification. Of those we have two; financial data and email data.  

### Articles on 409A and Deferred Payments

[https://executivebenefitsolutions.com/lessons-learned-from-enron-and-chrysler-how-to-secure-nonqualified-deferred-compensation-plans/](https://executivebenefitsolutions.com/lessons-learned-from-enron-and-chrysler-how-to-secure-nonqualified-deferred-compensation-plans/)  
[https://www.institutionalinvestor.com/article/b150nnb56pj7fj/blame-it-on-enron](https://www.institutionalinvestor.com/article/b150nnb56pj7fj/blame-it-on-enron)  

### Who is Eugene Lockhart and the New Power Company

[https://money.cnn.com/2000/05/16/technology/enron/](https://money.cnn.com/2000/05/16/technology/enron/)  
[https://www.wsj.com/articles/SB1017015132933556040](https://www.wsj.com/articles/SB1017015132933556040)  

## Questions

1. Summarize for us the goal of this project and how machine learning is useful in trying to accomplish it. As part of your answer, give some background on the dataset and how it can be used to answer the project question. Were there any outliers in the data when you got it, and how did you handle those?  [relevant rubric items: “data exploration”, “outlier investigation”]

1. What features did you end up using in your POI identifier, and what selection process did you use to pick them? Did you have to do any scaling? Why or why not? As part of the assignment, you should attempt to engineer your own feature that does not come ready-made in the dataset -- explain what feature you tried to make, and the rationale behind it. (You do not necessarily have to use it in the final analysis, only engineer and test it.) In your feature selection step, if you used an algorithm like a decision tree, please also give the feature importances of the features that you use, and if you used an automated feature selection function like SelectKBest, please report the feature scores and reasons for your choice of parameter values.  [relevant rubric items: “create new features”, “intelligently select features”, “properly scale features”]

1. What algorithm did you end up using? What other one(s) did you try? How did model performance differ between algorithms?  [relevant rubric item: “pick an algorithm”]

1. What does it mean to tune the parameters of an algorithm, and what can happen if you don’t do this well?  How did you tune the parameters of your particular algorithm? What parameters did you tune? (Some algorithms do not have parameters that you need to tune -- if this is the case for the one you picked, identify and briefly explain how you would have done it for the model that was not your final choice or a different model that does utilize parameter tuning, e.g. a decision tree classifier).  [relevant rubric items: “discuss parameter tuning”, “tune the algorithm”]

1. What is validation, and what’s a classic mistake you can make if you do it wrong? How did you validate your analysis?  [relevant rubric items: “discuss validation”, “validation strategy”]

1. Give at least 2 evaluation metrics and your average performance for each of them.  Explain an interpretation of your metrics that says something human-understandable about your algorithm’s performance. [relevant rubric item: “usage of evaluation metrics”]