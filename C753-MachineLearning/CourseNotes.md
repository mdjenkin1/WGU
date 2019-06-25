---
output:
    html_document:
        toc: true
        toc_float: true
---
# Intro to Machine Learning

Learning from examples  

## Environment

Python  
> sklearn (Scikit-Learn)  

### Python

* sklearn.naive_bayes
  * GaussianNB
    * fit(\<features\>, \<labels\>) : learns patterns
    * predict(\<features\>)

## Naive Bayes - 9 hrs

### Vocabulary

Supervised Classifications: known answers to examples  
Classifies unknown examples based on known examples.  
Examples and outcomes are defined.  

Unsupervised Classifications: unknown answers and/or unknown examples.  
Examples and/or outcomes are not defined.  

Features: Features are descriptors of examples that produce outcomes.  
Labels: categories of outcomes  

Decision Surface (DS): Line of delineation between categories.  
Linear DS: straight line  
Machine learning defines DS based on data  

Naive Bayes: Method of determining DS. Named for Philosopher that defined it as an attempt to prove/disprove god.  
[Bayes Theorem](https://en.wikipedia.org/wiki/Bayes%27_theorem)  

Overfitting: greater length of a decision boundary than is necessary.  

### Gaussian Naive Bayes in Python

[https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.GaussianNB.html#sklearn.naive_bayes.GaussianNB](https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.GaussianNB.html#sklearn.naive_bayes.GaussianNB)

```{python}
from sklearn.naive_bayes import GaussianNB      # Import module
clf = GaussianNB()                              # clf : classifier
clf.fit(X, Y)                                   # train clf to fit features X into Labels Y
pred = clf.predict(Z)                           # predict which Label the feature Z belongs too
```

### Evaluate our Classifier

Accuracy: The number of correctly identified points divided by the number of all points in test set  

Prevent or mitigate over fitting of data. Thinking you know better than you actually know.

save a portion of your data for testing and accuracy.

#### Accuracy Quiz

```{python}
### Data set is broken into 4 parts
# features_train    : Feature set for training the data
# labels_train      : Known good labels for training features
# features_test     : Features for testing the classifier
# labels_test       : Known good labels for calculating classifier accuracy

### create classifier
clf = GaussianNB()
### fit the classifier on the training features and labels
clf.fit(features_train, labels_train)
### use the trained classifier to predict labels for the test features
pred = clf.predict(features_test)
```

#### Manual accuracy calculation

```{python}
# Manual calculation
### Number of accurate calculations / number of test points.
# Number of accurate calculations <- labels_test[x] == pred[x]
# Number of test points <- len(labels_test)

# Initiate a variable counting how may predictions are accurate. Starting at zero.
num_acc = 0

# Compare each label
## This is an illustrative way of doing it
for ii in range(0, len(labels_test)):
    if (int(labels_test[int(ii)]) == int(pred[int(ii)])):
        #print("expected {} received {}".format(int(labels_test[int(ii)]), int(pred[int(ii)])))
        num_acc += 1

## This is the Python way of doing it
for t, p in zip(labels_test, pred):
    if t == p:
        num_acc += 1

## final results
acc_man = num_acc / len(labels_test)
```

#### Accuracy Calculation from python module

```{python}
### import metrics module for accuracy calculation
from sklearn.metrics import accuracy_score

### Module calculation
acc_mod = accuracy_score(labels_test, pred)
```

#### Performance

Calculate the time it takes for the code to complete.  

```{Python}
t0 = time()
### < your clf.fit() line of code >
print "training time:", round(time()-t0, 3), "s"
```

### Bayes Rule

Given a prior probability, determine the posterior probability in light of test evidence.  
aka. Probabilistic Inference - Given a set of values, what's the probability of a random event?  

Easy to implement.
Breaks in funny ways.

#### Cancer Example

Determine what percent of the population do and do not have cancer by their test results.  

##### Medical testing terminology  

_Sensitivity_ - Accurately tested positive  
_Specificity_ - Accurately tested negative  

##### Percent of population with Cancer. (Pretest)

> $P(C) = 1\% = 0.01$  
> $\therefore P(\neg C) = 99\% = 0.99$  \

##### Percent of population with accurate test results. (Test Results)

Sensitivity:  
> $P(Pos | C) = 90\% = 0.9$  
> $\therefore P(Pos |\neg C) = 10\% = 0.1$  

Specificity:  
> $P(\neg Pos | C) = 90\% = 0.9$  
> $\therefore P(Pos |\neg C) = 10\% = 0.1$  

##### ~~Posterior~~ Joint Probability

Determine the ratio of accurate to inaccurate results of those that tested positive.  

> True Positive: $P(C | Pos) = P(C) \times (Pos | C) = 0.01 \times 0.9 = 0.009$  
> False Positive: $P(\neg C | Pos) = P(\neg C) \times (Pos | \neg C) = 0.99 \times 0.1 = 0.099$  

##### Normalizer

Sum of joint probabilities.  

> $P(Pos) = P(C,Pos) + P(\neg C, Pos) = 0.009 + 0.099 = 0.108$  

##### Normalized Posterior

Use the normalizer to convert the joint probability from ratio to a percent.

> $P(C | Pos)$ $=$ $P(C | Pos) \over P(Pos)$ $=$ $0.009 \over 0.108$ $= 0.083\overline{3}$  
> $P(\neg C | Pos)$ $=$ $P(C | \neg Pos) \over P(Pos)$ $=$ $0.099 \over 0.108$ $= 0.916\overline{6}$

The sum of the normalized posteriors should equal 1.  

#### Text learning

Given the frequency of word use, determine the likelihood of who sent a message.  

##### Prior Probability

> $P(Chris) = 50\% = 0.5$  
> $P(Sara) = 50\% = 0.5$  

##### Evidence of Word Use

Chris  
> $P("Love") = 10\% = 0.1$  
> $P("Deal") = 80\% = 0.8$  
> $P("Life") = 10\% = 0.1$  

Sara  
> $P("Love") = 50\% = 0.5$  
> $P("Deal") = 20\% = 0.2$  
> $P("Life") = 30\% = 0.3$  

##### Joint Probability "Love Life"

> $P("Love\ Life" | Chris) \times P(Chris) = 0.1 \times 0.1 \times 0.5 = 0.005$  
> $P("Love\ Life" | Sara) \times P(Sara) = 0.5 \times 0.3 \times 0.5 = 0.075$  

##### Joint Probability "Life Deal"

> $P("Life\ Deal"| Chris) \times P(Chris) = 0.1 \times 0.8 \times 0.5 = 0.04$  
> $P("Life\ Deal" | Sara) \times P(Sara) = 0.3 \times 0.2 \times 0.5 = 0.03$  

##### Posterior Probability "Life Deal"

> Normalizer: $N = P("Life\ Deal"| Chris) + P("Life\ Deal" | Sara) = 0.04 + 0.03 = 0.07$  
> $P(Chris | "Life\ Deal") =$ $P("Life\ Deal"| Chris) \over N$ $=$ $0.04 \over 0.7$ = $0.5714 \approx 57\%$  
> $P(Sara | "Life\ Deal") =$ $P("Life\ Deal"| Sara) \over N$ $=$ $0.03 \over 0.7$ = $0.4285 \approx 43\%$  

##### Joint Probability "Love Deal"

> $P("Love\ Deal"| Chris) \times P(Chris) = 0.1 \times 0.8 \times 0.5 = 0.04$  
> $P("Love\ Deal" | Sara) \times P(Sara) = 0.5 \times 0.2 \times 0.5 = 0.05$  

##### Posterior Probability "Love Deal"

> Normalizer: $N = P("Love\ Deal"| Chris) + P("Love\ Deal" | Sara) = 0.04 + 0.05 = 0.09$  
> $P(Chris | "Love\ Deal") =$ $P("Love\ Deal"| Chris) \over N$ $=$ $0.04 \over 0.9$ = $0.4\overline{4} \approx 44\%$  
> $P(Chris | "Love\ Deal") =$ $P("Love\ Deal"| Chris) \over N$ $=$ $0.05 \over 0.9$ = $0.5\overline{5} \approx 56\%$  

## Support Vector Machines (SVM) - 6 hrs

Finds the hyper-plane (linear) between data of different class.  
Maximizes the distance to nearest point (margin) between both classes.  
Maximized margins is referred to as robustness.  

Correct classification occurs before determining the margin.  
Outliers are data points of a class that exist outside of the class's grouping.  
Toleration of outliers occurs with best fit hyper-planes.  

Works well for complicated domains where there's a clear margin of separation.  
Time intensive to train with large datasets.  
Looses effectivness with noisy datasets.

[https://scikit-learn.org/stable/modules/svm.html](https://scikit-learn.org/stable/modules/svm.html)  
> Memory Efficient.  
> Effective in high dimensional spaces.  
> Indirect probability estimates through expensive five-fold cross-validation.  

```{python}
from sklearn import svm
clf = svm.SVC(<parameters>)
clf = svm.fit(x,y)              # X is set of features, y are labels
pred = svm.pred(z)              # Z is set of prediction features
```

### Nonlinear SVMs

Linearly Separable: Classification of labels can be separated by one line.  

By adding features it is possible to transform linearly inseparable datasets into linearly separable datasets.  

Feature transformation  
_e.g._:  
> Linear separation of radial decision plane
$$Z(X,Y) => X^2 + Y^2$$  

> Linear separation by pivoting values on axis.
$$Z(X,Y) => (|X|,Y)$$

### Kernel Trick

Functions that transform low dimensional inseparable feature space to a higher dimensional separable feature space. The linear solution of the higher dimensional separable feature space can be returned lower dimensional feature space as a non-linear separation.  

This course focuses on the Support Vector Classifier (SVC) kernel.  

[https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html#sklearn.svm.SVC](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html#sklearn.svm.SVC)  

### Parameters

Passed during classifier creation  
> kernel: (string) linear, poly, rbf, sigmoid  
> C: (float) controls tradeoff between smooth decision boundary and accurate training. larger values of C are biased towards accuracy due to smaller margin selection.  
> gamma: (float) default is auto ($1\over n_{features}$). Impact of a single feature's influence on training. Higher gamma means points closer to the hyperplane will have greater impact on the hyperplane.  

All can be used to manage overfitting.  

## Decision Trees - 6 hrs

Splitting data on numerical or categorical definitions.  
Non-linear decision making with a linear decision surface.  
Multiple linear decision surfaces.  

Root Node > Internal Nodes > Leaf Nodes  

_Is it this or that?_  
_If it's this then is this one or this other?_  
_If it's one is it divisible or indivisible?_  
_..._  

Algorithm to determine boundaries.  
Prone to overfitting. Stop the growth at the appropriate time.  
Can build classifiers out of decision trees (ensemble methods - see Choose Your Own Algorithm).  

```{python}
from sklearn import tree
clf = tree.DecisionTreeClassifier()
clf = clf.fit(features_train, labels_train)
```

Overfitting: long legs within the decision boundary. greater surface/length of the decision boundary.

### Tuning options of DecisionTreeClassifier

[https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html#sklearn.tree.DecisionTreeClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html#sklearn.tree.DecisionTreeClassifier)  

> **min_samples_split** (default 2): minimum size of leaf. Smaller numbers are more prone to overfitting. Overfitting can produce poorer accuracy.  
> **criterion** (default "gini"): Gini impurity or entropy for information gain.  

### Impurity

_Impurity measurements are used to decide where to split data._  

Purity is defined as a measure of homogeneity.  
A decision surface that produces a 100% accurate split of features to labels is not impure.  

#### Gini Impurity

Calculation for the Gini impurity of each leaf.  

[https://www.youtube.com/watch?v=7VeUPuFGJHk](https://www.youtube.com/watch?v=7VeUPuFGJHk)

$$G_{leaf} = 1 - P(X)^2 - P(\neg X)^2$$
$$P(X) = {X \over {X+\neg X}}$$
$$P(\neg X) = {\neg X \over {X+\neg X}}$$

The population in each leaf may differ. Therefore, the Gini impurity score of each leaf will need to be weighted according to it's portion of the population.  

$$G_{weighted_a} = \bigg({P_{leaf_a} \over {P_{leaf_a} + P_{leaf_b}}}\bigg) \times G_{leaf_a}$$

The total Gini impurity of a node is the sum of its leaves weighted Gini Impurities.  

$$ G_{node} = \sum {G_{leaves_{weighted}}} $$

Lowest Gini impurity between all potential nodes wins.  
If a node has a lower Gini impurity than its possible leaves, it becomes a leaf.  

Decision for where to split numerical data is determined by comparing Gini impurity if data is split between adjacent values in ordered list.  

Ranked and selection data is split by determining the impurity score on all possible subsets where the subset is not the entirety of the set.  

$$A_n \subsetneq B$$

#### Entropy

$$Entropy = {\sum_i} -\smash{p_i} log_2(p_i)$$  

$p_i$: fraction of examples in class i

$Entropy = 0$ when all examples are of the same class (minimal value)  
$Entropy = 1.0$ when all examples are evenly split between classes (maximum value)  

e.g.  
> Consider a node with four examples.  
> Two examples are class 'slow'.  
> Two examples are class 'fast'.  
> $p_{slow} = {slow\_examples \over tot\_examples} = {2 \over 4} = 0.5$  
> $p_{fast} = {fast\_examples \over tot\_examples} = {2 \over 4} = 0.5$
> $Entropy = {\sum_i} -\smash{p_i} log_2(p_i) = (-\smash{p_{slow}} \times log_2 p_{slow}) + (-\smash{p_{slow}} \times log_2 p_{fast})$  

```{python}
import math
-0.5*math.log(0.5, 2) -0.5*math.log(0.5, 2)
```

### Information Gain

The difference between the entropy of the parent minus the weighted average of the entropy of the children.  
Used by decision trees make decisions to maximize information gain.  

$$Information_Gain = Entropy_{parent}-Entropy_{children_{weighted}}$$

#### Example

| grade | bumpiness | Spd Limit | speed |
|-------|-----------|-----------|-------|
| steep | bumpy     | yes       | slow  |
| steep | smooth    | yes       | slow  |
| flat  | bumpy     | no        | fast  |
| steep | smooth    | no        | fast  |

Entropy of parent = 1.0  
o : fast  
x : slow  

#### Information Gain of speed decided by grade

|           | steep | flat |
|-----------|-------|------|
| parent    | oox   | x    |
| 1st child | oo    | x    |
| 2nd child | o     |      |

|           | $p_{slow}$ | $p_{fast}$ | entropy |
|-----------|------------|------------|---------|
| 1st child | 0.667      | 0.333      | 0.918   |
| 2st child | 0.0        | 1.0        | 0.0     |  

Weighted average of children: ${3\over4}\times0.9183 + {1\over4}\times0 = 0.6887$  
Information gain: $E_{parent}-E_{children} = 1.0 - 0.6887 = 0.3113$  

#### Information Gain of speed decided by bumpiness

|           | bumpy | smooth |
|-----------|-------|--------|
| parent    | xo    | xo     |
| 1st child | xo    | xo     |
| 2nd child | xo    | xo     |

|           | $p_{slow}$ | $p_{fast}$ | entropy |
|-----------|------------|------------|---------|
| 1st child | 0.5        | 0.5        | 1.0     |
| 2st child | 0.5        | 0.5        | 1.0     |

Weighted average of children: ${2\over4}\times1.0 + {2\over4}\times1.0 = 1.0$  
Information gain: $E_{parent}-E_{children} = 1.0 - 1.0 = 0.0$  

#### Information Gain of speed decided by speed limit

|           | yes | no |
|-----------|-----|----|
| parent    | xx  | oo |
| 1st child | xx  |    |
| 2nd child |     | oo |

|           | $p_{slow}$ | $p_{fast}$ | entropy |
|-----------|------------|------------|---------|
| 1st child | 1.0        | 0.0        | 0.0     |
| 2st child | 0.0        | 1.0        | 0.0     |

Weighted average of children: ${2\over4}\times0.0 + {2\over4}\times0.0 = 0.0$  
Information gain: $E_{parent}-E_{children} = 1.0 - 0.0 = 1.0$  

### Bias-Variance Dilemma

Bias-Variance tradeoff is the balancing of two sources of algorithm error.

* Bias is the underfitting of data due to erroneous assumptions. When relevant relations between features are missed, bias increases. The data is seen as more homogeneous than it is. At the extreme, all features are of the same label.
* Variance is the overfitting of data due to high data sensitivity. The algorithm is more sensitive to random noise. At the extreme, all features are of different labels.

Finding the best balance between variance and bias is part of the art of machine learning.  

## Choose Your Own Algorithm - 1 hr

[https://tex.stackexchange.com/questions/319284/mind-map-type-that-i-didnt-find-out](https://tex.stackexchange.com/questions/319284/mind-map-type-that-i-didnt-find-out)  
[https://i.stack.imgur.com/RlHJB.png](https://i.stack.imgur.com/RlHJB.png)  
![.\RlHJB.png](.\RlHJB.png)  

### Choices

* k nearest neighbors
* random forest
* adaboost (boosted decision tree)

The choices provided here are types of ensemble algorithms. Ensemble algorithms are meta classifiers commonly built from decision trees. They combine weak learners (e.g. high bias, low-variance) to produce strong models.  

#### K Nearest Neighbors k-NN

[https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm)  
[https://scikit-learn.org/stable/modules/neighbors.html](https://scikit-learn.org/stable/modules/neighbors.html)  

* k-NN Classification: Features are labeled according to commonality with nearest neighbors.  
* k-NN Regression: average value of k nearest neighbors as property value.  

K: number of nearest neighbors to query. No hard or soft rules for determining accurate values of K.  
Each neighbor's vote counts for claiming the membership of the device.  
Neighbors are initially determined by training data.  
Value of neighbors are commonly weighted by distance ($1\over{d}$)  

[https://scikit-learn.org/stable/modules/classes.html#module-sklearn.neighbors](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.neighbors)  

```{Python}
from sklearn.neighbors import NearestNeighbors
import numpy as np
X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(X)
distances, indices = nbrs.kneighbors(X)
```

[https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html)  

```{Python}
X = [[0], [1], [2], [3]]
y = [0, 0, 1, 1]
>>> from sklearn.neighbors import KNeighborsClassifier
>>> neigh = KNeighborsClassifier(n_neighbors=3)
>>> neigh.fit(X, y)
>>> print(neigh.predict([[1.1]]))
[0]
>>> print(neigh.predict_proba([[0.9]]))
[[0.66666667 0.33333333]]
```

[https://scikit-learn.org/stable/auto_examples/neighbors/plot_classification.html#sphx-glr-auto-examples-neighbors-plot-classification-py](https://scikit-learn.org/stable/auto_examples/neighbors/plot_classification.html#sphx-glr-auto-examples-neighbors-plot-classification-py)  

```{Python}
print(__doc__)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets

n_neighbors = 15

# import some data to play with
iris = datasets.load_iris()

# we only take the first two features. We could avoid this ugly
# slicing by using a two-dim dataset
X = iris.data[:, :2]
y = iris.target

h = .02  # step size in the mesh

# Create color maps
cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

for weights in ['uniform', 'distance']:
    # we create an instance of Neighbours Classifier and fit the data.
    clf = neighbors.KNeighborsClassifier(n_neighbors, weights=weights)
    clf.fit(X, y)

    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, x_max]x[y_min, y_max].
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure()
    plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

    # Plot also the training points
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold,
                edgecolor='k', s=20)
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.title("3-Class classification (k = %i, weights = '%s')"
              % (n_neighbors, weights))

plt.show()
```

#### Random Forest

Build multiple decision trees and let them vote on how to classify inputs.  
From one dataset, build multiple trees by bootstrapping data.  
Non-sampled data can be used as test data for each tree.  

[https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)  

```{Python}
from sklearn.ensemble import RandomForestClassifier
```

[https://scikit-learn.org/stable/modules/ensemble.html#forests-of-randomized-trees](https://scikit-learn.org/stable/modules/ensemble.html#forests-of-randomized-trees)  

```{Python}
from sklearn.ensemble import RandomForestClassifier
X = [[0, 0], [1, 1]]
Y = [0, 1]
clf = RandomForestClassifier(n_estimators=10)
clf = clf.fit(X, Y)
```

[https://www.youtube.com/watch?v=J4Wdy0Wc_xQ](https://www.youtube.com/watch?v=J4Wdy0Wc_xQ)  

Decision Trees are inaccurate due to inflexibility. Random Forests addresses this issue.  

The best possible tree from a full dataset is a decision tree. Accurate only for that dataset.  
Instead...  
Take a random (duplicates allowed) sample of the dataset (bootstrapped).  
Determine nodes on a random selection of features.  
Produce a wide variety of trees from the same dataset.  

New feature sets can tested against all of these trees. The tally of the results from the trees determine the label of new feature sets.  

Bagging: Bootstrapping data and using the aggregate to make a decision.  
Out-Of-Bag Dataset: the dataset not used in the bootstrapped data set. Useful as a testing dataset.

Accuracy is determined by the proportion of correctly classified Out-Of-Bag samples. Incorrectly classified samples "Out-Of-Bag Error". Adjustments to random forest accuracy can be modified using alternate selection values used to build the random tree. Common starting point is starting by selection a number of variables equal to the square root of the number of variables.  

##### Missing Data

Data missing from the original Dataset  
Data missing from a new sample  

Fill in missing data by making a best guess and testing.  

Proximity matrix: column to row for each entry.  
Score a point for each column/row that lands in the same leaf node.  
Divide point total by total number of trees (proximity).  
Adjust the guess by weighing according to proximity.  

$P_{value}$ : sum of proximity for specific value
$P_{total}$ : sum of all proximities  
$P_{weight}$ : Weighted Proximity of value  

$$P_{weight} = {P_{value} \over P_{total}}$$

Categorical guess adjustments  

$X_{total}$  : Total number of occurrences  
$X_{value}$  : Occurrence of specific value  

$${X_{value} \over X_{total}}\times P_{weight}$$

Numerical guess adjustment (weighted average)

$$\sum{X_{value_n} \times P_{weight_n}}$$  

Repeat entire process until missing values converge.  

As an aside, Distance: $D_{value} = 1-P_{value}$  
Distance can be used to create a heat map.  

For missing data in samples needing classification, assume all possible values and iterate for each.

#### Adaboost (Adaptive Boosting)

Definitive Text: [https://towardsdatascience.com/boosting-algorithm-adaboost-b6737a9ee60c](https://towardsdatascience.com/boosting-algorithm-adaboost-b6737a9ee60c)  
Maths: [https://brage.bibsys.no/xmlui/handle/11250/2433761](https://brage.bibsys.no/xmlui/handle/11250/2433761)  
Video: [https://www.youtube.com/watch?v=LsK-xG1cLYA](https://www.youtube.com/watch?v=LsK-xG1cLYA)

_Stump:_ A tree of one node and two leaves. Not great at making decisions. Weak Learners.

Adaboost is an ensemble algorithm. The weak learners it uses is almost always stumps. This provides similarities to random forests.  

Adaboost uses stumps. Random Forests use full trees.
Adaboost weighs the value of each stump. Random Forests considers each tree equal.  
Adaboost considers the mistakes of previous trees when making new stumps. Random forests make each tree independent of other trees.  

##### Adaboost Algorithm

Assign an equal sample weight for each observation: $1 \over N_{samples}$  
Determine which variable best classifies the observations (Gini Index or Entropy).  
Create the First Stump.  
Adjust sample weight according to errors in the first stump.  

##### Finding Stump Weight from Error

Total Stump Error  : $T_{err}$  
Total Stump Weight : $T_{wgt}$  
Weight of "Incorrect Sample" : $S_{err}$  

Sum the weight of samples that predicted incorrectly  
$$T_{err} = \sum {S_{err}}$$  

Calculate Stump Weight (Strength of Stump's Final Vote)  
$$T_{wgt} = {1 \over 2} \times \log \bigg( {1 - T_{err} \over T_{err}} \bigg)$$  

Negative weight is a bad predictor  
Zero weight is 50/50  
Positive weight is a good predictor  

##### Adjust Weight of Samples

Increase the weight of incorrectly classified samples.  
Decrease the weight of correctly classified samples.  

Old Sample Weight : $S_{wgt}$  
New Sample Weight : $S_{new}$  
Normalized Sample Weight : $S_{adj}$  
Total Stump Weight : $T_{wgt}$  

Adjusted weight of incorrect samples
$$S_{new} = S_{wgt} \times e^{T_{wgt}}$$  

Adjusted weight of correct samples  
$$S_{new} = S_{wgt} \times e^{-T_{wgt}}$$  

Normalize sample weights  
$$S_{adj} = {S_{new} \over {\sum S_{new}}}$$

By increasing the incorrectly classified sample weights and decreasing the correctly classified sample weights, the next stump will put more emphasis on correctly classifying the incorrectly classified samples.  

##### Weighted Bootstrap

Weighted data bootstrap as an alternate to weighted Gini Indexing.  

* Length of bootstrap should be equal to length of original dataset.
* Assign each sample a value equal to the sum of weights of preceding samples and its own weight.
* Generate a random number between 0 and 1 for each sample in the bootstrapped set.
* For each random number, select the sample from the original data set where the random number is greater than the assigned number of the preceding sample and less than or equal to the sample's assigned number.

Sample's assigned number : $S_{n}$  
Adjusted weight of Sample : $S_{adj}$  
Random Number : $X$  

Assign a number to each sample n
$$S_{n} = \sum_0^n S_{adj}$$

Generate Random number  
$$X \in [0, 1]$$

Select sample (with replacement)  
$$S_{n-1} < X \le S_{n}$$

The weights of the samples in the bootstrapped set are now equal.  
The original sample set may be discarded.  

##### Final Model Use

Classify the new observation according to the sum of weighted values for each stump that voted for a specific classification. The classification with the highest number wins.

$$Votes_{true} = \sum T_{wgt_{true}}$$
$$Votes_{false} = \sum T_{wgt_{false}}$$

##### Doing it in Python

[https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html)  
[https://scikit-learn.org/stable/auto_examples/ensemble/plot_adaboost_twoclass.html#sphx-glr-auto-examples-ensemble-plot-adaboost-twoclass-py](https://scikit-learn.org/stable/auto_examples/ensemble/plot_adaboost_twoclass.html#sphx-glr-auto-examples-ensemble-plot-adaboost-twoclass-py)

```{Python}
print(__doc__)

# Author: Noel Dawe <noel.dawe@gmail.com>
#
# License: BSD 3 clause

import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_gaussian_quantiles


# Construct dataset
X1, y1 = make_gaussian_quantiles(cov=2.,
                                 n_samples=200, n_features=2,
                                 n_classes=2, random_state=1)
X2, y2 = make_gaussian_quantiles(mean=(3, 3), cov=1.5,
                                 n_samples=300, n_features=2,
                                 n_classes=2, random_state=1)
X = np.concatenate((X1, X2))
y = np.concatenate((y1, - y2 + 1))

# Create and fit an AdaBoosted decision tree
bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1),
                         algorithm="SAMME",
                         n_estimators=200)

bdt.fit(X, y)

plot_colors = "br"
plot_step = 0.02
class_names = "AB"

plt.figure(figsize=(10, 5))

# Plot the decision boundaries
plt.subplot(121)
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, plot_step),
                     np.arange(y_min, y_max, plot_step))

Z = bdt.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)
cs = plt.contourf(xx, yy, Z, cmap=plt.cm.Paired)
plt.axis("tight")

# Plot the training points
for i, n, c in zip(range(2), class_names, plot_colors):
    idx = np.where(y == i)
    plt.scatter(X[idx, 0], X[idx, 1],
                c=c, cmap=plt.cm.Paired,
                s=20, edgecolor='k',
                label="Class %s" % n)
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.legend(loc='upper right')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Decision Boundary')

# Plot the two-class decision scores
twoclass_output = bdt.decision_function(X)
plot_range = (twoclass_output.min(), twoclass_output.max())
plt.subplot(122)
for i, n, c in zip(range(2), class_names, plot_colors):
    plt.hist(twoclass_output[y == i],
             bins=10,
             range=plot_range,
             facecolor=c,
             label='Class %s' % n,
             alpha=.5,
             edgecolor='k')
x1, x2, y1, y2 = plt.axis()
plt.axis((x1, x2, y1, y2 * 1.2))
plt.legend(loc='upper right')
plt.ylabel('Samples')
plt.xlabel('Score')
plt.title('Decision Scores')

plt.tight_layout()
plt.subplots_adjust(wspace=0.35)
plt.show()
```

## Datasets and Questions

An exercise in exploring the Enron Email Dataset

### Enron Dataset

Identifying People of Interest from the Enron email dataset.

[https://www.cs.cmu.edu/~enron/](https://www.cs.cmu.edu/~enron/)  
[https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz](https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz)  

Structured as directories per person.  
_LastName-FirstNameInitial_  

### Exploration Methodologies

**Regressions:** Relationship between variables.  
**Clustering:** Type of unsupervised learning. Performs grouping  
**Outliers:** Dataset error detection and removal.  

### Defining a Person Of Interest (POI)

Determine the criteria for the label. Initial considerations follow.  

1. Indicted
1. Settled without admitting guilt
1. Testified in exchange for immunity

### Training Set Considerations

As training set size increases, accuracy approaches the maximal limit of the training set.  
Mixing similar data from different sources can introduce training bias. When mixing data sources, be sure to mitigate any introduced bias.  

## Regressions

### Data Types

| Type        | Example                       |
|-------------|-------------------------------|
| Numerical   | Salary, Review Score          |
| Categorical | Discrete Values, Movie Genres |
| Time Series | Date, Timestamp               |
| Text        | Words                         |

### Continuous Learning vs Discrete Supervised Learning

**Continuous:** Output as a function of Input (e.g. continuous output)  
**Discrete:** values are categorical (individual and distinct)  

e.g.  
> Age as a funtion of time passed since birth is continuous.  
> Weather as a state of cloudy or sunny is discrete.  


| Property    | Supervised Classification | Regression              |
|-------------|---------------------------|-------------------------|
| Output Type | Discrete                  | Continuous              |
| What        | Decision Boundary         | Best Fit                |
| Evaluation  | Accuracy                  | $\sum \beta^2$ or $r^2$ |

### Basic Linear Formula

$$f(x) = m\times x + b$$  
$m$ - Slope (rise over run i.e. $y \over x$)  
$b$ - Intercept (where the line crosses y-axis i.e. $f(0)$)  

### General Linear Models

Linear Regression: minimize sum of squared errors between observations and linear prediction.  

**Ordinary Least Squares (OLS):** sklearn LinearRegression  
**Gradient Decent:** out of scope for course.  

[https://scikit-learn.org/stable/modules/linear_model.html](https://scikit-learn.org/stable/modules/linear_model.html)

$$\hat{y}(\omega,x) = \omega + \omega_1x_1 + \omega_2x_2 +...+\omega_nx_n$$  


$\hat{}$ : decoration denoting estimated value. e.g. $\hat{y}$  
$\omega = (\omega_1...\omega_n)$: coef_  
$\omega_0$: intercept_  

$$\underset{\omega}{min}\|X\omega-y\|_2^2$$

$\|x\|$: vector of magnitude $x$  
$\|x\|_2$: Euclidean norm of vector $x$  
$\|x\|^2_2$: Square of the Euclidean norm (i.e $p$-$norm = 2$) of vector $x$ e.g. $\|x\|^2_2 = \sqrt{x^2_1 + x^2_2 +...+ x^2_n}$

```{Python}
from sklearn import linear_model                # module import
reg = linear_model.LinearRegression()           # Classifier instantiation
reg.fit([[0, 0], [1, 1], [2, 2]], [0, 1, 2])    # Array [X, y]
reg.coef_                                       # Slope
reg.predict([])                                 # Prediction of value
reg.intercept_                                  # Intercept of regression
reg.score(X, y)                                 # r-squared score (performance metric)
```

Visualization  

```{Python}
plt.scatter(X, y)
plt.plot(X, reg.predict(X))
plt.show()
```

### Quantifying and Minimizing Errors

Error ($\beta$): difference between actual value ($y$) and predicted value ($\hat{y}$).  

**Error:** $\beta = y - \hat{y}$  
**Sum of error absolutes:** $\sum|\beta_x|$: problem of fundamental ambiguity  
**Sum of errors squared:** $\sum|\beta_x^2|$: as data samples increases, sum of squares also increases  
**Coefficient of Determination:** $0.0 < r^2 < 1.0$ Measure of how much change in output is explained by change in input. Larger is better.  

### Multivariate Regression

Multiple input variables to determine predictive regression.  
_Linear Hyperplanes_  

$$\hat{y} = \beta_0 + \sum_{i=1}^{p}{\beta_i \times X_i}$$

$\beta_i$ - coefficient of $x_i$
$\beta_0$ - initial value $x_i$

## Outliers

Data points far removed from the rest of the dataset, they warp the results of data interpretation.  
Common causes: Sensor malfunctions, Data entry errors, Freak events. Freak events should not be ignored.  

### Detection and Rejection

1. Train
1. Remove points with highest residual errors (~ 10%)
1. Train

Investigate any data points suspected as outliers before rejecting.  

## Clustering - 3hr 5/13

Classification of similar data point subsets into groups.  
A form of unsupervised learning (Dimensionality Reduction is another)  

[https://scikit-learn.org/stable/modules/clustering.html](https://scikit-learn.org/stable/modules/clustering.html)

### K-Means Clustering

**Hill climbing algorithm:** resulting fit depends on initial cluster center positioning.  
**Local Minimum:** single cluster is split between multiple centers.  

1. Assign group center(s) at random
1. Optimize: minimize the total quadratic lengths from centers to grouped data points

Visualizing K-Means Clustering: [http://www.naftaliharris.com/blog/visualizing-k-means-clustering/](http://www.naftaliharris.com/blog/visualizing-k-means-clustering/)  

[https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans)  

```{Python}
from sklearn.cluster import KMeans                              # Import Package
import numpy as np                                              # Build Data (Numpy Array)
X = np.array([[1, 2], [1, 4], [1, 0],                           # Build Data (Numpy Array)
              [10, 2], [10, 4], [10, 0]])                       # Build Data (Numpy Array)
kmeans = KMeans(n_clusters=2, random_state=0).fit(X)            # Fit Data 
kmeans.labels_                                                  # List of labels per point in data, label datatype
kmeans.predict([[0, 0], [12, 3]])                               # Predict data classification
kmeans.cluster_centers_                                         # Coordinates of cluster centers
```

**Question for exploration:** What would happen if the algorithm is seeded with an excessive number of cluster centers which are fitted and then become the new dataset?  

## Feature Scaling

Type of preprocessing to assign values to nulls based on known values of other observations.  
Normalize the scale of features to better compare the weight of unlike values in determining object classification.  
Algorithms that work on two or more dimensions are affected by feature rescaling.  

* SVM decision boundaries are decided by distances that can change when scaled.
* Cluster warping will change outcome of K-Means clustering.
* Decision trees make binary decisions when branching. Binary decisions are immune to scaling
* Linear Regression depends on coefficient values on a per feature basis. Scaling does not affect feature coefficients.

$$X\prime = {{X - X_{min}}\over{X_{max} - X_{min}}}$$

$X\prime$ : Scale of new feature to be scaled  
$X_{min}$ : Min of old, unscaled feature  
$X_{max}$ : Max of old, unscaled feature  
$X$ : Original value of feature to be scaled  

Manual Min/Max

```{python}
def featureScaling(arr):
    low = min(arr)
    high = max(arr)

    if low == high:
        return arr
    else:
        primes = list(map(lambda x: float(x-low)/float(high-low), arr))
        return primes

# tests of your feature scaler--line below is input data
data = [115, 140, 175]
print("{}".format(featureScaling(data)))
# [0.0, 0.4166666666666667, 1.0]
```

Min/Max Scaler in sklearn  
[https://scikit-learn.org/stable/modules/preprocessing.html](https://scikit-learn.org/stable/modules/preprocessing.html)  

```{python}
from sklearn.preprocessing import MinMaxScaler
import numpy
weights = numpy.array([[115.],[140.],[175.]])
scaler = MinMaxScaler()
rescaled_weight = scaler.fit_transform(weights)
rescaled_weight
# array([[0.        ],
#        [0.41666667],
#        [1.        ]])
```

## Text Learning

### Bag of Words

**Problem:** No standards for measuring word use or word value in text phrases.  
**Solution:** Dictionary containing frequency count of word use.  

Word order doesn't matter  
Phrase length impacts input vectors.  
Cannot accommodate complex phrases (unless additional buckets created)  

### CountVectorizer

[https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html)  

```{python}
######
# Create Vectorizer
######
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()

######
# Toy Data
######
email0 = "blah blah boo"
email1 = "foo baz bar"
email2 = "boo bar blah foo"
email_list = [email0, email1, email2]

######
# Bag It
######
bag_of_words = vectorizer.fit(email_list)
bag_of_words = vectorizer.transform(email_list)

# bag_of_words returns tuples and integers
# the tuple contains indexes (document, word)
# the integer is count
# e.g.
# boo: (0, 3) 1
# boo: (2, 0) 1

```

### Word Information

**Low Information Words:** offer low to no information on what words are about.  
**Stopwords:** frequently encountered low information words. Removed as part of preprocessing.  
**corpus:** a body of documents  
**Stemming:** Methodology for grouping of non-unique words via root stems. Stem lists (stemmers) are curated by linguists. Use them.  
**TfIdf:** Term Frequency, Inverse document frequency. Weighting rarer words higher by document (Tf) or Corpus (Idf)

### Natural Language Tool Kit (NLTK)

#### Loading Stopwords from a corpus

```{python}
import nltk
nltk.download()                 # gui download tool
nltk.download('stopwords')      # just the stopwords

from nltk.corpus import stopwords
sw = stopwords.words("english")
```

#### Stemming

```{python}
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
stemmer.stem("responsiveness")
stemmer.stem("responsivity")
stemmer.stem("unresponsiveness")
```

_note:_ un is included with the stem of unresponsiveness. Modifying this behavior is part of configuring for your use case.  

#### Tf Idf

[https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Inverse_document_frequency](https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Inverse_document_frequency)  
[https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting](https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting)  

**Tf:** term frequency - frequency of word in document. tf(t,d)  
**Idf:** inverse document fequency - frequency of word in corpus. $idf(t)$  

Rarity in corpus and frequency in document result in a higher weight.

$$tf.idf(t,d) = tf(t,d)\times idf(t)$$  
$$idf(t) = \log{{1+n}\over{1+df(t)}}+1$$  

$n:$ total number of documents in set.  
$df(t):$ number of documents with term in set.  

[https://scikit-learn.org/stable/modules/feature_extraction.html](https://scikit-learn.org/stable/modules/feature_extraction.html)  

```{Python}
# count is a count matrix.
# sklearn.feature_extraction.text.CountVectorizer will convert a corpus to a count matrix
# TfidfTransformer normalizes a count matrix to a normalized tf-idf representation
from sklearn.feature_extraction.text import TfidfTransformer
transformer = TdifTransformer(smooth_idf=False)
tfidf = transformer.fit_transform(counts)
```

```{Python}
# Combine CountVectorizer with TfidTransformer.
# corpus is a list of documents
from sklearn.feature_extraction.text.TfidfVectorizer
vectorizer = TfidfVectorizer
x = vectorizer.fit_transform(corpus)
```

## Feature Selection

Make everything as simple as possible but no simpler.  

1. Intuition for new feature
1. Code the feature
1. Visualize
1. Repeat

Create new features, beware of bugs and bad logic.  
Determine if there's features that should be ignored.  

* Noisy
* Causes overfitting
* Highly correlated with other features (redundant)
* Performance concerns

Quality over Quantity.  
use the minimal amount of features to maximize information.  

### Univariate Feature Selection

Treat each feature independently and determine its impact on classification and regression.  

#### SKLearn univariate tools  

* SelectPercentile: select X% of highest impact features
* SelectKBest: select a number K of the highest impact features

### Bias Variance Dilemma

High Bias - over simplifies data. high error on training set. Lower number of features are prone to higher bias.  
High variance - lack of generalization leading to overfitting. higher error on test set compared to training set. Larger number of features are prone to higher variance. Excess tuning to minimize sum of squares errors leads to higher variance.  

Finding the balance between having enough features to accurately label features but not so many that you reduce the quality of the model.  

#### Regularization and Lasso Regression

Method of automatically penalizing extra features.  

Minimizing: ${SSE} + \lambda |\beta|$  
$\lambda$: penalty parameter  
$\beta$: coefficients of regression (number of features in use)  

Eliminate penalized features by setting their coefficients to zero.  

[https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html)  

```{Python}
import sklearn.linear_model.Lasso
features, labels = GetMyData()
regression = Lasso()
regression.fit(features, labels)
regression.predict([[2,4]])
print regression.coef_
```

## Principal Component Analysis (PCA)

Given any shape of data, through translation and rotation, find the coordinate system that best fits the longitudinal and orthogonal axis of the data.  

Determining latent features  
Reduction of dimensionality  
Reduction of noise  
visualizaition of high dimensional data  
Preprocessing for other algorithms  

Determine new center of origin for data set  
$x_0' = {{x_1 + x_2}\over{2}}$  
$y_0' = {{y_1 + y_2}\over{2}}$  

Find orthogonal axis of data  
Domination of Major Axis over Minor axis

Measurable vs Latent Variables  
e.g. Number of Rooms and Square footage are measurable variables of latent size  

Composite Features: Preserve Information while condensing features  

Dimensionality reduction for unsupervised relations
(Not a regression).  
(similar to a standard deviation)  

Neighborhood method
Variance: roughly the spread of a data ditribution  

The principal component of a dataset is the direction that has the largest variance.  

Maximal variance is found via linear algebra. Information is condensed to one line. Lost dimension is lost information (sum of distances between spots and principal component)

[https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html)

```{Python}
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
pca.fit(data)
pca.transform(data)

pca.explained_variance_ratio_                   # eigenvalues
pca.components_[n]                              # list of requested priniciple components
```

### Eigenfaces

Something that needs to be researched further.

## Validation

Training and testing data for performance estimation and checks against overfitting.

Changed to sklearn.model_selection in 0.17 [sklearn.cross_validation](https://scikit-learn.org/stable/modules/cross_validation.html)  
[https://scikit-learn.org/stable/modules/classes.html#module-sklearn.metrics](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.metrics)  
[https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html#sklearn.model_selection.train_test_split](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html#sklearn.model_selection.train_test_split)  

### Train/Test Split > PCA > SVM

Train - Fit  
Transform - Reduce Dimensionality  
Predict - Produce  

PCA: fit training features then transform training features  
SVM: fit training features  
PCA: transform testing features
SVM: predict testing features

### Cross Validation

Min/Max testing and training data split  

#### K-fold

1. partition dataset into k bins
1. Run k learning experiements
1. Average test results

K-fold gains accuracy at the cost of runtime  
[https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.KFold.html#sklearn.model_selection.KFold](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.KFold.html#sklearn.model_selection.KFold)  
Beware of sorted data introducing bias to K-folds

#### GridSearchCV

Automated parameter tuning  

[https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html)

```{Python}
parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}          # Parameters for testing
svr = svm.SVC()                                                 # Algorithm selection
clf = grid_search.GridSearchCV(svr, parameters)                 # Classifier creation with parameter optimization
clf.fit(iris.data, iris.target)                                 # Fit using optimized parameters
clf.best_params_                                                # property clf using best parameters
```

## Evaluation Metrics

### Accuracy

Number of items scored accurately out of all scored items.  
Limited in use with skewed populations  
_In a skewed population, the number of hits approaches zero in relation to the population._  

### Confusion Matrix

matrix of counts actual class crossed with predicted class  

$p: true positive$  
$\neg p: false positive$  
$\neg n: false negative$  

**Recall:** Out of all items classified as positive for the label, how many were classified correctly?  
Ratio of correctly labeled positive features out of total number of features that should have should have been labeled as positive.  
$Recall = p\over{p+\neg n}$  

**Precision:** given a prediction, what is the probability that prediction is correct?  
Ratio of correctly labeled positive features out of total number of features labeled as positive.  
$Precision = p \over {p + \neg p}$  

**F Score:** measure of accuracy based on precision and recall.  
[https://en.wikipedia.org/wiki/F1_score](https://en.wikipedia.org/wiki/F1_score)  

## Tying it All Together

Four major areas.

1. **Determine Dataset:** What is the question and what dataset can answer that question?
1. **Feature Selection:** Which features in the dataset will help you answer the question?  
1. **Algorithm Selection:** What algorithm to use and tune to learn from the features?
1. **Evaluation:** How accurate is the Algorithm?

![Summary](.\summary.png)

## Project - 6/7

Identify Enron employees who may have committed fraud.

### Provided Files

**poi_id.py:** starter code for POI identifier (submitted)  
**final_project_dataset.pkl:** project dataset  
**tester.py:** script used by Udacity to validate solution  
**emails_by_address:** directory of text files containing messages.  

### Features

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

**POI Label:** boolean  

### Series of Questions and Topics

1-2 paragraph answers  
[Answers Rubic](https://review.udacity.com/#!/rubrics/27/view)  

1. Summarize goal, role of machine learning and data usefulness.
    * data exploration
    * outlier investiagtion
1. What features were used and why?
    * create new features
    * intelligently select features
1. What algorithms were tried, which was selected?
    * pick an algorithm
1. How and why was the algorithm tuned?
    * discuss parameter tuning
    * tune the algorithm
1. Describe validation. How did you validate your analysis?
    * discuss validation
    * validation strategy
1. Generate and interperate evaluation metrics
    * usage of evaluation metrics

### Submission Files

* Code/classifier
  * my_dataset.pkl
  * my_classifier.pkl
  * my_feature_list.pkl
  * poi_id.py
  * readme for any supplimental scripts
* Written Doumentation
  * Answers to questions
  * References