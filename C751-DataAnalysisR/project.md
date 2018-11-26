# Project Notes

# Getting Started

## Software To Install

* [R-CRAN](http://cran.r-project.org/)
* [R Studio](http://www.rstudio.com/products/rstudio/download/)

Add packages to R Studio

```R
install.packages("ggplot2", dependencies = T) 
install.packages("knitr", dependencies = T)
install.packages("dplyr", dependencies = T)
```

## Things to Learn

* Variable distribution, anomalies and outliers
* Variable quantification and visualizations
* Variables relationship identification
* Visualization methods

## Things to Produce

R-Markdown (RMD) file

* explore variables, structure, patterns, oddities and relationships
* Stream of consciousness
* [Project Template](https://d17h27t6h515a5.cloudfront.net/topher/2017/February/58af99ac_projecttemplate/projecttemplate.rmd) - [Alt](http://video.udacity-data.com.s3.amazonaws.com/topher/2017/February/58af99ac_projecttemplate/projecttemplate.rmd) - [local](.\projecttemplate.rmd)

HTML file

* knitted from RMD file

Data Set

* Include text file describing data source and variables (e.g. ?diamonds)

## How-To

1. Choose Data Set: [List](https://docs.google.com/document/d/e/2PACX-1vRmVtjQrgEPfE3VoiOrdeZ7vLPO_p3KRdb_o-z6E_YJ65tDOiXkwsDpLFKI3lUxbD6UlYtQHXvwiZKx/pub?embedded=true) - Red Wine Data Set
1. Organize 
1. Explore Data
1. Document Analysis
    * analysis and exploration
        * Univariate, Bivariate, Multivariate plots
        * Question, code, answer. Follow Thought Process
        * Plots and Visualizations 
            * 20 minimum
            * Varied type
            * Aesthetics 
    * final plots and summary
        * Three plots to reflect study
        * Identify Trends
        * Wide Audience
        * perception vs reality
        * Polished
    * reflection
        * on analysis process
1. Knit RMD
1. Data Documentation

* _knitr chunk_
* _pandoc options_

# Per Section Work

## Section 1 - Loading and investigating data

Loading a CSV file is as simple as calling the `read.csv` function and storing the output to a variable
```{R}
wines.red <- read.csv("wineQualityReds.csv")
```
After reading in a data set, it's a good idea to perform some initial investigation.  
To obtain a list of just the column names we use the `names` function
```{R}
names(wines.red)
```
the function `str` will return a short report on the data structure.
```{R}
str(wines.red)
```
Combining these, we can generate a list of the variables tracked in our dataset. Using that as a checklist, we can look for gaps and generate knowledge about these variables.

* X: This appears to be an untitled index field. We can probably exclude it as it is redundant to features included with R.
* fixed.acidity - This appears to be a decimal value measured in an unknown unit.
* volatile.acidity - This value appears to be measurements in hundredths of a unknown unit.
* citric.acid - another unknown unit based value. also reported in hundredths
* residual.sugar - decimal values of some unit with whole measurements of that unit
* chlorides - unknown unit, now getting down to the thousandths
* free.sulfur.dioxide - unknown unit, Whole values, could be integers
* total.sulfur.dioxide - expected to be similar and greater than the free values for sulfur dioxide.
* density - Are these metric?
* pH - The variable is a unit of measure
* sulphates - Unknown unit of measure
* alcohol - Unknown unit of measure
* quality - Construct

There's not enough information within the dataset to have a good understanding of the data it contains. There's just too many measured variables with unknown units of measure. A quick glance at the accompanying documentation provides this missing information.
[https://s3.amazonaws.com/udacity-hosted-downloads/ud651/wineQualityInfo.txt](https://s3.amazonaws.com/udacity-hosted-downloads/ud651/wineQualityInfo.txt)

I do notice this dataset contains construct describing the wine's quality. The value for this field is based on the opinion of experts. Whenever there's an numeric score assigned to opinion, there's a question of how harsh or lenient the opinions utilize the given range. In this case, the range is stated as 1-10. What is the utilization of the stated range? This is a question that can be answered with a simple histogram

```{R}
qplot(data = wines.red, x = quality, binwidth = 1)
```

This produced an normal distribution with a mode in the middle of our range. This suggests an evenly applied opinion scale. If the scale was shifted to the right, opinions would be too lenient. The idea being, if everyone is exceptional then no one is exceptional. If such a shift existed, we should strongly consider correcting the scale.  

When correlating variables there is an expectation of potential shift. Perhaps wine of better quality was produced in one year compared to another. These cases would have a shift in our scale.  

As we investigate this dataset, we will look into the available variables for a shift in quality distribution. A measurable shift to the right or left would suggest that variable has an effect on wine quality.  

To start that investigation, we'll take a quick look at a statistical summary of our dataset.

```{R}
summary(wines.red)
```

Two that stand out are the sulfur dioxide values. They both have a wide range with a mean above the median. Both their mean and median do not fall anywhere near the middle of their range. A quick look at the distribution of sulfur content shows it is skewed.

```{R}
qplot(data = wines.red, x = free.sulfur.dioxide, binwidth=3)
qplot(data = wines.red, x = total.sulfur.dioxide, binwidth=10)
```

## Section 2 - Exploring One Variable

* Faceting
* Skeptical of Outliers and Anomalies
* Exploring with bin widths
* Plot Labeling
* Transforming/Scaling
* Frequency Polygons
* Box Plots