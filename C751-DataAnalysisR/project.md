# Project Notes

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

1. Choose Data Set: [List](https://docs.google.com/document/d/e/2PACX-1vRmVtjQrgEPfE3VoiOrdeZ7vLPO_p3KRdb_o-z6E_YJ65tDOiXkwsDpLFKI3lUxbD6UlYtQHXvwiZKx/pub?embedded=true) - Wine Data Set
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