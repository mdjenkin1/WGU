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

It seems the best option would be to focus on one airport. Orlando has the most traffic, so it will be our pick. 
