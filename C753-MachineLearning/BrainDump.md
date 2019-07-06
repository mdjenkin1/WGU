# Brain Dump and Development Documentation

To complete this project I'll need to answer a series of questions.  

* What is the goal?
* What features were used and why?
* Which algorithms were tried?
* How was the algorithm tuned?
* How was the analysis validated?
* Generate and evaluate metrics.

In my experience, each company has their own vocabulary. Each group within that company has their own dialect of that vocabulary. It would follow the clique committing fraud would have their own dialect. The goal of our machine learner is to identify this dialect. This dialect can then be used to identify potential people of interest.  

The dataset features targeted by this learning goal would be the bodies of the emails. Without an external corpus, it would be difficult to determine a company wide common vocabulary. Such a determination would only be useful if we needed to identify an Enron employee from a non-employee. We already know everyone in our dataset is an employee. Instead, finding separate dialects within the emails will be our focus.  

We're seeking to split the corpus into two dialects. One used by POI and the other used by non-POI. To process the email data, I would first split them into two groups. One for POI and the other for non-POI. The POI group I would split into training and validation sets. The non-POI group would be split into three groups. One for training, a second for validation and a third for identification.  

With the data set split into training, validation, and identification sets, it's time to determine which algorithm to use to train our learner. One option is to use the TextBlob module for each email sender. For each sender, create a wordblob comprised of all emails they composed. Remove the stop words and generate a frequency count for each sender's word blob. Using the average frequency values for POI, we can use Naive Bayes to generate a probability for email matches the vocabularies of POI and test against the unknown POI dataset. Further direction is contingent on the outcome of this test.  
