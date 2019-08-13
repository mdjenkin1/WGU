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

All 146 people in the dataset have entries for all 21 unique features in the dataset.
All identified people of interest in the dataset have been labeled as poi.
Not all identified poi are in the dataset.

On this initial pass of data investigation, some name cleaning was applied. Single characters (initials) and the specific title JR were removed. On a closer inspection, there's some names that don't make sense. Some additional cleaning is in order.  

## Questions

1. Summarize for us the goal of this project and how machine learning is useful in trying to accomplish it. As part of your answer, give some background on the dataset and how it can be used to answer the project question. Were there any outliers in the data when you got it, and how did you handle those?  [relevant rubric items: “data exploration”, “outlier investigation”]

1. What features did you end up using in your POI identifier, and what selection process did you use to pick them? Did you have to do any scaling? Why or why not? As part of the assignment, you should attempt to engineer your own feature that does not come ready-made in the dataset -- explain what feature you tried to make, and the rationale behind it. (You do not necessarily have to use it in the final analysis, only engineer and test it.) In your feature selection step, if you used an algorithm like a decision tree, please also give the feature importances of the features that you use, and if you used an automated feature selection function like SelectKBest, please report the feature scores and reasons for your choice of parameter values.  [relevant rubric items: “create new features”, “intelligently select features”, “properly scale features”]

1. What algorithm did you end up using? What other one(s) did you try? How did model performance differ between algorithms?  [relevant rubric item: “pick an algorithm”]

1. What does it mean to tune the parameters of an algorithm, and what can happen if you don’t do this well?  How did you tune the parameters of your particular algorithm? What parameters did you tune? (Some algorithms do not have parameters that you need to tune -- if this is the case for the one you picked, identify and briefly explain how you would have done it for the model that was not your final choice or a different model that does utilize parameter tuning, e.g. a decision tree classifier).  [relevant rubric items: “discuss parameter tuning”, “tune the algorithm”]

1. What is validation, and what’s a classic mistake you can make if you do it wrong? How did you validate your analysis?  [relevant rubric items: “discuss validation”, “validation strategy”]

1. Give at least 2 evaluation metrics and your average performance for each of them.  Explain an interpretation of your metrics that says something human-understandable about your algorithm’s performance. [relevant rubric item: “usage of evaluation metrics”]