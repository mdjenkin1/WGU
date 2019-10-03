# Udacity Data Visualizations Project Notes

Dataset study in tandem with course material.

## Airline Data

One of the suggested, intermediate, datasets is being used for this project. Specifically, historical flight data from RITA.

* [RITA](https://www.google.com/url?q=http://www.transtats.bts.gov/OT_Delay/OT_DelayCause1.asp&sa=D&ust=1554488156369000)
* [Flights](https://www.google.com/url?q=http://stat-computing.org/dataexpo/2009/the-data.html&sa=D&ust=1554488156368000)

| Name| Description| Quali \ Quanti |  |
|--|--|--|--|
| Year | 1987-2008 | Quantitative | Continuous |
| Month | 1-12 | Quantitative | Continuous |
| DayofMonth | 1-31 | Quantitative |
 Continuous |
| DayOfWeek | 1 (Monday) - 7 (Sunday) | Quantitative | Continuous |
| DepTime | actual departure time (local, hhmm) | Quantitative | Continuous |
| CRSDepTime | scheduled departure time (local, hhmm) | Quantitative | Continuous |
| ArrTime | actual arrival time (local, hhmm) | Quantitative | Continuous |
| CRSArrTime | scheduled arrival time (local, hhmm) | Quantitative | Continuous |
| UniqueCarrier | unique carrier code | Qualitative | Categorical |
| FlightNum | flight number | Qualitative | Categorical |
| TailNum | plane tail number | Qualitative | Categorical |
| ActualElapsedTime | in minutes | Quantitative | Discrete |
| CRSElapsedTime | in minutes | Quantitative | Discrete |
| AirTime | in minutes | Quantitative | Discrete |
| ArrDelay | arrival delay, in minutes | Quantitative | Discrete |
| DepDelay | departure delay, in minutes | Quantitative | Discrete |
| Origin | origin IATA airport code | Qualitative | Categorical |
| Dest | destination IATA airport code | Qualitative | Categorical |
| Distance | in miles | Quantitative | Discrete |
| TaxiIn | taxi in time, in minutes | Quantitative | Discrete |
| TaxiOut | taxi out time in minutes | Quantitative | Discrete |
| Cancelled | was the flight cancelled? | Qualitative | Categorical |
| CancellationCode | reason for cancellation (A = carrier, B = weather, C = NAS, D = security) | Qualitative | Categorical |
| Diverted | 1 = yes, 0 = no | Qualitative | Categorical |
| CarrierDelay | in minutes | Quantitative | Discrete |
| WeatherDelay | in minutes | Quantitative | Discrete |
| NASDelay | in minutes | Quantitative | Discrete |
| SecurityDelay | in minutes | Quantitative | Discrete |
| LateAircraftDelay | in minutes | Quantitative | Discrete |