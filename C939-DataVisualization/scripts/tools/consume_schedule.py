#!/usr/bin/python

import csv
import datetime as dt
def consume_schedule_csv(csvFile):
    '''
        Perform minimal data preparation on raw csv files for loading to mongodb
    '''
    rawSchedule = []
    with open(csvFile, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            record = {
                'origin_date': dt.datetime(year = int(row['Year']), month = int(row['Month']), day = int(row['DayofMonth'])),
                'sched_depart_local_time': row['CRSDepTime'],
                'sched_arrive_local_time': row['CRSArrTime'],
                'sched_travel_time': row['CRSElapsedTime'],
                'actual_depart_local_time': row['DepTime'],
                'actual_arrive_local_time': row['ArrTime'],
                'actual_travel_time': row['ActualElapsedTime'],
                'carrier': row['UniqueCarrier'],
                'flight_num': row['FlightNum'],
                'tail_num': row['TailNum'],
                'origin': row['Origin'],
                'destination': row['Dest'],
                'taxi_time_in': row['TaxiIn'],
                'taxi_time_out': row['TaxiOut'],
                'air_time' : row['AirTime'],
                'cancelled': row['Cancelled'],
                'cancel_code': row['CancellationCode'],
                'diverted': row['Diverted'],
                'distance': row['Distance'],
                'time_delay_arrival': row['ArrDelay'],
                'time_delay_depart': row['DepDelay'],
                'time_delay_carrier': row['CarrierDelay'],
                'time_delay_weather': row['WeatherDelay'],
                'time_delay_nas': row['NASDelay'],
                'time_delay_security': row['SecurityDelay'],
                'time_delay_aircraft': row['LateAircraftDelay']
            }
            rawSchedule.append(record)

    print("Retrieved {} records.".format(len(rawSchedule)))
    return rawSchedule