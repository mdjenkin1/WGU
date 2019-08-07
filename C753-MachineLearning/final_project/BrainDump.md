# Machine Learning Final Project

## Brain Storming Session 1

What information is available to us?  
pulled in updated version of explore_enron_data.py  
Dataset contains 21 features across 146 people.
How many of those features are financial?
How many of those features are social?
What are some natural relationships of those features?
Where are there holes in the dataset?

The majority/entirety of social data is email based. 35 people do not have email addresses in the

```{Python}
In [90]: no_email = set()

In [91]: for x in enron_data:
    ...:     if enron_data[x]['email_address'] == 'NaN' : no_email.add(x)
    ...:

In [92]: no_email
Out[92]:
{'BADUM JAMES P',
 'BAXTER JOHN C',
 'BAZELIDES PHILIP J',
 'BELFER ROBERT',
 'BLAKE JR. NORMAN P',
 'CHAN RONNIE',
 'CLINE KENNETH W',
 'CUMBERLAND MICHAEL S',
 'DUNCAN JOHN H',
 'FUGH JOHN L',
 'GAHN ROBERT S',
 'GATHMANN WILLIAM D',
 'GILLIS JOHN',
 'GRAMM WENDY L',
 'GRAY RODNEY',
 'JAEDICKE ROBERT',
 'LEMAISTRE CHARLES',
 'LOCKHART EUGENE E',
 'LOWRY CHARLES P',
 'MENDELSOHN JOHN',
 'MEYER JEROME J',
 'NOLES JAMES L',
 'PEREIRA PAULO V. FERRAZ',
 'REYNOLDS LAWRENCE',
 'SAVAGE FRANK',
 'SULLIVAN-SHAKLOVITZ COLLEEN',
 'THE TRAVEL AGENCY IN THE PARK',
 'TOTAL',
 'URQUHART JOHN A',
 'WAKEHAM JOHN',
 'WALTERS GARETH W',
 'WHALEY DAVID A',
 'WINOKUR JR. HERBERT S',
 'WROBEL BRUCE',
 'YEAP SOON'}

In [93]: len(no_email)
Out[93]: 35

In [94]:
```
