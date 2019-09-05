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

If you are still experiencing errors, please provide the head and tail of the stack dump and a dump of the environment you're using to grade.
_i.e._  

```{Python}
conda list --explicit > <env_dump_file>
```

### Understanding the Dataset

Add Dataset Summary

### Identify Outlier(s)

Eugene Lockhart was removed. Also removed, and not mentioned, were Robert Belfer and Sanjay Bhatnagar. The data for these entries is not sane. Their values appear to have been shifted.  

### Optimize Feature Selection/Engineering

Clarity of purpose for dropping the email statistics does not appear to have been communicated.
Explanation of feature selection process is unclear.  
_e.g._ Simplify with SelectKBest?  
[https://www.quora.com/How-do-I-properly-use-SelectKBest-GridSearchCV-and-cross-validation-in-the-sklearn-package-together](https://www.quora.com/How-do-I-properly-use-SelectKBest-GridSearchCV-and-cross-validation-in-the-sklearn-package-together)  
Explanation of scaled features missing.  

### Pick and Tune and Algorithm

No Items

### Validate and Evaluate

tester.py unable to run due to environmental issue noted above.  

### Revision Plan

Rework feature selection logic  
