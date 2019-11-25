# Udacity Data Visualizations Project Notes

Dataset study in tandem with course material.

## Airline Data

One of the suggested, intermediate, datasets is being used for this project. Specifically, historical flight data from RITA.

* [RITA](https://www.google.com/url?q=http://www.transtats.bts.gov/OT_Delay/OT_DelayCause1.asp&sa=D&ust=1554488156369000)
* [Flights](https://www.google.com/url?q=http://stat-computing.org/dataexpo/2009/the-data.html&sa=D&ust=1554488156368000)

## Data Investigation

Some investigation of the available fields prior to data loading.  

| Name| Description | Continuous</br>Discrete | Initial</br>Consideration |
|--|--|--|--|
| Year | 1987-2008 | Continuous | DateTime |
| Month | 1-12 | Continuous | DateTime |
| DayofMonth | 1-31 | Continuous | DateTime |
| DayOfWeek | 1 (Monday) - 7 (Sunday) | Continuous | DateTime |
| DepTime | actual departure time (local, hhmm) | Continuous | DateTime |
| CRSDepTime | scheduled departure time (local, hhmm) | Continuous | DateTime |
| ArrTime | actual arrival time (local, hhmm) | Continuous | DateTime |
| CRSArrTime | scheduled arrival time (local, hhmm) | Continuous | DateTime |
| UniqueCarrier | unique carrier code | Categorical | Flight Identifier |
| FlightNum | flight number | Categorical | Flight Identifier |
| TailNum | plane tail number | Categorical | Flight Identifier |
| ActualElapsedTime | in minutes |  Discrete | Flight Time |
| CRSElapsedTime | in minutes |  Discrete | Flight Time |
| AirTime | in minutes |  Discrete | Flight Time |
| ArrDelay | arrival delay, in minutes |  Discrete | Flight Time |
| DepDelay | departure delay, in minutes |  Discrete | Flight Time |
| Origin | origin IATA airport code | Categorical | Flight Identifier</br>Trip Detail |
| Dest | destination IATA airport code | Categorical | Flight Identifier</br>Trip Detail |
| Distance | in miles |  Discrete | Trip Detail |
| TaxiIn | taxi in time, in minutes |  Discrete | Flight Time |
| TaxiOut | taxi out time in minutes |  Discrete | Flight Time |
| Cancelled | was the flight cancelled? | Categorical | Trip Detail |
| CancellationCode | reason for cancellation</br>(A = carrier, B = weather, C = NAS, D = security) | Categorical | Trip Detail |
| Diverted | 1 = yes, 0 = no | Categorical | Trip Detail |
| CarrierDelay | in minutes |  Discrete | Attributed Delay Time |
| WeatherDelay | in minutes |  Discrete | Attributed Delay Time |
| NASDelay | in minutes |  Discrete | Attributed Delay Time |
| SecurityDelay | in minutes |  Discrete | Attributed Delay Time |
| LateAircraftDelay | in minutes |  Discrete | Attributed Delay Time |

### Question Brainstorming

Does when a flight happen have any indication of anything?
What flights do/do not cross time zones?  
For similar flights, is there a difference between seasons, months, day of week, time of day?  
What makes for a similar flight?  
What information is encoded with tail numbers?  
What information is encoded with flight numbers?  
Does the direction of travel have any impact?  
How does direction of travel compare to travel distance?  
How do taxi times compare for origin airports?  
How do origin airports compare for departure time vs scheduled departure time?  
Is there a misjudged component of travel time that could be better calculated to determine proper float for accurate scheduled arrival?  
Are the attributed delay times calculated, derived or manually collected?  
How do attributed delay times factor into total travel time?  
What are the date/time relations to delay times?  

### Project Scoping

The primary goal of the course appears to be understanding the available functionality of Tableau. Data visualization and communication of data exploration appears to be secondary. Therefore the scope of this project will be directed to the capabilities of Tableau.  

## Loading Dataset

[https://kb.tableau.com/articles/howto/connecting-multiple-data-sources-without-joining-or-blending](https://kb.tableau.com/articles/howto/connecting-multiple-data-sources-without-joining-or-blending)  

Apparent options:  

* Load each csv as an individual data source
* Union each csv to a singular data source

Decision was to union. This resulted in a dataset of 123,534,969 rows. This is well in excess of the 15,000,000 row limit of Tableau. Saving is not available.  

## Transforming Dataset

From talking to others about the dataset and the goals of this project, I decided to limit this investigation to the number of take-offs and delays for each airport. Investigating a possible relationship between number of flights in/out of an airport and how many of them are delayed. It's my assumption that the ratio of delayed flights to total flights is relatively equal across all airports.

Before starting this investigation, I need to reduce the number of records to something Tableau can handle. To aid in this investigation, I've started a python script "csv_investigate.py"

My first thought was to select a handful of the busiest airports. A quick parse of the data shows this isn't going to be tenable. Over the 22 years of data, Orlando has had the most departing flights at 6.6 million and Atlanta had 6.1 million. Between these two airports, that leaves little more than 2.3 million records before hitting Tableau's limits. That's not enough for the next largest airport, Dallas Fort Worth, let alone inbound flights.  

My next thought is to compare the growth in airport capacity/flow for two airports. In this case Salt Lake City and Orlando. Salt Lake City is the airport I've most commonly used and Orlando is the busiest. Even this is too much for Tableau.  

It seems the best option would be to focus on one airport. Orlando has the most traffic, so it will be our pick. With a little bit of Python, all rows containing traffic into and out of Orlando has been extracted and compiled to one csv. In total, there's 13.2 million rows across the 22 years. Still a sizeable dataset, but not too big for Tableau.  

```{python}
(py37) C:\Users\Michael\Documents\WGU\WGU-Projects\C939-DataVisualization>python csv_investigate.py
         Year  Month  DayofMonth  DayOfWeek  DepTime  CRSDepTime  ArrTime  CRSArrTime  ... Cancelled  CancellationCode Diverted  CarrierDelay  WeatherDelay  NASDelay  SecurityDelay  LateAircraftDelay
14659    1987     10           1          4   1803.0        1800   1942.0        1915  ...         0               NaN        0           NaN           NaN       NaN            NaN                NaN
14660    1987     10           2          5   1801.0        1800   1915.0        1915  ...         0               NaN        0           NaN           NaN       NaN            NaN                NaN
14661    1987     10           5          1   1802.0        1800   1916.0        1915  ...         0               NaN        0           NaN           NaN       NaN            NaN                NaN
14662    1987     10           7          3   1800.0        1800   1921.0        1915  ...         0               NaN        0           NaN           NaN       NaN            NaN                NaN
14663    1987     10           8          4   1810.0        1800   1930.0        1915  ...         0               NaN        0           NaN           NaN       NaN            NaN                NaN
...       ...    ...         ...        ...      ...         ...      ...         ...  ...       ...               ...      ...           ...           ...       ...            ...                ...
7008446  2008     12          12          5    724.0         725   1018.0         956  ...         0               NaN        0           0.0           0.0      22.0            0.0                0.0
7008484  2008     12          12          5   1619.0        1624   1854.0        1854  ...         0               NaN        0           NaN           NaN       NaN            NaN                NaN
7008628  2008     12          12          5   1727.0        1650   2123.0        2054  ...         0               NaN        0           0.0           0.0       0.0            0.0               29.0
7009156  2008     12          13          6    951.0         955   1112.0        1112  ...         0               NaN        0           NaN           NaN       NaN            NaN                NaN
7009450  2008     12          13          6    714.0         715    944.0        1005  ...         0               NaN        0           NaN           NaN       NaN            NaN                NaN

[13235476 rows x 29 columns]
               Year         Month    DayofMonth     DayOfWeek       DepTime    CRSDepTime  ...      Diverted  CarrierDelay  WeatherDelay      NASDelay  SecurityDelay  LateAircraftDelay
count  1.323548e+07  1.323548e+07  1.323548e+07  1.323548e+07  1.282051e+07  1.323548e+07  ...  1.323548e+07  3.561521e+06  3.561521e+06  3.561521e+06   3.561521e+06       3.561521e+06
mean   1.998553e+03  6.552078e+00  1.571906e+01  3.934180e+00  1.323559e+03  1.293060e+03  ...  2.442602e-03  4.115982e+00  8.486082e-01  7.647379e+00   1.104528e-02       7.382481e+00
std    6.141658e+00  3.440199e+00  8.785181e+00  1.988582e+00  4.687764e+02  4.811744e+02  ...  4.936229e-02  2.099290e+01  9.644373e+00  2.538340e+01   8.828610e-01       2.585451e+01
min    1.987000e+03  1.000000e+00  1.000000e+00  1.000000e+00  1.000000e+00  0.000000e+00  ...  0.000000e+00  0.000000e+00  0.000000e+00  0.000000e+00   0.000000e+00       0.000000e+00
25%    1.993000e+03  4.000000e+00  8.000000e+00  2.000000e+00  9.250000e+02  9.070000e+02  ...  0.000000e+00  0.000000e+00  0.000000e+00  0.000000e+00   0.000000e+00       0.000000e+00
50%    1.999000e+03  7.000000e+00  1.600000e+01  4.000000e+00  1.320000e+03  1.310000e+03  ...  0.000000e+00  0.000000e+00  0.000000e+00  0.000000e+00   0.000000e+00       0.000000e+00
75%    2.004000e+03  1.000000e+01  2.300000e+01  6.000000e+00  1.715000e+03  1.700000e+03  ...  0.000000e+00  0.000000e+00  0.000000e+00  0.000000e+00   0.000000e+00       0.000000e+00
max    2.008000e+03  1.200000e+01  3.100000e+01  7.000000e+00  2.430000e+03  2.359000e+03  ...  1.000000e+00  1.393000e+03  1.352000e+03  1.359000e+03   3.820000e+02       1.280000e+03

[8 rows x 24 columns]

(py37) C:\Users\Michael\Documents\WGU\WGU-Projects\C939-DataVisualization>
```

### Data Cleaning in Tableau

After loading the dataset to Tableau, it became apparent that it would be necessary to prepare the fields. For instance, the dates are split and the times are integers that have been converted to doubles.  

For the dates, I concatenated the year, month and day of month fields into a string that was then converted into a date. Starting on the times is when trouble began. Every attempt at correcting a time field resulted in longer and longer processing time until the program eventually hung. So back to Python to further clean and prepare the dataset.  

With the size of Orlando's data causing trouble for Tableau, I fell back to a smaller airport, SLC. Tableau does appear to be a powerful exploration tool, but it is limited in the size of data it can handle. It also appears to have some memory leaks that are exacerbated by data size.

### Cleaning Data outside of Tableau

These limitations of Tableau prompted a need for more power to clean the dataset. It's for this reason, the lion's share of data preprocessing has been moved to Python. In python, the date parts were concatenated into a date; scheduled time features were converted from numbers to times; and time measurements were transformed to timedeltas.  

```{python}
        ActualElapsedTime          AirTime          ArrDelay   ArrTime  ArriveDate CRSArrTime CRSDepTime CRSElapsedTime CancellationCode  Cancelled  ... FlightNum  LateAircraftDelay         NASDelay Origin    SecurityDelay TailNum           TaxiIn          TaxiOut  UniqueCarrier     WeatherDelay
18149            02:47:00             None          00:06:00  19:20:00  1987-10-01   19:14:00   15:35:00       02:39:00              NaN          0  ...       190               None             None    SLC             None     NaN             None             None             TW             None
18150            02:52:00             None          00:12:00  19:26:00  1987-10-02   19:14:00   15:35:00       02:39:00              NaN          0  ...       190               None             None    SLC             None     NaN             None             None             TW             None
18151            02:51:00             None          00:10:00  19:24:00  1987-10-03   19:14:00   15:35:00       02:39:00              NaN          0  ...       190               None             None    SLC             None     NaN             None             None             TW             None
18152            02:49:00             None          00:09:00  19:23:00  1987-10-04   19:14:00   15:35:00       02:39:00              NaN          0  ...       190               None             None    SLC             None     NaN             None             None             TW             None
18153            02:38:00             None -1 days +23:57:00  19:11:00  1987-10-05   19:14:00   15:35:00       02:39:00              NaN          0  ...       190               None             None    SLC             None     NaN             None             None             TW             None
...                   ...              ...               ...       ...         ...        ...        ...            ...              ...        ...  ...       ...                ...              ...    ...              ...     ...              ...              ...            ...              ...
7009682          01:14:00  0 days 00:58:00          00:02:00  08:54:00  2008-12-13   08:52:00   07:40:00       01:12:00              NaN          0  ...      1585                NaT              NaT    BOI              NaT  N376DA  0 days 00:06:00  0 days 00:10:00             DL              NaT
7009683          01:27:00  0 days 00:50:00          00:24:00  21:33:00  2008-12-13   21:09:00   19:54:00       01:15:00              NaN          0  ...      1586    0 days 00:12:00  0 days 00:12:00    SLC  0 days 00:00:00  N3735D  0 days 00:04:00  0 days 00:33:00             DL  0 days 00:00:00
7009701          01:52:00  0 days 01:19:00          00:38:00  17:20:00  2008-12-13   16:42:00   15:00:00       01:42:00              NaN          0  ...      1611    0 days 00:12:00  0 days 00:10:00    SLC  0 days 00:00:00  N395DN  0 days 00:04:00  0 days 00:29:00             DL  0 days 00:00:00
7009712          01:45:00  0 days 00:53:00          00:04:00  10:25:00  2008-12-13   10:21:00   08:43:00       01:38:00              NaN          0  ...      1624                NaT              NaT    SLC              NaT  N3738B  0 days 00:06:00  0 days 00:46:00             DL              NaT
7009721          02:11:00  0 days 01:43:00          00:16:00  09:23:00  2008-12-13   09:07:00   06:15:00       01:52:00              NaN          0  ...      1635    0 days 00:00:00  0 days 00:16:00    GEG  0 days 00:00:00  N907DA  0 days 00:05:00  0 days 00:23:00             DL  0 days 00:00:00

[4007604 rows x 28 columns]
            ActualElapsedTime                ArrDelay          CRSElapsedTime     Cancelled     DayOfWeek                DepDelay      Distance      Diverted     FlightNum
count                 3957451                 3957451                 4007488  4.007604e+06  4.007604e+06                 3963674  3.982811e+06  4.007604e+06  4.007604e+06
mean   0 days 02:01:35.277025  0 days 00:05:40.060756  0 days 02:02:23.934344  1.097339e-02  3.979958e+00  0 days 00:06:36.422753  7.315265e+02  1.541070e-03  1.952975e+03
std    0 days 00:59:38.948831  0 days 00:26:39.607207  0 days 00:58:47.248000  1.041776e-01  1.997685e+00  0 days 00:27:27.514608  4.685312e+02  3.922621e-02  1.371341e+03
min         -1 days +12:30:00       -1 days +08:10:00       -1 days +23:34:00  0.000000e+00  1.000000e+00       -1 days +04:11:00  2.800000e+01  0.000000e+00  3.000000e+00
25%           0 days 01:22:00       -1 days +23:53:00         0 days 01:23:00  0.000000e+00  2.000000e+00       -1 days +23:58:00  4.020000e+02  0.000000e+00  9.710000e+02
50%           0 days 01:41:00         0 days 00:00:00         0 days 01:42:00  0.000000e+00  4.000000e+00         0 days 00:00:00  5.880000e+02  0.000000e+00  1.618000e+03
75%           0 days 02:29:00         0 days 00:10:00         0 days 02:30:00  0.000000e+00  6.000000e+00         0 days 00:05:00  9.880000e+02  0.000000e+00  2.816000e+03
max           1 days 05:19:00         0 days 23:55:00         0 days 09:25:00  1.000000e+00  7.000000e+00         0 days 23:59:00  2.994000e+03  1.000000e+00  9.604000e+03
```

There's some gaps in the dataset, but it should be good enough for our purposes. Time to go back to Tableau.

There's some new problems loading to Tableau that need addressing. Times and dates should be combined and Tableau doesn't handle time deltas. To complicate matters, on reloading the preprocessed csv a mixed type warning is received for a number of columns.  

```{python}
sys:1: DtypeWarning: Columns (2,9,11,20,21,23,24,25,26,28) have mixed types. Specify dtype option on import or set low_memory=False.
Index(['Unnamed: 0', 'ActualElapsedTime', 'AirTime', 'ArrDelay', 'ArrTime',
       'ArriveDate', 'CRSArrTime', 'CRSDepTime', 'CRSElapsedTime',
       'CancellationCode', 'Cancelled', 'CarrierDelay', 'DayOfWeek',
       'DepDelay', 'DepTime', 'DepartDate', 'Dest', 'Distance', 'Diverted',
       'FlightNum', 'LateAircraftDelay', 'NASDelay', 'Origin', 'SecurityDelay',
       'TailNum', 'TaxiIn', 'TaxiOut', 'UniqueCarrier', 'WeatherDelay'],
      dtype='object')
```

A closer inspection of this Dtypewarning shows it's nothing to be concerned with. The columns with mixed data types have a mix of NaN and actual values. I expect the missing values for AirTime can be calculated. Others are most likely values that just weren't captured. Seems some data sanity checks are in order.  

### A whole new direction

After troubleshooting validations and a code refactor, it seems a large number of the 'NaN' being introduced to my dataset is due to a regressive bug in pandas. The behavior closely resembles what is described here: [https://github.com/pandas-dev/pandas/issues/18775](https://github.com/pandas-dev/pandas/issues/18775). A major difference is that bug report specifies lambda returning a datetime field. I've recreated the bug with lambda returning afield of type 'object'. After searching for a workaround to this bug, I decided the best course of action would be to abandon pandas for cleaning this dataset and doing it the old fashioned way, while file each line like it's 1999. Once I have more time, I'll dig more into the bug reports and ensure there's a path to resolution on this.  

During this iteration of preprocessing, I added some carrier code processing. Greater depth of carrier codes were obtained from [http://stat-computing.org/dataexpo/2009/carriers.csv](http://stat-computing.org/dataexpo/2009/carriers.csv). Also available is airline data: [http://stat-computing.org/dataexpo/2009/airports.csv](http://stat-computing.org/dataexpo/2009/airports.csv). This information was also incorporated into the preprocessing script. With this additional information, it is possible to add direction of travel as a feature to our dataset. [https://www.movable-type.co.uk/scripts/latlong.html](https://www.movable-type.co.uk/scripts/latlong.html).  

$$\Theta = \arctan2(sin \Delta\lambda \times \cos\phi_2, \cos\phi_1 \times \sin\phi_2 - \sin\phi_1 \times \cos\phi_2 \times \cos \Delta\lambda)$$  

We can also use the 'Haversine' formula to find the shortest distance. There's potentially a discrepancy between the reported distance and calculated distance. It's possible the direction of travel is opposite the calculated shortest distance.  

$$a = \sin^2({\Delta\phi\over2}) + \cos\phi_1 \times \cos\phi_2 \times \sin^2({\Delta\lambda\over2})$$
$$c = 2 \times \arctan2(\sqrt{a}, \sqrt{(1-a)})$$
$$d = R \times c$$  

Another option for calculating distance presented to us is the Spherical Law of Cosines. Which is much simpler formula, although it has slower performance  

$$d = \arccos(\sin \phi_1 \times \sin \phi_2 + \cos \phi_1 \times \cos \phi_2 \times \cos\Delta\phi) \times R$$  

For all formulas:

* $R$: Radius of the earth ($6,371 km \approx 3959miles$)
* $\phi$: Latitude
* $\lambda$: Longitude
* $(\phi_1, \lambda_1)$: Origin
* $(\phi_2, \lambda_2)$: Destination

For the sake of performance, there's no reason to calculate distance and direction for each row in our dataset. Each origin, destination set should have the same distance and direction. This should also help simplify validation of the distance feature in our flight data. Should the same origin, destination flight have a wildly different distance, then that's something that should be investigated.  

#### Converting a degree heading into a compass direction

This solution exists on a number of websites.  
[https://www.campbellsci.com/blog/convert-wind-directions](https://www.campbellsci.com/blog/convert-wind-directions)  
[https://stackoverflow.com/questions/7490660/converting-wind-direction-in-angles-to-text-words](https://stackoverflow.com/questions/7490660/converting-wind-direction-in-angles-to-text-words)  

while heading angles are useful for their exact description of travel; they're not very helpful when talking to your average person. So it would be best to convert these angles into a natural language direction. There's a number of solutions to this problem on the internet. The most common is a variation of the same theme. This is my explanation of the most common solution.  

The number of points on our compass is arbitrary. Given functional logic, any number of desired points should result in proper direction resolution. Starting most simply would be 2 points on the compass North and South.  

Degrees can range from -360 to 360. It's possible that a larger degree is supplied, but a modulo 360 will return the degree between our stated range. Further, Python's modulo operator will always return a number that agrees in sign with the denominator. This simplifies the logic further by always having a heading degree range of 0 inclusive and 360 exclusive.  

The arcs for each point on our compass are equal. In the case of a "North,
 South" compass, the arc for each direction is 180 degrees. Exact North has a heading of 0 degrees and exact South has a heading of 180 degrees. Everything else in the arc ranges can be described as more North than South or more South than North. There is the exception of the boundaries between the two arcs. At exactly 90 degrees and 270 degrees, the direction cannot be described as more Northerly or Southerly.

Dividing the heading degree by the directional arc size will return a number between 0 inclusive and N exclusive where N is the number of directions. The split between each directional arc happens at some fractional value between each whole number.  

For our compass consisting of just North and South, the splits happen at 90 and 270 degrees. With N = 2, our arc size is 180.  
Treating our splits as the headings to convert, we get 0.5 and 1.5 for arc direction boundaries.

It's at this point in the solution an earlier assumption we made about "an arbitrary number of points" is betrayed. The commonly found solution relies on rounding rules to assign the degree to the correct arc. Rounding rules only work for this purpose if the number of points in our compass is a multiple of 2.  

Another earlier statement we made can also be modified. It is not necessary to take the initial modulo of the supplied heading as we have to take the modulo of the resulting rounding. After rounding we'll have N+1 possible integers ranging from 0 to N. If we skip the initial modulo we'll have xN+1 possible integers ranging from 0 to xN. Either way, taking the modulo N of the resulting rounding, we'll have N possible integers ranging from 0 to N-1. The same range as the index of our compass point name list. At this point, we just use the index to retrieve and return the compass point.  

To sum up the compass point calculation.  

It is possible to determine the direction of travel for a degree heading using an ordered list of compass points. The ordered list must contain a multiple of 2 number of points in clockwise order. This method will return the index of the named arc within that ordered list.  

##### Given

> Heading (in degrees): $\phi$  
> Ordered list of points: $P$  
> Length of list $P$: $P.len$  
> Arc size of each direction: $360 \over P.len$  
> Index of direction in list: $I$  

##### Return Direction

> If $P.Len  \%  2 == 0$  
> ${\phi \times P.len \over 360}$ will produce a fraction of the compass as a multiple of $P.len$  
> $round({\phi \times P.len \over 360})$ will return an integer value $x \times P.len + I$  
> $round({\phi \times P.len \over 360}) \% P.len$ will return $I$  

One consideration not addressed here is the accuracy of floating point calculations, rounding and integer calculations. For our purpose, this is not a concern. Close is good enough for this art project.  

#### Validations

Calculated distances were rounded. There's no logic in comparing floats to integers for accuracy. For our development dataset, the difference between calculated and reported distances ranges from 0 to 5 miles. This is an acceptable range that can be attributed to differences in calculation method.  

For directions and headings, a handful of flight paths were randomly selected and manually compared to an actual map. In each case, the determined direction matched what was seen on a map.  

### Revisiting Dates

All that should be left of preprocessing are the date and time fields that originally threw us down this preprocessing path. Converting our date time functions from pandas to file stream processing shouldn't be too difficult.  

One refinement is including day of the week as named days instead of numbers. The source dataset provides day of the week as ISO defined numbers (Monday = 1). This can also be determined after the time parts are reassembled into an actual date. This provides an additional opportunity for data validation.  

### Wrapping up Preprocessing

Having added the final fields to the data preprocessing scripts, the remainder of the raw data was queued for preprocessing. This is when some new anomalies were discovered.

```{python}
processing 2003.csv
row: 1928155
TimeField: ArrTime
rawTime: 2524
tmpTime: {'Hour': 25, 'Min': 24}
```

The hour and minute time split appears to be good. However, an arrival time greater than 2400 suggests this may be a calculated instead of recorded field. The thought that it's a recorded field was an assumption. Rather than working with assumed data definitions, it would be better to refer to the glossary.  

[https://www.transtats.bts.gov/glossary.asp](https://www.transtats.bts.gov/glossary.asp)  

With the glossary open, it's also good chance to review some time and scheduling fields.  

| Name| Summary | Description |
|--|--|--|
| CRSArrTime | scheduled arrival time (local, hhmm) |  |
| CRSDepTime | scheduled departure time (local, hhmm) |  |
| CRSElapsedTime | in minutes | The time difference between</br>CRSArrTime and CRSDepTime |
| DepTime | actual departure time (local, hhmm) | Parking Break Released |
| TaxiOut | taxi out time in minutes | Minutes between</br>Leaving Gate</br>Wheels off Ground |
| AirTime | in minutes | Minutes between</br>Wheels off Ground</br>Wheels on Ground |
| TaxiIn | taxi in time, in minutes | Minutes between</br>Wheels on Ground</br>Arrival at Gate |
| ArrTime | actual arrival time (local, hhmm) | Arrived at gate</br>Set Parking Break |
| ActualElapsedTime | in minutes | ArrTime minus DepTime</br>TaxiOut + AirTime + TaxiIn |
| ArrDelay | arrival delay</br>in minutes</br>Flight is On time if this is less than 15 min | Difference between</br>ArrTime and CRSArrTime |
| DepDelay | departure delay</br>in minutes | Difference between</br>DepTime and CRSDepTime |

So let's take a closer look at what's going on with this record.  

```{python}
OrderedDict([('Year', '2003'),
             ('Month', '4'),
             ('DayofMonth', '27'),
             ('DayOfWeek', '7'),
             ('DepTime', '2430'),
             ('CRSDepTime', '2215'),
             ('ArrTime', '2524'),
             ('CRSArrTime', '2301'),
             ('UniqueCarrier', 'EV'),
             ('FlightNum', '4191'),
             ('TailNum', 'N713EV'),
             ('ActualElapsedTime', '114'),
             ('CRSElapsedTime', '106'),
             ('AirTime', '-1353'),
             ('ArrDelay', '143'),
             ('DepDelay', '135'),
             ('Origin', 'SLC'),
             ('Dest', 'ONT'),
             ('Distance', '558'),
             ('TaxiIn', '1449'),
             ('TaxiOut', '18'),
             ('Cancelled', '0'),
             ('CancellationCode', 'NA'),
             ('Diverted', '0'),
             ('CarrierDelay', 'NA'),
             ('WeatherDelay', 'NA'),
             ('NASDelay', 'NA'),
             ('SecurityDelay', 'NA'),
             ('LateAircraftDelay', 'NA')])
```

Looking at the scheduled and actual depart times, it seems the recorded time was a method of illustrating arrival happening after midnight. However, there's a number of other oddities in this record. Negative time in the air? More than a day to taxi from landing to the gate?  

Converting the times from HHMM to MinuteOfDay (1440 minutes in a day) shows a gate to gate time of 54 minutes. This doesn't match the recorded 114 Elapsed Time. For scheduled flight time, the 46 minutes doesn't match the reported 106 minutes. Both are off by 60 minutes. Direction of travel is southwest and a map check shows a flight takes approximately 1hr 45min. This suggests the missing hour is from a change in timezone. Flying west agrees with this. The origin is MST and the destination is PST. Clearly a calculation of local times. Time differences should be addressed for the various flights. A possible solution would be to maintain UTC time calculations.  

The negative airtime is something else to consider. With 1440 minutes in a day and the AirTime/TaxiIn times falling on either side of this number, it seems this record has added and subtracted a day. I suspect what happened is the scheduled arrival and departure was for the same day and near midnight. However the flight didn't happen until after midnight. If the recorded departure date was accurate but the scheduled arrival date was recorded as the actual arrival, then this could introduce a miscalculation when determining flight time. Correcting this record gives an air time of 87 minutes. Looking at some air times for SLC to ONT, this is reasonable. What isn't reasonable are air times in the 180 minute range with elapsed times closer to 100 min.  

With these inaccuracies, it will be necessary to redesign the logic used to prepare the date time information. Based on the investigation so far, scheduled information should be considered valid. Actual times should be held in question of arrival and depart delay times. Provided dates considered as scheduled depart dates. Seconds since the epoch seems to be Python's implemented solution to Datetime since 3.3. Working with epoch time should make this easier and cleaner.  
