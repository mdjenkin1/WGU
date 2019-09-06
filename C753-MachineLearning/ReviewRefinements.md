# Addressing Revision Requirements

## Initial Submission Revision

### Code improvements required

Specifics appear to follow in other rubric items.  

### poi_id.py Cannot Be Ran

The error message that triggered the stack trace is missing from this item.  
I am not able to troubleshoot your environment without an error message. Most likely there is a versioning mismatch.  
I have added a dump of my environment to ./submission/py27_env.txt. You can clone my environment by running:  

```{Python}
conda create --name <env> --file ./submission/py27_env.txt
```

If you are still experiencing errors, please provide the head and tail of the stack dump. A dump of the environment you're using to grade would also be of help.
_i.e._  

```{Python}
conda list --explicit > <env_dump_file>
```

### Understanding the Dataset

Dataset Summary has been added. Although, this has caused the section to go a little over the 2 paragraph recommended size.  

### Identify Outlier(s)

Eugene Lockhart was removed. Also removed, and not mentioned, were Robert Belfer and Sanjay Bhatnagar. The data for these entries is not sane. Their values appear to have been shifted.  

### Optimize Feature Selection/Engineering

~~Clarity of purpose for dropping the email statistics does not appear to have been communicated.~~
~~Explanation of feature selection process is unclear.~~  
_e.g._ Simplify with SelectKBest?  
[https://www.quora.com/How-do-I-properly-use-SelectKBest-GridSearchCV-and-cross-validation-in-the-sklearn-package-together](https://www.quora.com/How-do-I-properly-use-SelectKBest-GridSearchCV-and-cross-validation-in-the-sklearn-package-together)  
~~Explanation of scaled features missing.~~  

Clarification of initial feature selection process has been streamlined.  
Added information on manually scrubbed features.  
Included explanation of scaled features in classifier pipelines.  

### Pick and Tune and Algorithm

No Items

### Validate and Evaluate

~~tester.py unable to run due to environmental issue noted above.~~  

### Revision Plan

~~Rework feature selection logic~~  

## Second submission Revision

### Quality of Code

Enrich the report. Export PDF?  

### Optimize Feature Selection

Show impact of new feature on final model.  
Add plots and graphs of feature selection.  
Justify use of feature scaling  

### Second Pass Validate and Evaluate

~~Export the final model, not the grid search object.~~  

## Second Revision Plan

Add plots and graphs to illustrate feature selection.  
Engineer one new feature that will be considered in the feature selection.  
Add scaler justification.  
