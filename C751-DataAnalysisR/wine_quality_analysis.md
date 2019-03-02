# Chemical Composition as Predictor of Wine Quality

by Michael Jenkins  

```{r echo=FALSE, message=FALSE, warning=FALSE, packages}
library(ggplot2)
library(knitr)
library(dplyr)
library(data.table)
library(GGally)
library(gridExtra)
library(reshape2)
library(RColorBrewer)
library(scales)
```

```{r echo=FALSE, Load_the_Data}
wines.red <- read.csv("wineQualityReds.csv")
wines.white <- read.csv("wineQualityWhites.csv")
```

## Introduction

When shopping for a bottle of wine, it can be difficult to choose due to all \
of the available options. These datasets about wine could offer some insight \
to make those decisions easier. I have a preference for red wine. So that's \
where I'll begin.  

They contain a sampling of wine chemical composition and a quality rating. \
Quality is determined by an average of expert opinions. Compositional \
qualities are provided in a variety of measurements across 10 variables. In \
total, there are 6,497 observations with 1,599 red and 4,898 whites.  

This dataset should give a good exploration between the relationship of wine \
quality and chemical composition.  

The datasets explored in this analysis were found \
[here for red](https://bit.ly/2KTzkjX) and \
[here for white](https://bit.ly/1QqxDBL). The accompanying documentation of \
the datasets can be found [here](https://bit.ly/2vinuZz).  

### Citations

P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis.  
Modeling wine preferences by data mining from physicochemical properties.  
In Decision Support Systems, Elsevier, 47(4):547-553. ISSN: 0167-9236.  

[@Elsevier] http://dx.doi.org/10.1016/j.dss.2009.05.016  
[Pre-press (pdf)] http://www3.dsi.uminho.pt/pcortez/winequality09.pdf  
[bib] http://www3.dsi.uminho.pt/pcortez/dss09.bib  

## Univariate Investigation

First a quick look at the data structure.  

```{r echo=FALSE, Initial_Data_Structure}
str(wines.red)
```

There's not much to go on with just raw numbers. We'll need to investigate the \
accompanying documentation to give context to these numbers. From the \
documentation we find the data set contains compositional measurements of \
various solutes found within a solution of wine. Also included is a measure of \
quality saved as an integer.  

This investigation is primarily concerned with predicting wine quality from \
wine composition. It only makes sense to start with an investigation of the \
quality score. How utilized is the 0-10 quality scale?  

```{r echo=FALSE, Quality_Scale_Validation}
summary(wines.red$quality)
```

With a minimum of three and a maximum of eight, it's fair to say the range is \
under utilized. With a median near the mean, there's no reason to suspect \
skew. What does give me pause is the 1st and 3rd quartiles are separated by 1. \
This would suggest an inordinate occurrences of middling quality range. \
Histograms are cheap and will give a quick visualization to confirm.  

```{r echo=FALSE, Red_Quality_Distribution}
ggplot(data=wines.red, aes(x=quality)) +
  geom_histogram(binwidth = 1)
```

It appears the dataset does primarily consist of wines of average quality. \
A pie-chart would provide an understanding of how homogenous the population \
quality is.  

```{r echo=FALSE, Univariate_Plots}
red_quality_counts <- wines.red %>%
  group_by(quality) %>%
  summarise(no_obs = length(quality))

ggplot(data = red_quality_counts, 
       aes(x = "", y = no_obs, fill = quality)) + 
  geom_bar(width = 1, stat="identity") + 
  coord_polar("y", start=0)
```

Wines of average quality definitely account for a large portion of our sample. \
Without performing a calculation, I estimate about 80% of the red wine sample \
are of average quality.  

It might be valuable to include the sample of white wines to increase the \
sample size.  

```{r echo=FALSE, White_Wine_Structure}
str(wines.white)
```

The datasets share a source. It makes sense they would have compatible \
variables. However, white wine does contain about two and a half times the \
sample size of red wines.  

Remember, the primary purpose of adding the white wine dataset to the \
investigation is to increase the granularity of quality ratings. There is the \
possibility that including white wine will skew our data.  

```{r echo=FALSE, White_Wine_Quality_Scale}
summary(wines.white$quality)
```

Not much is different. The mean and 1st to 3rd quartiles are unchanged. On a \
successful note, the quality range is better utilized. We now have a \
population of wines rated as nine.  

Perhaps the distribution of quality for white wines has greater utilization.  

```{r echo=FALSE, White_Wine_Quality_Distribution}
ggplot(data=wines.white, aes(x=quality)) +
  geom_histogram(binwidth = 1)
```

That's diappointing. There is still a disproportionate number of average \
quality wines in the white sample.  

```{r echo=FALSE, White_Wine_Quality_Proportions}
white_quality_counts <- wines.white %>%
  group_by(quality) %>%
  summarise(no_obs = length(quality))

ggplot(data = white_quality_counts, 
       aes(x = "", y = no_obs, fill = quality)) + 
  geom_bar(width = 1, stat="identity") + 
  coord_polar("y", start=0)
```

That disproportion is more apparent in a pie chart. Still, A lesser percentage \
of white wines are considered average quality. It seems approximately 75% of \
the sample is rated at five and six compared to the 80% of reds. So there \
was some success in our attempt at gaining granularity.  

### Univariate Analysis

There may not be enough of a sample size to predict if a wine is of \
exceptionally good or poor quality based on its composition alone. There does \
seem to be enough samples to determine the chemical make-up of an average \
quality wine.  

Perhaps it will be enough to predict if a wine is of average quality. If it \
doesn't, then it's either very bad or very good. With this thinking, analysis \
on average vs. not-average may provide the best insight this data-set can \
provide. We might be able to say what makes a wine average.  

#### Dataset Description

Some rudimentary research on wine research turned up \
[Wine Chemistry on Wikipedia](https://en.wikipedia.org/wiki/Wine_chemistry). \
From this we see there's a possibly of some missing measures. For example, \
phenolic compounds and proteins. The possibility of missing solute data is \
a cause of concern. However, The accompanying documentation makes the claim no \
compositional information is missing. We'll proceed with the information we do \
have.  

The datasets contain thirteen variables for each observation. Ten of those \
variables describe composition. Eight of the ten are measures of \
concentration. Alcohol content is provided as a percent. Density provides a \
measure of the entire solution. Some of the solute measures are the same. \
Some are of different units. These should be converted to equal units of \
measure. With equal units, we can make better compositional comparisons.  

The remaining variables are not compositional measurements. X is an index that \
is not linked to another dataset. It can be discarded. Quality is 
provided as an integer. There may be cause to convert it to a factor. \
Converting quality to a factor would reduce the scale. This may complicate \
any future additions to the dataset. Finally there's Ph. Ph is is a \
descriptor of acidity. It may be of interest to explore the relationship \
between total acidic composition and Ph.  

#### Points of Interest

Of most interest are the measures of concentration. The mass per volume of \
each solute is assumed to have a corelative relationship to the wine's \
quality. Comparing the ratios of a wine's compostition correlated to the \
wine's quality is the most interesting feature to investigate.  

Another interest is the non-compositional value of Ph. There's a few questions \
we can try to answer here. What commonality between Ph values exists at varied \
concentrations of acidic solute? Is there a relationship between Ph and \
quality?  

With both red and white datasets, we can also investigate differences between \
the two types. How do their compositions differ? Do those compositional \
differences affect the qualitative scale between whites and reds?  

## Data Preparation

As previously noted, we will need to convert our compositional data to units \
of equal measure. First we should consider what options are available and \
which best fits our purpose.  

The first option is mass per volume. The data is presented to us in this \
format. This could be a good measure to perform investigation. Grams per \
cubic meter may be a common measure to the drug markets. I'd like a unit of \
measure that is more widely understood.  

Parts per million (ppm) is a commonly reported unit of concentration. This \
would make for easily reported values. What effect would a scale in the \
millions have on visualizations?

A solute's percentage of a solution should cover these concerns. A summation \
of solute percent can be used to determine the ratio of solvent in each \
solution of wine. Percents should provide a more manageable scale, and are \
commonly understood.

If any of these assumptions about percents proves false, it will be easy to \
convert back to another better suited measure. 1% is equal to 10,000 ppm and 1 \
ppm is equal to 1 mg/L. We can also easily convert to grams per serving. \
There's 33.8 ounces in a liter and 5 ounces in a serving.

Having considered the options, we can generate a working dataset. The \
following list should cover what has been decided on.

1. Add a field to note the wine's color.
1. Merge the two datasets into one.
1. Add a logical field to note if the wine is ordinary. (i.e. quality is 5 or 6)
1. Convert density from grams per cubic centimeter to grams per cubic \
decimeter. (i.e. multiply by 1000)
1. Convert Sulfur dioxides from milligrams per cubic decimeter to grams per \
cubic decimeter. (i.e. divide by 1000)
1. Convert solute concentration values to percents. (i.e. divide their value \
by density and multiply by 100)
1. Add fields for total solute and solvent percents.

```{r echo=FALSE, Data_Conversion}
# Add a color field
wines.red$color = "red"
wines.white$color = "white"

# Merge the datasets into a temporary table
winesTmp <- rbind(wines.red,wines.white)

# Add a field to delineate average wines from others.
winesTmp$quality.class = ifelse((winesTmp$quality == 5 | 
                                   winesTmp$quality == 6), 'ordinary', 
                                'extreme')

# Factor the quality values
winesTmp$quality.class <- factor(winesTmp$quality.class)
winesTmp$quality <- factor(winesTmp$quality)

# Drop the unused index
winesTmp <- subset(winesTmp, select = -c(X))

# Convert values to grams per cubic decimeter
winesTmp$density <- winesTmp$density * 1000
winesTmp$free.sulfur.dioxide <- winesTmp$free.sulfur.dioxide / 1000
winesTmp$total.sulfur.dioxide <- winesTmp$total.sulfur.dioxide / 1000

# Group columns that will be excluded in percent conversion
notConcentrate <- names(winesTmp) %in% 
  c('pH', 'color', 'alcohol', 'quality', 'quality.class', 'density')

# Convert grams per cubic decimeter to percent solution 
# Store results in final table
wines <- winesTmp[,!notConcentrate] / winesTmp[,"density"] * 100
wines <- cbind(winesTmp[,notConcentrate],wines)

# Prepare columns for solute to solvent calculations
solutes <- names(winesTmp) %in% 
  c('alcohol', 'fixed.acidity', 'volatile.acidity', 'citric.acid', 
    'residual.sugar', 'chlorides', 'total.sulfur.dioxide', 'sulphates')

# Calculate and add solute and solvent percents to table
wines$total.solute <- rowSums(wines[,solutes])
wines$total.solvent <- 100 - wines$total.solute

# clean up after ourselves
rm('notConcentrate')
rm('winesTmp')
rm('wines.red')
rm('wines.white')

# Inspect our final work
head(wines)
```

### Data Preparation Aftermath

Having cleaned up the data, I'd like to take note of the variables added. It \
is good to keep track of such things. Just in case we forget why they were \
added.  

The sum of the percent solutes does not account for the total solution. With \
no information on the composition of the remaining solution, and the claim \
there are no missing attributes, we must assume the unaccounted solution is a \
tasteless solvent (e.g. water). We're also making the assumption that alcohol \
is not a solvent for this case. Higher solvent content may be a factor in \
determining quality. We could hypothesize Watered down wine is of lower \
quality. These values will allow us to test these hypotheses.  

Another variable we added retains information on which dataset the observation \
originated from. This will allow us to compare the differences between red and \
white wines. As someone with a preference for reds, I think this part is the \
most important.  

The exceptional vs ordinary variable is intended for exploring what is common \
in wines of average quality. In this case, exceptional is defined as not \
average. Exceptionally bad and exceptionally good wines have similar numbers \
of observations. Comparing what makes for average vs. non-average wine and \
then comparing both ends of the extremes may give a more complete picture of \
wine quality.  

Finally, the solute columns were changed from mass per volume to percents. \
Density, by definition is 100% of the solution this is shown in our \
calculation. We should also not forget the unit conversions we have. While we \
are working with percents, it helps to be able to report whichever value is \
most conducive.

1% is equal to:  

* 10,000 ppm
* 10 g/L
* 1.48 g per serving

## Bivariate Investigation

When cleaning up the dataset, a number of questions were raised on the \
relationships between variables. A matrix synopsis between the solutes should \
give a good direction on where to go.  

### Universal Comparisons

```{r echo=FALSE, The_Matrix}
# Define items for the matrix
subjects <- c('alcohol', 'fixed.acidity', 'volatile.acidity', 
    'citric.acid', 'residual.sugar', 'chlorides', 'total.sulfur.dioxide', 
    'sulphates', 'free.sulfur.dioxide', 'pH', 'quality.class', 'quality')

# Create the matrix
theme_set(theme_minimal(base_size=8))
ggpairs(wines[,subjects], progress = FALSE, 
        lower=list(combo=wrap("facethist", binwidth=15)))
```

From this initial comparison, it seems alcohol content is the best predictor \
of wine quality. It also suggests the thought of average versus other may not \
provide the results hoped for. Based on the distribution of alcohol content by \
quality, there's more sense in breaking quality as less than average and better \
than average values. This would regroup the observations with a split between \
qualities 5 and 6.  

The strongest solute correlation is between free sulfur dioxide and total \
sulfur dioxide. This makes sense as one is a subset of the other. Sulfuric \
content related to quality does have an interesting phenomena. It appears that \
lower quality wines have larger range of sulfur dioxide content.

Acidic content also appears to have a slight impact on wine quality. The upper \
and lower bounds of acidic solutes lessens as quality improves. Total acidic \
content could be investigated further.

Total solvent and color are missing from the comparisons. They should be added \
in the next comparison set. Variable ordering should also be adjusted in the \
next comparison set.

### Refined Comparisons

```{r echo=FALSE, The_Matrix_Reloaded}
# Add new values
wines$quality.class = ifelse(as.numeric(wines$quality) <= 3, 'lesser', 'better')
wines$quality.class = factor(wines$quality.class, levels=c('lesser', 'better'))
wines$total.acid <- rowSums(wines[,c('fixed.acidity', 'volatile.acidity', 
                                     'citric.acid')])

# Redefine values for the matrix
subjects <- c('alcohol', 'total.solvent', 'pH', 'total.acid', 'fixed.acidity',
              'volatile.acidity','citric.acid', 'residual.sugar', 'chlorides', 
              'total.sulfur.dioxide', 'sulphates', 'free.sulfur.dioxide',
              'color', 'quality.class', 'quality')

# Reload the matrix
theme_set(theme_minimal(base_size=8))
ggpairs(wines[,subjects], progress = FALSE, 
        lower=list(combo=wrap("facethist", binwidth=15)))
```

This new set has a higher number of correlated values. As alcohol content \
increases, total solvent decreases. This suggests that alcohol is a greater \
portion of the solution than the other solutes. The opposite is true for \
total acid and fixed acidity. As one increases, so does the other. This \
suggests that fixed acidity has a higher proportion of total acidity than the \
other acidic forms.  

Residual sugar appears to be consistent through all observations. This is \
surprising due to the relationship between sugar as a fuel for yeast to turn \
into alcohol.  

Despite the low correlation between pH and total acidity, there does appear to \
be a loose relationship. As total acidity increases, the pH drops (becomes \
more acidic). There's also appears to be a slight relationship between acidity \
and quality. Fixed acidity, citric acid and pH seems to be consistent through \
all grade qualities. Volatile acidity seems to have a higher content in lesser \
quality wines.  

We start to see hints at the variation in chemical makeup between red and \
white wines. White wines tend to have more residual sugar, more sulfur \
dioxides, and lower pH. The lower pH of white wines contrasts with the lower \
acidic content of white wine. Remember, lower pH means more acidic. The \
expectation is higher acidic content would have lower pH. One possible \
explanation is fixed vs. other forms of acid.  

I did note earlier that the range of total sulfur dioxide is greater at lower \
qualities. However, the mean of sulfur dioxide content does remain constant. \
The difference in range could be attributed to white wine's tendency to have a \
higher concentration of sulfur dioxides than red wines. There's some logic to \
save these values for a future analysis. One with greater focus on the \
compositional differences of red and white wines.  

The effect of acidic compounds and pH on quality also appears to be dependent \
on wine variety. With all of these differences between red and white, It would \
be good to compare red and white composition separately.  

### Comparisons of Varietals

#### Red

```{r echo=FALSE, The_Matrix_Red_Band}
theme_set(theme_minimal(base_size=8))
ggpairs(subset(wines[,subjects], color=="red"), progress = FALSE, 
        lower=list(combo=wrap("facethist", binwidth=15)))
```

#### White

```{r echo=FALSE, The_Matrix_White_Band}
theme_set(theme_minimal(base_size=8))
ggpairs(subset(wines[,subjects], color=="white"), progress = FALSE, 
        lower=list(combo=wrap("facethist", binwidth=15)))
```

When splitting out the comparisons by color. It's easier to see how \
differences in composition affects quality. Acidic and sulfuric compounds are \
a greater predictor of wine quality in reds than whites. Across both types, \
alcohol remains the greatest predictor of wine quality. Acidic and sulfuric \
compounds will be reserved for future analysis.  

Is there something that indirectly influences quality? A relationship between \
alcohol content and the remaining compounds? What are the ratios of other \
compounds compared to alcohol content?  

Distribution of chlorides (salt) across alcohol seems to match the curve of \
alcohol content for all types. Less alcoholic wine tends to have more salt. \
Aside from some outliers, the percent salt content in red and whites appears \
to be similar.

Despite the low correlation, residual sugar and alcohol content also appears \
to have a universal trend across the varietals. We can only speculate on the \
unknown factors that would produce such a result. One factor could be the \
starting sugar. Another might be the yeast used to convert sugar to alcohol. \
At what alcohol content does that yeast die? Was the fermentation process \
interrupted at a certain point? These are questions we don't have the answers \
too. We shouldn't ignore this apparent relationship due to unknown influences.  

From all of this, the plots between alcohol, salt and sugar should be the \
center of our exploration. There appears to be some type of relationship \
between alcohol and quality. There's also appears to be a relationship between \
ratios of salt and sugar to alcohol. Before moving forward, it's only prudent \
to take some steps back.  

### Alcohol and Quality

```{r echo=FALSE, Alcohol_Content_Distribution} 
ggplot(aes(x = alcohol), data = wines) +
  geom_histogram(binwidth = .4, color = 'black', fill = 'orange')
```

Distribution of the alcohol content in our samples is right skewed. Are the \
samples of higher content skewing the quality contents? So far, we've \
been directing our thinking on alcohol content and wine quality by the \
tendency of higher average alcohol content at higher levels of quality. We \
should take a closer view at the data to support this assumption.  

```{r echo=FALSE, Alcohol_by_Quality}
ggplot(data=wines, aes(x=quality, y=alcohol)) +
  geom_point()
```

There's quite a bit of overplotting in that graph. Still, there is some \
pattern in the extreme qualities.  

```{r echo=FALSE, Alcohol_by_Quality_Better_Visibility}
ggplot(data=wines, aes(x=quality, y=alcohol)) +
  geom_jitter()
```

Wine samples graded as a 9 can be counted on one hand. There's still a bit of \
overplotting. It is more clear to see the clusters of samples rise as quality \
improves.  

```{r echo=FALSE, Alcohol_by_Quality_Most_Visible}
ggplot(data=wines, aes(x=quality, y=alcohol)) +
  geom_jitter(alpha=.4) 
```

Reducing the alpha a bit and the change in the clusters become more clear. \
It's also clear we can't say that wine quality will be better just because the \
alcohol content is higher. This is different from saying higher quality wines \
tend to have higher alcohol content. Do not confuse this with saying lower \
quality wines will always have lower alcohol content.  

```{r echo=FALSE, Alcohol_by_Quality_Categories}
ggplot(data=wines, aes(x=quality.class, y=alcohol)) +
  geom_jitter(alpha=.4)
```

Taking the bins we've defined for lesser and better quality shows a clearer \
picture. Better quality wines seems evenly dispersed across the range of \
alcohol content. It looks that the cut off is just above 10% alcohol \
content. Wines with more than 10% alcohol content are more likely to be of \
better quality.  

Considering we would rather increase than give up resolution of quality, \
it would be good take a look at the upper and lower quality wines bins from \
another perspective. To facilitate this, let's recreate the smaller bins \
without the added field.  

```{r echo=FALSE, Alcohol_by_Binned_Quality}
wines %>%
  subset(as.numeric(quality) < 7) %>%
  group_by(class=cut(as.numeric(quality), breaks=seq(0, 7, by = 3))) %>%
  ggplot(data=., aes(x=class, y=alcohol)) +
  geom_jitter(alpha=.4)
```

We ended up dropping wines of quality 9. As there are so few observations with \
that rating, it could be considered outliers. Basically this is the same graph \
as previously created. The benefit of this method is allowing us to maintain \
quality granularity within wines of better of lesser quality.  

I'm also having some regret in the decision to transform quality into a \
factor. That does give more control over the scale. That additional control is \
under utilized when quality is on an integer scale.  

```{r echo=FALSE, Alcohol_at_Higher_Quality}
wines %>% 
  subset(as.numeric(quality) > 3) %>%
  ggplot(aes(x=quality, y=alcohol)) +
  geom_jitter(alpha=.4)
```

Taking a closer look at the breakdown of the better quality wines, We see that \
wines of quality 6 runs the full spectrum of alcohol content. Disregarding \
wines of quality 6, better wines start to occur more frequently at alcohol \
content near 10-11%. Wines of the highest quality have even fewer occurrences \
with alcohol content under ~9.5%.

```{r echo=FALSE, Alcohol_at_Middle_Quality}
wines %>% 
  subset(as.numeric(quality) >= 3 & as.numeric(quality) <= 5) %>%
  ggplot(aes(x=quality, y=alcohol)) +
  geom_jitter(alpha=.4)
```

The shift for wines of greater vs lesser quality around 10% is more apparent \
by limiting the view to the middle quality scores. Wines of quality 6 appear \
to be a merge between wines of quality 5 and 7.  

```{r echo=FALSE, Alcohol_at_Lowest_Quality}
wines %>% 
  subset(as.numeric(quality) <= 3) %>%
  ggplot(aes(x=quality, y=alcohol)) +
  geom_jitter(alpha=.4)
```

Breaking out the least quality wines shows a dispersion that rarely breaks \
11.5% alcohol. If the least quality wines rarely rise above 11.5% alcohol and \
the highest quality wines rarely have less than 9.5% alcohol, then the \
average quality wines must fall within that range.  

What would happen to our graphs if we eliminated the ordinary wines defined as \
having alcohol content between 9.5% and 11.5%? This also revisits the idea of \
average versus non-average wines. We have a definition of what makes for an \
ordinary wine. Eliminating those from our views, it should become easier to \
see the differences at the extremes.  

```{r echo=FALSE, Alcohol_and_Quality_missing_middles}
wines %>% 
  subset(alcohol <= 9.5 | alcohol >= 11.5) %>%
  ggplot(aes(x=quality, y=alcohol)) +
  geom_jitter(alpha=.4) +
  stat_summary(fun.y = mean, fun.ymin = mean, fun.ymax = mean,
                 geom = "crossbar", width = 1, color = 'red')
```

The cut off between better and lesser quality wines is even easier to see when \
we remove the middle range of alcohol content. This split more clearly occurs \
at some granularity of quality rated 6.  

It's now clear that quality 6 wines are ambiguous in quality. We should look \
back at the lesser vs better quality graph while eliminating the ambiguous \
value.  

```{r echo=FALSE, Quality_Minus_Ambiguity}
wines %>%
  subset(as.numeric(quality) < 7 & as.numeric(quality) !=4) %>%
  group_by(class=cut(as.numeric(quality), breaks=seq(0, 7, by = 3))) %>%
  ggplot(data=., aes(x=class, y=alcohol)) +
  geom_jitter(alpha=.4) +
  stat_summary(fun.y = mean, fun.ymin = mean, fun.ymax = mean,
                 geom = "crossbar", width = 1, color = 'red')
```

It is now a quite clear relationship between quality and alcohol content. We \
should remember the quality scale is subjective and based on the opinion of \
experts. It's possible those experts have a preference for higher alcohol \
content in their wines. On the observations made this far, I would suggest \
that preference is likely.  

As part of due diligence, we should a look at actual value correlation between \
quality and alcohol.  

```{r echo=FALSE, Quality_Alcohol_Correlation}
cor.test(wines$alcohol, as.numeric(wines$quality))
```

Across all samples, there is a moderate correlation between quality and \
alcohol content. This correlation includes the ambiguous quality rating. This \
is a central value that fits the model but skews the data. This skew appears \
to be because of a lack of resolution in the quality scale. What happens to \
correlation if we omit this ambiguous score?  

```{r echo-FALSE, Quality_Alcohol_Adjusted_Correlation}
wines.noMiddle <- subset(wines, as.numeric(quality) != 4)
cor.test(wines.noMiddle$alcohol, as.numeric(wines.noMiddle$quality))
rm(wines.noMiddle)
```

By omitting the ambiguous quality value on our scale, the correlation \
becomes strong. I would hypothesize, if we had a more granular and less \
subjective quality scale the correlation between would be even stronger. For \
now, I will state that alcohol is an acceptable measure of quality. It lends \
greater granularity than the current quality scale.  

```{r echo-FALSE, Alcohol_Summary}
summary(wines$alcohol)
```

The earlier observations on the upper limit of alcohol content for lower \
quality wines and lower limit for higher quality wines fall almost exactly on \
the 1st and 3rd quartiles of the alcohol content range. This gives even more \
confidence in the assertion that alcohol is the measure of quality.  

## Bivariate Analysis

> **Tip**: As before, summarize what you found in your bivariate explorations
here. Use the questions below to guide your discussion.

To summarize, there is a strong correlation between wine quality and alcohol \
content for wines outside of average alcohol content and not of average \
quality. The number of qualifiers for this correlation is due to the \
granularity of the subjective scale used to convey quality. Without a more \
granular quality scale, we can only assume the trend maintains for wines \
of average quality and average alcohol content.

Given this assumption, we can take alcohol content as an objective measure of \
quality. With this as an objective measure, we can better investigate the \
ratios of other solutes as they relate to our quality surrogate.

Across both colors of wine, chlorides (salt) and residual sugar have an \
interesting relationship with alcohol. These compounds should be explored for \
their contribution to wine quality.


### Talk about some of the relationships you observed in this part of the \
investigation. How did the feature(s) of interest vary with other features in \
the dataset?

### Did you observe any interesting relationships between the other features \
(not the main feature(s) of interest)?

### What was the strongest relationship you found?


# Multivariate Plots Section

> **Tip**: Now it's time to put everything together. Based on what you found in
the bivariate plots section, create a few multivariate plots to investigate
more complex interactions between variables. Make sure that the plots that you
create here are justified by the plots you explored in the previous section. If
you plan on creating any mathematical models, this is the section where you
will do that.

Using alcohol as a surrogate to quality, how does salt concentration compare \
at various levels of alcohol?

```{r echo=FALSE, Multivariate_Plots}
ggplot(data=wines, aes(x=alcohol, y=chlorides)) +
  geom_jitter(alpha=.4)
```

The majority of wines have less than a hundredth of a percent of salt. There's \
a jump in salt content around 9.5 percent alcohol. Most of them appear to be \
outliers. This could use some subsetting and scaling to get a better picture.

```{r echo=FALSE, Multivariate_Plots}
ggplot(data=subset(wines, chlorides < .03), aes(x=alcohol, y=chlorides)) +
  geom_jitter(alpha=.2) +
  scale_y_log10() +
  geom_smooth()
```

On a log10 scale, it's easier to see the fraction of a fractional difference \
between each level of alcohol content. Across the range of average alcohol \
content we see a consistent drop in salt content from ~0.006 to ~0.004 percent.  

```{r echo=FALSE}
ggplot(data=subset(wines, chlorides < .03), aes(x=alcohol, y=chlorides)) +
  geom_jitter(alpha=.4) +
  scale_y_continuous(limits = c(.002, .006)) +
  geom_smooth()
```

Using this natural scale, the drop is even more dynamic.

What about sugar content?

```{r echo=FALSE}
ggplot(data=wines, aes(x=alcohol, y=residual.sugar)) + 
  scale_y_continuous() +
  geom_smooth()
```

Low alcohol content wine has a large amount of residual sugars. This seems \
logical as sugar is what yeast uses to create alcohol. There's interesting \
bumps in alcohol content near where the average and better than averge wines \
were determined. this should be compared to a scatterplot to look for any \
outliers that may be skewing the data.

```{r echo=FALSE}
ggplot(data=wines, aes(x=alcohol, y=residual.sugar)) + 
  scale_y_continuous() +
  geom_jitter(alpha=.5) +
  geom_smooth()
```

There does appear to be outliers above 2.5% residual sugar

```{r echo=FALSE}
ggplot(data=subset(wines, residual.sugar <= 2.5), aes(x=alcohol, 
                                                  y=residual.sugar)) + 
  scale_y_continuous() +
  geom_jitter(alpha=.4) +
  geom_smooth()
```

The bump does seem to be valid. One reason this could be is the type of yeast \
used. Another reason could be interuption in the ferment process. Type of \
grape used is another possiblity. Grape type or wine color is one possiblity \
that we do have data to test.

```{r echo=FALSE}
ggplot(data=subset(wines, residual.sugar <= 2.5), aes(x=alcohol, y=residual.sugar)) + 
  scale_y_continuous() +
  geom_jitter(alpha=.4) +
  geom_smooth(aes(color=color))
```

Reds wines appear to have a consistent residual sugar content across all \
alcohol levels. It's white wines that have a sharp drop in sugar content \
across levels. Is there a similar phenomenon in salt content?

```{r echo=FALSE}
ggplot(data=subset(wines, chlorides < .03), aes(x=alcohol, y=chlorides)) +
  geom_jitter(alpha=.4) +
  scale_y_log10(limits = c(.002, .02)) +
  geom_smooth(aes(color=color))
```

White wines have less salt than reds. White wines also have \
a more pronounced drop in salt content as alcohol content increases.

Returning to sugar content, sugar content in red wines is lower than \
white wines. It might be helpful to break these into their own scales.

```{r echo=FALSE}
ggplot(data=subset(wines, residual.sugar <= 0.7 & color == "red"), aes(x=alcohol, y=residual.sugar)) + 
  scale_y_continuous() +
  geom_jitter(alpha=.5) +
  geom_smooth(aes(color=color))
```

Unlike white wines, red wines appear to have a slight increase in sugar \
content as alcohol increases. It's so slight, starting around 0.225 and \
ending near 0.25. Given the low sample size and lack of measurement error, \
the best we can say is red wine has consistent sugar content across all \
values. There may be some miniscule differences, but there's not enough \
information to say sugar content is a contributing factor in wine quality.

To be sure, we can check this hypothesis.

```{r echo=FALSE}
ggplot(data=subset(wines, residual.sugar <= 0.7 & color == "red"), 
       aes(x=quality, y=residual.sugar)) + 
  scale_y_continuous() +
  geom_smooth(aes(color=color)) +
  geom_boxplot()
```

The majority of values reside under 0.4% sugar content. Adjusting both graphs \
might yield a better image. Before making this adjustment, it's worth noting \
the 1st quartile and mean is fairly consistent across quality range. There is \
some variation in the 3rd quartile, but no consistent pattern.  

```{r echo=FALSE}
p1 <- ggplot(data=subset(wines, residual.sugar <= 0.4 & color == "red"),
             aes(x=alcohol, y=residual.sugar)) + 
  scale_y_continuous() +
  geom_jitter(alpha=.5) +
  geom_smooth(aes(color=color))

p2 <- ggplot(data=subset(wines, residual.sugar <= 0.4 & color == "red"), 
       aes(x=quality, y=residual.sugar)) + 
  scale_y_continuous() +
  geom_smooth(aes(color=color)) +
  geom_boxplot()


grid.arrange(p1,p2, ncol = 1)

```

Removing these outliers has produced a more consistent pattern in both \
graphs. The sugar content for the range of alcohol content is more flat. \
Sugar content at each quality score has a consistent mean with variation \
occuring at the 1st and 3rd quartiles. This also supports our earlier \
investigation showing that alcohol content is a good predictor of wine \
quality.  

One final graph I want to look at is alcohol content at ratios \
of salts and sugar.

```{r echo=FALSE}
wine.tastes <- data.frame("sugar" = round(wines$residual.sugar, 2), 
                          "salt" = round(wines$chlorides, 4),
                          "alcohol" = wines$alcohol,
                          "type" = wines$color)
head(wine.tastes)

```

```{r echo=FALSE}
wine.ratios <- melt(wine.tastes, id.vars = c("sugar", "salt", "type"))
wine.ratios
```

```{r echo=FALSE}
ggplot(aes(y = sugar, x = salt, fill = value),
  data = wine.ratios) +
  geom_tile() +
  scale_fill_gradientn(colours = colorRampPalette(c("blue", "red"))(100)) +
  scale_y_continuous(limits = c(0,2)) + 
  scale_x_continuous(limits = c(0,0.02))
```

What we see is a concentration of higher alcohol content at \
lower salt and lower sugar content. Some of that could be attributed to the \
intersection of red and white wines. 

Red wine tends to have a much lower sugar content and higher salt content than \
white wine. That does explain the lower leg of this graph.  

Another thing to consider is the range of alcohol content as wine quality. \
The spread of alcohol content across ratios of sugar to salt becomes more \
apparent by introducing more colors to our graph.

```{r echo=FALSE}
ggplot(aes(y = sugar, x = salt, fill = value),
  data = wine.ratios) +
  geom_tile() +
  scale_fill_gradient2(low = "green", mid = "blue", high = "red", 
                       midpoint = 12) +
  scale_y_continuous(limits = c(0,2)) + 
  scale_x_continuous(limits = c(0,0.02))
```

It becomes even more clear that lower alcohol content wines tend to \
occur at extreme values of sugar and salt content.

```{r echo=FALSE}
ggplot(aes(y = sugar, x = salt, fill = value),
  data = wine.ratios) +
  geom_tile() +
  scale_fill_gradientn(colours = colorRampPalette(
    c("orange","green","blue", "red"))(50)) +
  scale_y_continuous(limits = c(0,2)) + 
  scale_x_continuous(limits = c(0,0.02))
```

Introducing more colors doesn't provide any additional insight. It does help \
solidify what we've already seen. It also helps futher illustrate at which \
ratios of sugar to salt we're getting the highest alcohol content. There \
seems to be the highest concentration of red dots near 0.0025% salt and \
0.25% sugar.

It's worth noting that what has been refered to this far as a ratio between \
two compounds is a bit of a misnomer. It describes 100 grams of sugar for \
every gram of salt. We just see a higher conncentration of the highest alcohol \
content wines around 0.3% sugar and 0.003% salt. We're not seeing any examples \
at 2% sugar and 0.02% salt. There is no diagonal line that would describe a \
perfect ratio.

To be more accurate, we should say that the highest alcohol content wines \
occur between 0.003% and 0.004% salt content and 0.1 to 0.75% sugar content.

```{r echo=FALSE}
ggplot(aes(y = sugar, x = salt, fill = value),
  data = wine.ratios) +
  geom_tile() +
  scale_fill_gradientn(colours = colorRampPalette(c("green","blue", "red"))(50)) +
  scale_y_continuous(limits = c(0,0.75)) + 
  scale_x_continuous(limits = c(0,0.006))
```

Zooming in on this range we can see that it isn't a true ratio. It's more of a \
happy spot where the balance between salt and sugar isn't too much in one \
direction or the other.

```{r echo=FALSE}
ggplot(aes(y = sugar, x = salt, fill = value),
  data = wine.ratios) +
  geom_tile() +
  scale_fill_gradient2(low = "white", mid = "blue", high = "black", 
                   midpoint = 11.5) +
  scale_y_continuous(limits = c(0,0.75)) + 
  scale_x_continuous(limits = c(0,0.006))
```

Focusing on one color centered close to the lower middle range of the highest \
alcohol content and gradiated between white to black provides a good contrast \
on what's happening in the happy spot. We can better see where there's \
not enough sugar for the amount of salt in that bright blue. Just above that \
spot, we see a higher distribution of higher alcohol content wines in the \
darker colors. As sugar and salt gets a little too high, the alcohol content \
starts to sharply drop. It happens more rapidly for salt concentration than \
sugar concentration.

```{r echo=FALSE}
ggplot(aes(y = sugar, x = salt, fill = value),
  data = wine.ratios) +
  geom_tile() +
  scale_fill_gradient2(low = "white", mid = "blue", high = "black", 
                   midpoint = 11.5) +
  scale_y_continuous(limits = c(0,2)) + 
  scale_x_continuous(limits = c(0,0.02))
```

Zooming back out with this color scale, it's easier to see the happy spot.  

This leaves the question of reds vs whites.  

```{r echo=FALSE}
ggplot(aes(y = sugar, x = salt, fill = value),
  data = subset(wine.ratios, wine.ratios$type == "red")) +
  geom_tile() +
  scale_fill_gradient2(low = "white", mid = "blue", high = "black", 
                   midpoint = 11.5) +
  scale_y_continuous(limits = c(0,2)) + 
  scale_x_continuous(limits = c(0,0.02))+
  geom_smooth(aes(color=type))
```

Red wine's contribution to the happy spot is clear and not unexpected.

```{r echo=FALSE}
ggplot(aes(y = sugar, x = salt, fill = value),
  data = subset(wine.ratios, wine.ratios$type == "white")) +
  geom_tile() +
  scale_fill_gradient2(low = "white", mid = "blue", high = "black", 
                   midpoint = 11.5) +
  scale_y_continuous(limits = c(0,2)) + 
  scale_x_continuous(limits = c(0,0.02))+
  geom_smooth(aes(color=type))
```

White wine's contribution to the happy spot is also quite clear. Although, \
white wine seems to be more forgiving on sugar content. Rather, white wines \
with high sugar content are fine. After an amount of salt, sugar becomes less \
acceptable.

```{r echo=FALSE}
wine.quality <- data.frame("sugar" = round(wines$residual.sugar, 2), 
                          "salt" = round(wines$chlorides, 4),
                          "quality" = as.numeric(wines$quality),
                          "type" = wines$color)
head(wine.quality)
```

```{r echo=FALSE}
wine.qratio <- melt(wine.quality, id.vars = c("sugar", "salt", "type"))
wine.qratio
```

```{r echo=FALSE}
ggplot(aes(y = sugar, x = salt, fill = value),
  data = wine.qratio) +
  geom_tile() +
  scale_fill_gradient2(low = "white", mid = "blue", high = "black", 
                       midpoint = 5) +
  scale_y_continuous(limits = c(0,2)) + 
  scale_x_continuous(limits = c(0,0.02))+
  geom_smooth(aes(color=type))
```  
  
  The relationship between salt, sugar and quality doesn't change much when \
  reverting back from alcohol content to quality scores. Although, granularity \
  is lost. This strengthens our assumption that alcohol content is a good \
  measure of quality.
  
# Multivariate Analysis

Based on what we've seen, salt content has more impact on wine \
quality than sugar. Even with sugar rich white wines, salt content is the largest \
determining factor. In white wines, you can have more sugar in a higher \
quality wine as long as the salt content remains in a decreasing range.

Between red and white wines, there is a convergence where wines of the highest \
alcohol content occurs with a balance of sugar and salt. This sweet spot begs \
a question of wine quality and how it relates to alcohol. Is alcohol content \
just a by product of the process used to balance sugar with salt? 

Alcohol content as a granular measure of quality is something that shouldn't \
escape scrutiny. In this analysis, alcohol content was taken as a rough model \
for quality. It offered a level of granularity not present in the quality \
scale. One issue with this is it may hide the relationship of other solutes in \
the solution and how the combination of those solutes relate to quality.

### Talk about some of the relationships you observed in this part of the \
investigation. Were there features that strengthened each other in terms of \
looking at your feature(s) of interest?

### Were there any interesting or surprising interactions between features?

### OPTIONAL: Did you create any models with your dataset? Discuss the \
strengths and limitations of your model.

------

# Final Plots and Summary

> **Tip**: You've done a lot of exploration and have built up an understanding
of the structure of and relationships between the variables in your dataset.
Here, you will select three plots from all of your previous exploration to
present here as a summary of some of your most interesting findings. Make sure
that you have refined your selected plots for good titling, axis labels (with
units), and good aesthetic choices (e.g. color, transparency). After each plot,
make sure you justify why you chose each plot by describing what it shows.

```{r echo=FALSE}
thm <- theme(plot.title = element_text(size = 16, face="bold"), 
            axis.title.x = element_text(size = 10, face="bold"),
            axis.title.y = element_text(size = 10, face="bold"),
            panel.background = element_rect(fill = "seashell3", color = "darkgrey"),
            panel.grid.major = element_line(size = .1, color = "seashell2", linetype = "dashed"),
            panel.grid.minor = element_line(size = .1, color = "grey", linetype = "dashed"),
            plot.background = element_rect(fill = "azure1"))
```

### Plot One
```{r echo=FALSE, Plot_One}
wines %>% 
  subset(alcohol <= 14.5) %>%
  ggplot(aes(x=quality, y=alcohol)) +
  geom_jitter(alpha=.4, shape = 21, fill = I('#2679af')) +
  stat_summary(fun.y = mean, fun.ymin = function(z){quantile(z, 0.25)}, 
               fun.ymax = function(z){quantile(z, 0.75)},
                 geom = "crossbar", width = 1, fill = '#f70800', alpha = .3) +
  scale_y_continuous(breaks = seq(8, 14, 1)) +
  labs(title="Alcohol Content as Quality", y="Percent Alcohol Content",
       x = "Average Quality Score") + thm


```

### Description One

This data set has an issue of granularity within the quality scale. Without a \
a greater level of granularity, the deliniation between good an bad quality \
wines is lost. Alcohol content was identified as a surrogate to quality. It \
offers a greater level of granularity.

This granularity of quality found in alcohol content is illustrated here. The \
exceptionally good and exceptionally bad wines have a lack of observation \
density to produce consistency with this assumption. However, on the \
observations we do have, we see the alcohol content means of lesser quality \
wines are much lower than higher quality wines. Through the middling quality \
wines, where the majority of our observations lie, this trend is more \
pronounced.

### Plot Two
```{r echo=FALSE, Plot_Two}
ggplot(data=subset(wines, chlorides < .025), 
       aes(x=alcohol, y=(chlorides*100))) +
  geom_jitter(alpha=.3, shape = 21, fill = I('#605f5d')) +
  scale_y_continuous(limits=c(0.2, 1.2),breaks = seq(0.2, 1.2, 0.2)) +
  geom_smooth(data = subset(wines, color=="red"), aes(color = "Red")) +
  geom_smooth(data = subset(wines, color=="white"), aes(color = "White")) + 
  scale_colour_manual(name="Varietal", values=c("#540000", "#d2e8a9")) +
  labs(title="Salt and Alcohol Content", 
       y="Salt (ppm)", x = "Alcohol (ABV)") +
  thm
```

### Description Two

Using alcohol as a granular measurement of quality revealed salt \
content as a major factor for determing wine quality. Across both varities we \
see that as alcohol content increases, salt content decreases. It becomes \
apparent that better wines have less salt.

The amount of salt in the wine samples is miniscule. Where alcohol can be \
measured in full percents by volume, salt is best described in parts per \
million. It is interesting that slight variation in a small amount can have \
such a great effect on quality.

We also start to see a divergence between the two main varietals of wine. Red \
wines tend to have almost twice the amount of salt of white wines. This \
suggests that quality is reliant on a combination of compounds.


### Plot Three
```{r echo=FALSE, Plot_Three}


ggplot(aes(y = sugar*100, x = salt*100),
  data = wine.ratios) +
  geom_raster(aes(fill=value),interpolate = TRUE) +
#  scale_fill_gradientn(colors = rainbow(50)) + #, start = .4)) + #, s = 1, v = .7)) +
#  scale_fill_gradientn(colors = colorRampPalette(c("lightgoldenrod", "red4","grey10"), bias = .9, alpha = TRUE)(200)) +
  scale_fill_gradientn(colors = brewer.pal(n = 5,name = "Greys")) +
  scale_y_continuous(limits = c(0,200)) + 
  scale_x_continuous(limits = c(0,1.5)) +  
  geom_smooth(data = subset(wine.ratios, type=="red"), aes(color = "Red")) +
  geom_smooth(data = subset(wine.ratios, type=="white"), aes(color = "White")) + 
  scale_colour_manual(name="Varietal", values=c("#540000", "#d2e8a9")) +
  labs(title="ABV Related to Salt and Sugar", y="Sugar (ppm)",
       x = "Salt (ppm)", fill = "ABV") +
  thm
```

### Description Three

We now start to see the relationship between combinations of compounds and \
quality. Also apparent are the differences and simularities between red and \
white wines. There's a convergence between both varietals for ratios of salt \
and sugar where the highest alcohol content occurs. This sweet spot for salt \
and sugar is represented in the darkened area of the graph.  

There's a range of salt that is acceptable for reds and whites. There's a \
similar range for sugar as well. The difference for varietals is which solute \
is more forgiving in quality. More salt is acceptable in red wines as long as \
it remains within a limitation of sugar. The inverse is true for white wines.  

------

# Reflection

One thing that strikes me about this data is how worthless the quality score \
is. Asking someone to rate something on a scale of one to whatever does offer \
some insight. The question here is, how many opinions using that scale is \
needed to get a usable granularity? It's a great starting point with limited \
use.  

Despite the limitations of quality score, the dataset does offer a depth of \
possibilities. Differences of composition between varietals absent of \
quality considerations is the top of my list. While alcohol content was \
chosen as a surrogate to quality, it still is a measure of alcohol content. It \
could be that alcohol is a good measure of quality. I would argue that the \
polled experts have a bias for alcohol content. What makes them experts and \
what criteria do they use in rating decisions?  

There's also many items noted in the initial pass of the data that wasn't \
explored further. These questions could be their

One compound I didn't explore and would in a future analysis are the acids. \
There's enough evidence to explore the relationship between citric acid, sugar \
and salt. There's also an expectation that Ph is influenced by the acidic \
compounds. Expectations should always be tested.  

At the end of it, the insight gleaned is something I look forward to testing. \
Next time I'm in the store for a bottle of wine, I'm going to use alcohol \
content as my primary deciding factor. It will be interesting how many bottles \
go through before it proves to be a bad metric.

> **Tip**: Here's the final step! Reflect on the exploration you performed and
the insights you found. What were some of the struggles that you went through?
What went well? What was surprising? Make sure you include an insight into
future work that could be done with the dataset.

> **Tip**: Don't forget to remove this, and the other **Tip** sections before
saving your final work and knitting the final report!