"""
### metadata hash
# 
# missing = {
#   sched_depart = bool
#   sched_arrive = bool
#   sched_travel_time = bool
#   actual_depart = bool
#   actual_arrive = bool
#   actual_travel_time = bool
# }
# 
# dst_sane = {
#   sched_depart = bool
#   sched_arrive = bool
#   actual_depart = bool
#   actual_arrive = bool
# }
#
# next_day = {
#   sched_arrive = bool
#   actual_arrive = bool
# }

### Scheduled time processing

Non-Cancelled flights
sched_depart != sched_arrive != 0

Start with flight['origin_date']
add flight['sched_depart_local_time']
add db.airports.find_one({'iata' : flight['origin']})['timezone']
result schDepart_orgTZ

check schDepart_orgTZ for possible DST ambiguity

if we have flight['sched_travel_time'] (in minutes)
    add it to schDepart_orgTZ
    result schArrive_est_orgTZ
if we do not have flight['sched_travel_time']
    schArrive_est_orgTZ = None

Start with flight['origin_date']
add flight['sched_arrive_local_time']
add db.airports.find_one({'iata' : flight['origin']})['timezone']
result schDepart_orgTZ

"""


""" 
Scrub flight scheduling data after consumption of raw air travel csv files
Pre-existing Collections:
> db.airports.findOne()
{
    "_id" : ObjectId("5e9c9bba6018921f596f83db"),
    "iata" : "00M",
    "airport" : "Thigpen ",
    "city" : "Bay Springs",
    "state" : "MS",
    "country" : "USA",
    "lat" : 0.557698402771604,
    "long" : -1.5574359137504208,
    "timezone" : "America/Chicago"
}

> db.raw_schedules.findOne()
{
    "_id" : ObjectId("5e9d1d5609199fdc472129f0"),
    "origin_date" : ISODate("1987-10-14T00:00:00Z"),
    "sched_depart_local_time" : "730",
    "sched_arrive_local_time" : "849",
    "sched_travel_time" : "79",
    "actual_depart_local_time" : "741",
    "actual_arrive_local_time" : "912",
    "actual_travel_time" : "91",
    "carrier" : "PS",
    "flight_num" : "1451",
    "tail_num" : "NA",
    "origin" : "SAN",
    "destination" : "SFO",
    "taxi_time_in" : "NA",
    "taxi_time_out" : "NA",
    "cancelled" : "0",
    "cancel_code" : "NA",
    "diverted" : "0",
    "distance" : "447",
    "time_delay_arrival" : "23",
    "time_delay_depart" : "11",
    "time_delay_carrier" : "NA",
    "time_delay_weather" : "NA",
    "time_delay_nas" : "NA",
    "time_delay_security" : "NA",
    "time_delay_aircraft" : "NA"
}

> db.routes.findOne()
{
    "_id" : ObjectId("5e9d2d9a09199fdc477e2869"),
    "destination" : "RDU",
    "origin" : "PIT",
    "distance_calculated" : 328,
    "bearing" : 166,
    "direction" : "South"
}

Target Collection schema
> db.flights.findOne()
{
    "flight" : {
        "carrier"
        "flight_num"
        "tail_num"
        "route" : {
            "route" : "org-dest"
            "origin" : {
                "iata"
                "airport"
                "city"
                "state"
                "country"
                "latitude"
                "longitude"
                "timezone"
            }
            "destination" : {
                "iata"
                "airport"
                "city"
                "state"
                "country"
                "latitude"
                "longitude"
                "timezone"
            }
            "bearing"
            "direction"
            "distance_calculated"
            "distance_recorded"
        }
    }

    "times" : {
        "sched_depart_utc"
        "sched_arrive_utc"
        "actual_depart_utc"
        "actual_arrive_utc"
        "travel_time" : {
            "recorded_scheduled"
            "recorded_actual"
            "taxi_in"
            "in_air"
            "taxi_out"
        }
    }

    "statistics" : {
        "schedule_accuracy" : {
            "arrival_minutes"
            "depart_minutes"
        }
        "cancelled" : {
            "diverted"
            "reason"
        }
        "attributed_delays" : {
            "carrier"
            "weather"
            "nas"
            "security"
            "late_aircraft"
        }
    }

    "metadata" : {}
}
"""

### Datetime calculations
#print("Flying from {} to {}".format(row['Origin'],row['Dest']))

tmpDT = {}
orgTz = pytz.timezone(airports[row['Origin']]['OlsenTz'])
destTz = pytz.timezone(airports[row['Dest']]['OlsenTz'])

for field in list(flightTimeNames.keys()):
    timeField = field + "Time"
    tmpDT[timeField], tmpDT[timeField+"Good"] = GetTime(row[timeField])

# Scheduled departure
tmpDT['RawDate'] = dt.datetime(year = int(row["Year"]), month = int(row["Month"]), day = int(row["DayofMonth"]))

## Naive Depart time
naiveSchedDepart = dt.datetime.combine(tmpDT['RawDate'], tmpDT['CRSDepTime'])

