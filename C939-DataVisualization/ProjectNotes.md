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

