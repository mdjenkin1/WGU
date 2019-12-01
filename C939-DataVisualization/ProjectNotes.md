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

With these inaccuracies, it will be necessary to redesign the logic used to prepare the date time information. Based on the investigation so far, scheduled information should be considered valid. Actual times should be held in question of arrival and depart delay times. Provided dates considered as scheduled depart dates. Seconds since the epoch seems to be Python's implemented solution to Datetime since 3.3. Working with epoch time should make this easier.  

### Restructing Time

Local timezone information is nowhere in our dataset. Luckily, a quick search turned up [https://pypi.org/project/timezonefinder/](https://pypi.org/project/timezonefinder/). We do have longitude and latitude data. So now it's just a matter of storing timezone information in a useful format.  

Digging deeper into the datetime and timezone solutions for python returned quite a selection. For determining timezones on a map, timezonefinder and tzwhere. Despite it's apparent popularity, tzwhere seems to be a stagnant project and timezonefinder has been updated recently.  

#### Lost at Sea

```{cmd}
Null timezone at airport FAQ Long: -169.4239058 Lat: 14.21577583
Null timezone at airport GRO Long: -145.2425353 Lat: 14.1743075
Null timezone at airport GSN Long: -145.7293561 Lat: 15.11900139
Null timezone at airport GUM Long: -144.7959825 Lat: 13.48345
Null timezone at airport PPG Long: -170.7105258 Lat: 14.33102278
Null timezone at airport TNI Long: -145.6180383 Lat: 14.99685028
Null timezone at airport TT01 Long: -145.7686111 Lat: 18.12444444
Null timezone at airport Z08 Long: -169.6700236 Lat: 14.18435056
```

After integrating timezonefinder to provide timezones, it introduced a new problem. It seems it cannot correctly provide timezones for islands in the middle of the Pacific ocean. To compensate for this, I attempted to lean on tzwhere. That package failed to install. It seems Anaconda doesn't provide for it in the default libraries and pip has it listed with a broken dependency chain. Taking another look at the timezonefinder page on pypi.org, ocean data has been excluded from the current dataset.  

The information on timezonefinder's project page, there's no simple drop in replacement for replacing the data set with ocean aware information. My solution will be to manually assign the timezone for these eight airports. Given the scope of the project and the need for these airports, this is an acceptable manual process. It will also give me the chance of addressing any issue with the TT01 and Z08 airports. One of these has too many characters for an IATA code and both of them have non-letter characters.  

| Code | Detail | Olsen tz |
|--|--|--|
| TT01 | Pagan Airstrip</br>Pagan Island</br>No IATA number | Pacific/Saipan |
| GRO | Rota Island | Pacific/Saipan |
| GSN | Saipan International | Pacific/Saipan |
| GUM | Guam International | Pacific/Saipan |
| TNI | West Tinian | Pacific/Saipan |
| Z08 | Ofu Village Airport</br>No IATA number | Pacific/Samoa |
| PPG | Pago Pago International | Pacific/Samoa |
| FAQ | Fitiuta Village | Pacific/Samoa |

#### Save the dates

For timezone aware datetimes, there's no shortage of options. A bit of searching turned up, datetime with pytz, arrow, pendulum, delorean and udatetime. Scratching the surface of those uncovered ciso8601 and mxDateTime.

Pendulum's latest release is from october of last year.  
Delorean's last merge is also from last year. They released v1.0 and dropped Python 2 support.  
Pytz had a release just last month and has had consistent updates.  
Udatetime has some impressive benchmarks, but development of it has slowed. The last release was almost 2 years ago.  
ciso8601 has had a slow release schedule but was updated last month for python 3.8 support.  
MxDateTime looks to be an opensource pet project that someone tried to monetize. It doesn't even list python 3.  

It seems that, despite all the options, there's really only datetime with pytz.  

### Assumed Good Times

A straight translation of times isn't going to be possible. Instead, I'll need to take a tested assumption approach. The place to start would be the scheduled timestamps.  

Starting with flight scheduling, the provided date is assumed to be scheduled departure date. Scheduled departure and arrival times will need to be converted to UTC. With both times in UTC the scheduled elapsed time can be calculated and compared. If the calculated elapsed time matches the scheduled elapsed time, then confidence in the reported scheduled times should be increased.  

These assumptions seem to be dead on. Calculated and provided elapsed times are in perfect agreement. Where they differ appears to be where daylight savings time is a possible factor. In these cases, the times are off by an hour. This can be accounted for by the ambiguous times introduced by daylight savings time. In these cases, the provided elapsed times can be used to flag the record as needing extra attention. This can help us address ambiguities of daylight savings time.  

```{python}
Ending daylight savings
Flying from LAS to SLC
local depart time: 2003-10-26 22:15:00-08:00 Timezone: America/Los_Angeles
local arrive time: 2003-10-26 00:30:00-06:00 Timezone: America/Denver
depart time UTC: 2003-10-27 06:15:00+00:00
arrive time UTC: 2003-10-27 06:30:00+00:00
Calculated scheduled elapsed time: 0:15:00
Provided scheduled elapsed time: 1:15:00
```

#### Ambiguities of DST

[https://en.wikipedia.org/wiki/Daylight_saving_time_in_the_United_States](https://en.wikipedia.org/wiki/Daylight_saving_time_in_the_United_States)  

For timezones affected by daylight savings time, twice a year, time keeping stops being continuous.  

At the start of daylight savings, the clock rolls over from 00:59 to 02:00. If a flight begins before the roll over and lands after the rollover, an additional hour may be aded to the flight time. This is what we see in the following example. The flight took off before the DST "spring forward" event and landed afterwards. The earlier arrival time on same day in this output is a result of date determination. Next day determination occurs after the converstion to UTC.  

```{cmd}
Nearing daylight savings
Flying from SLC to ATL
local depart time: 2003-04-05 22:55:00-07:00 Timezone: America/Denver
local arrive time: 2003-04-05 05:20:00-05:00 Timezone: America/New_York
depart time UTC: 2003-04-06 05:55:00+00:00
arrive time UTC: 2003-04-06 10:20:00+00:00
Calculated scheduled elapsed time: 4:25:00
Provided scheduled elapsed time: 3:25:00
```

```{cmd}
Nearing daylight savings
Flying from SLC to TUL
local depart time: 2003-04-06 20:50:00-06:00 Timezone: America/Denver
local arrive time: 2003-04-06 00:08:00-06:00 Timezone: America/Chicago
depart time UTC: 2003-04-07 02:50:00+00:00
arrive time UTC: 2003-04-07 06:08:00+00:00
Calculated scheduled elapsed time: 3:18:00
Provided scheduled elapsed time: 2:18:00
```

Another, related issue, is observed when pytz applies a non-DST timestamp to a DST time. This also appears to be an artifact of order of date determination. Rather than trying to determine how to correct these errors after the fact, it would be better try to prevent the error and then re-evaluate.  

One thing to be aware of is the loss of time by traveling West. It is not so straight forward to say "next day" arrival if the arrival time is earlier than the depart time. With a high confidence in the provided scheduled elapsed time, we can improve the logic to determine next day arrival.  

[http://www.physicalgeography.net/fundamentals/2c.html](http://www.physicalgeography.net/fundamentals/2c.html)  

For next day arrival, first question is how many timezones are we expecting to cross. There are 24 timezones and each are 15 degrees of longitude in width. The length of a degree of longitude varies according to latitude. This will not produce an accurate number of actual timezone crossed. There's other factors used to determine timezone boundaries. Artificial human constructs like government borders are a major factor in timezone construction. Still, it should suffice for our purposes. As this calculation doesn't change for each leg of flight, it should suffice to calculate it once as a part of leg description.  

The error introduced by this approximation of timezones crossed would be an addition day in flight time. That can easily be determined and removed after the conversion to UTC. However, if the arrival time is determined to be next day near or on a DST change date, what effect would this error produce? Rather than determine how to handle an error that could occur, it would be better to treat a next day arrival as a questioned boolean.  

This is our current "Probably Next Day Arrival" algorithm

1. Departure time is known: start with it in minute of the day
1. If traveling East: add the product of 60 times the number of estimated timezones crossed
1. If traveling West: subtract the product of 60 times the number of estimated timezones crossed.
1. Add minutes equal the predicted travel time.
1. Subtract 1440 (number of minutes in a day)
1. Is the result negative? Yes: probably same day arrival
1. Is the result positive? Yes: probably next day arrival
1. Is the absolute value of the result less than 120? (4 hour questionable range)
    * No: Signage should be good enough. It's clearly same day or next day.
    * Yes: Arrival time is close to midnight, local time.
        * Is the scheduled local arrival time greater than 22:00? Yes, same day
        * Is the scheduled local arrival time less than 03:00? Yes, next day

Perhaps that is over complicating the problem. Perhaps it would be simpler to just compare departure time to arrival time in light of estimated travel time.  

There's only 1440 minutes in a day.  
If we subtract the departure minute from 1440, then we know how many minutes are left on the day we departed. Dividing this by 1440 will return a ratio of how much of a day I have remaining.  
If we subtract the scheduled arrival minute from 1440, then we know how many minutes are left on the day we arrive.  
If we divide the number of minutes estimated traveling by 1440, then we know how much of a day was spent traveling.  

The ratio of day remaining plus the ratio of day traveling will provide a value relative to one. If that value is less than one, the travel didn't eat up the remainder of my day and relative to where I started, it's the same day. If that value is greater or equal to one, than it took up all of my remaining day and I arrived the next day relative to my starting point.

The ratio of day remaining on my arrival day minus the ratio of day spend traveling will produce a number between negative one and one. If that number is negative, then I started my journey the day before, relative to the place of my arrival. If that number is zero or positive, then I started my journey on the same day, relative to the place of my arrival.  

This provides four possible descriptions for my travel from the perspectives of where I started and where I ended.

|  | Depart Perspective</br>Arrived Same Day | Depart Perspective</br>Arrived Next Day |
|--|:--:|:--:|
| Arrival Perspective:</br>Departed Previous Day | Next Day | Next Day |
| Arrival Perspective:</br>Departed Same Day | Same Day | Same Day |

This shows that the arrival perspective is the only factor for deciding if arrival is "next day". It suggests to me there's a flaw in the logic used to get to this point. After some consideration, the flaw is it has ignored the relationship between dates of the origin and destination. While this didn't pan out, it did help illustrate a simpler method of determining "next day arrival".  

Up to now, we've been maintaining separate considerations for arrival and departure times. What the failure of the last algorithm illustrated to me is to expand this consideration to include all times at the destination timezone before converting to UTC. This is probably the most important lesson for dealing with time. Maintain a single standard and convert only when necessary. In this case, each record will be manipulated in the destination's time zone before conversion to UTC for export.  

The result of this simpler approach was a greater improvement in scheduled date times. Only two records in the 2003 test set resulted in not sane scheduled date times. Both of these seem to not be an issue in logic

```{python}
Scheduled times for RNO-SLC
{'ArrTime': datetime.time(0, 0),
 'ArrTimeGood': False,
 'CRSArrTime': datetime.time(21, 15),
 'CRSArrTimeGood': True,
 'CRSDepTime': datetime.time(20, 20),
 'CRSDepTimeGood': True,
 'DepTime': datetime.time(20, 33),
 'DepTimeGood': True,
 'ElapsedTime_Sched': datetime.timedelta(days=-1, seconds=86100),
 'ElapsedTime_SchedCalc': datetime.timedelta(seconds=86100),
 'RawDate': datetime.datetime(2003, 2, 27, 0, 0),
 'SchedArrive_dest': datetime.datetime(2003, 2, 28, 21, 15, tzinfo=<DstTzInfo 'America/Denver' MST-1 day, 17:00:00 STD>),
 'SchedDepart_dest': datetime.datetime(2003, 2, 27, 21, 20, tzinfo=<DstTzInfo 'America/Denver' MST-1 day, 17:00:00 STD>),
 'SchedDepart_local': datetime.datetime(2003, 2, 27, 20, 20, tzinfo=<DstTzInfo 'America/Los_Angeles' PST-1 day, 16:00:00 STD>)}
Difference in scheduled elapsed time for RNO-SLC.
Provided elapsed time: -1 day, 23:55:00
Calculated elapsed time: 23:55:00
```

For the first one, the provided elapsed time is negative. This is just bad data. The calculated elapsed time is also bad. The drive from Reno to Salt Lake only takes eight hours. Five minutes short of a full day for a flight is more than just unreasonable. According to Google, this flight should only take 1 hr 20 min. The issue appears to be one of the scheduled times was recorded in the timezone of the other end of the leg.  

```{python}
Scheduled times for ANC-SLC
{'ArrTime': datetime.time(7, 27),
 'ArrTimeGood': True,
 'CRSArrTime': datetime.time(7, 10),
 'CRSArrTimeGood': True,
 'CRSDepTime': datetime.time(1, 45),
 'CRSDepTimeGood': True,
 'DepTime': datetime.time(0, 45),
 'DepTimeGood': True,
 'ElapsedTime_Sched': datetime.timedelta(seconds=15900),
 'ElapsedTime_SchedCalc': datetime.timedelta(seconds=12300),
 'RawDate': datetime.datetime(2003, 10, 26, 0, 0),
 'SchedArrive_dest': datetime.datetime(2003, 10, 26, 7, 10, tzinfo=<DstTzInfo 'America/Denver' MST-1 day, 17:00:00 STD>),
 'SchedDepart_dest': datetime.datetime(2003, 10, 26, 3, 45, tzinfo=<DstTzInfo 'America/Denver' MST-1 day, 17:00:00 STD>),
 'SchedDepart_local': datetime.datetime(2003, 10, 26, 1, 45, tzinfo=<DstTzInfo 'America/Anchorage' AKST-1 day, 15:00:00 STD>)}
Difference in scheduled elapsed time for ANC-SLC.
Provided elapsed time: 4:25:00
Calculated elapsed time: 3:25:00
```

On this record, it's not clear why there's an hour difference between reported and calculated times. One troubling aspect is the predicted 4 hr 25 min travel time. According to Google, this should be closer to 6 hrs.  

[https://www.timeanddate.com/time/change/usa/anchorage?year=2003](https://www.timeanddate.com/time/change/usa/anchorage?year=2003)  

My first instinct for DST ambiguity seems to be the main factor. 1:45am happened twice on 10/26/2003. There's no way to say if the clock was the AKDT or AKST occurrence. If it was the AKDT occurrence, then the predicted time is correct. The shorter than modern predicted travel time is less concerning for our purpose.  

### Scheduled Time Edge Cases

Addressing the first error record is a question of completeness. The error seems to have occurred during data capture. Therefore it's out of my control to correct this error. As it's a capture error, the value of the record is put in question. What to do with it is a question of data completeness. For the needs of this project, I assume the inclusion of this record is not pivotal. So I'll make note of it as a dropped record and move on.  

For the second error, it's ambiguity of DST. Given a choice, I would do away with this ambiguity by having year round DST. As that's beyond my power, I'll need to introduce some rudimentary logic that determines potentially ambiguous DST datetimes and takes steps to mitigate any errors they may introduce.  

The first case is easy enough to address. If the scheduled elapsed time is negative, throw away the record. The second case needs some consideration. First step would be to determine if the scheduled arrival or departure time is causing the time skew. This would require knowing which timestamps can be ambiguous.  

One option is to build a determiner from information found on the internet: [https://www.worldtimeserver.com/time_zone_guide/documentation/](https://www.worldtimeserver.com/time_zone_guide/documentation/)  
Another option is to see what the pytz api offers. [http://pytz.sourceforge.net/](http://pytz.sourceforge.net/)  

The pytz sourceforge page specifically calls out this problem of DST caused ambiguous times under "[problems with local time](http://pytz.sourceforge.net/#problems-with-localtime)". The solution it offers is a boolean parameter "is_dst". Being able to specify if a date time is or is not DST will be helpful to ensure the correct local time zone is set. More useful is the ability to throw an exception by forcing pytz to not guess when a potentially ambiguous or impossible DST time is encountered.  

There's one error case involving ambiguous DST not covered by our logic this far. When both the departure and arrival datetimes are ambiguous and both are determined to fall on the wrong side of the DST switch, this error case is not caught with our current logic. For this purposes of this project, this error doesn't matter.

### Actual Travel Datetimes

With scheduled date times in place, what's left are the date times of actual travel. The data for these fields are captured, so the first question to settle is if we have data. The second question is if the actual depart and arrive dates match the scheduled dates. Third, are the travel times sane?  
The eight actual travel features we have can be broken up into 3 categories:

| Feature | Category |
|--|--|
| DepTime | Captured Timestamp |
| ArrTime | Captured Timestamp |
| TaxiOut | Time Passed (component) |
| AirTime | Time Passed (component) |
| TaxiIn | Time Passed (component) |
| ActualElapsedTime | Time Passed (sum) |
| ArrDelay | Time Difference |
| DepDelay | Time Difference |

The category of time passed can be further broken down, one is a sum of the times, the others are components of the elapsed times. Assessing what data we have can be done through the lens of these three categories. The completeness of data for these fields is where pandas is missed.  

## Down Scale

One final consideration is if actual travel times matter. The point of this project is to use data visualization to tell a story. The data cleaning performed this far should be more than sufficient to show the growth of an airport over time. Accurate and timely departure and arrivals would be a nice to have, but isn't necessary to complete this course.  

Another thing worth considering is refactoring the data cleanup script. In it's current form, it is functional. It also isn't the target product of this project. Consideration was to leave it as is and produce the pictures necessary to complete this course.

### Further Corrections

Having decided to focus only on scheduled times, I opened the full data set to the preparation script. I addressed some minor exceptions but then 1995 was starting to process. A large number of non-sane elapsed times were found in 1995. To complicate further, they're not multiples of 3600 and therefore do not suggest DST ambiguity.

First, I modified the DST ambiguity logic to remove the assumption of whole hours is necessary for DST anomalies. I also added logging for when no potential DST anomaly is found. From these changes, I found another data source issue. No scheduled times.  