## Depart time at origin
tmpDT['SchedDepart_local'] = orgTz.localize(naiveSchedDepart)

## Depart time at destination
tmpDT['SchedDepart_dest'] = tmpDT['SchedDepart_local'].astimezone(destTz)

# Determine date of scheduled arrival
## if the arrival time is sane
if tmpDT['CRSArrTimeGood']:
    schedArriveDate = tmpDT["SchedDepart_dest"].date()
    # compare depart and arrive times as clocked at the destination
    # add a day if the arrival time is earlier than depart time
    if tmpDT['CRSArrTime'] < tmpDT['SchedDepart_dest'].time():
        schedArriveDate = schedArriveDate + dt.timedelta(days=1)
else:
    print("Bad Arrival Time Recorded")
    continue

naiveSchedArrive = dt.datetime.combine(schedArriveDate, tmpDT['CRSArrTime'])
tmpDT['SchedArrive_dest'] = destTz.localize(naiveSchedArrive)

# Is the scheduled elapsed time sane
tmpDT['ElapsedTime_SchedCalc'] = tmpDT['SchedArrive_dest'] - tmpDT['SchedDepart_dest']
try:
    tmpDT['ElapsedTime_Sched'] = dt.timedelta(minutes=int(row['CRSElapsedTime']))
except:
    print("Invalid scheduled elapsed time provided: {}".format(row['CRSElapsedTime']))
    # Possible NA scheduled time from "Cancelled" flight. Additional context necessary
    if row['CRSElapsedTime'] == 'NA' and row['Cancelled'] == 1:
        print("Cancelled flight, Record requires context processing")
        #postProcess.append(row)
        continue

    # I do not know why this DST ambiguity check is here. I do not believe it needs to be here.
    #for label, dtime, dtz in (["depart", naiveSchedDepart, orgTz],["arrive", naiveSchedArrive, destTz]):
    #    if IsDstAmbiguousTime(dtime, dtz):
    #        print("Ambiguous {} time: {} {}".format(label, dtime, dtz))
    #        print("Check sanity of flight {} elapsed time: {}".format(journeyLeg, tmpDT['ElapsedTime_SchedCalc']))
    #    else:
    #        print("Scheduled {} time is not DST ambiguous: {} {}".format(label, dtime, dtz))
    elapsedTimesDiff = 0
    tmpDT['ElapsedTime_Sched'] = None
else:
    elapsedTimesDiff = (tmpDT['ElapsedTime_Sched'] - tmpDT['ElapsedTime_SchedCalc']).total_seconds()

if elapsedTimesDiff != 0:
    print("")
    print("Non-sane elapsed times, difference in seconds: {}".format(elapsedTimesDiff))

    # Scheduled Depart time and Scheduled Arrive time == 0, special post processing required
    if int(row['CRSArrTime']) == 0 and int(row['CRSArrTime']) == 0:
        print("Scheduled depart and arrive times = 0")
        print("Record requires context processing")
        postProcess.append(row)
        continue

    # Negative provided elapsed time suggests improper data capture. For our intent, drop the record and move on.
    if tmpDT['ElapsedTime_Sched'] <= dt.timedelta(minutes=0):
        print("Negative elapsed time, dropping record: {}".format(row))
        droppedRecords.append(row)
        continue

    # Errors of non-existent time have NOT been encountered. Saving incase this changes
    #if IsDstNonExistentTime(dtime, dtz):
    #    print("Nonexistant {} time: {} {}".format(label, dtime, dtz))
    #   print("Dropping record: {}".format(row))
    #    droppedRecords.append(row)
    #    continue

    # One or Two hour differences in elapsed times suggests an error of DST ambiguity
    #if elapsedTimesDiff % 3600 == 0:
    if IsDstAmbiguousTime(naiveSchedDepart, orgTz):
        print("Ambiguous {} time: {} {}".format("depart", naiveSchedDepart, orgTz))
        correctedTime = CorrectDstAmbiguousTime("depart", naiveSchedDepart, orgTz, elapsedTimesDiff)
        tmpDT['SchedDepart_local'] = correctedTime
        tmpDT['SchedDepart_dest'] = tmpDT['SchedDepart_local'].astimezone(destTz)
        print("Corrected ambiguous departure DST time.")

    if IsDstAmbiguousTime(naiveSchedArrive, destTz):
        print("Ambiguous {} time: {} {}".format("arrive", naiveSchedArrive, destTz))
        correctedTime = CorrectDstAmbiguousTime("arrive", naiveSchedArrive, destTz, elapsedTimesDiff)
        tmpDT['SchedArrive_dest'] = correctedTime
        print("Corrected ambiguous arrival DST time.")

    tmpDT['ElapsedTime_SchedCalc'] = tmpDT['SchedArrive_dest'] - tmpDT['SchedDepart_dest']
    if (tmpDT['ElapsedTime_Sched'] - tmpDT['ElapsedTime_SchedCalc']).total_seconds() == 0:
        print("Corrected elapsed time difference.")
    else: print ("Elapsed time mismatch remains")
