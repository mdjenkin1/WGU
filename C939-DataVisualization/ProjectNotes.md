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
