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
What are the date/time impacts of 
