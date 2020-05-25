#! /bin/python

import datetime as dt
import pytz
import pprint

from time_tools import HHMMToTimePart,IntMinutesToTimeDelta,DstSaneTime,TimeDeltaToIntMinutes

def GetFlightTimeData(flight, oTZ, dTZ):
    metadata = {}
    metadata['missing'] = {}
    metadata['dst_sane'] = {}
    metadata['next_day'] = {}

    try:
        orgTZ = pytz.timezone(oTZ)
        destTZ = pytz.timezone(dTZ)
    except pytz.exceptions.UnknownTimeZoneError:
        print("Unknown Timezone. Origin {} or Destination {}".format(oTZ,dTZ))
        pprint.pprint(flight)


    metadata['same_timezone'] = True if orgTZ == destTZ else False

    actDepart = HHMMToTimePart(flight['actual_depart_local_time'])
    actArrive = HHMMToTimePart(flight['actual_arrive_local_time'])

    if actDepart is None: metadata['missing']['actual_depart'] = True
    if actArrive is None: metadata['missing']['actual_arrive'] = True

    #### Scheduled Times
    #
    # Assume the times we have are valid
    # Generate metadata for later decision making
    #

    schDepart = HHMMToTimePart(flight['sched_depart_local_time'])
    schArrive = HHMMToTimePart(flight['sched_arrive_local_time'])
    
    # Arrive and depart times of both midnight are the same as not captured
    if schDepart == schArrive == dt.time(0,0):
        #print("Setting zero scheduled times to None")
        schDepart = None
        schArrive = None

    #Scheduled depart
    if schDepart:
        schDepart_naive = dt.datetime.combine(flight['origin_date'], schDepart)
        schDepart_orgTZ, dstSane = DstSaneTime(schDepart_naive, orgTZ)
        schDepart_utc = schDepart_orgTZ.astimezone(pytz.utc)
        metadata['missing']['sched_depart'] = False
        metadata['dst_sane']['sched_depart'] = dstSane
    else:
        schDepart_utc = None
        metadata['missing']['sched_depart'] = True
        metadata['dst_sane']['sched_depart'] = None
    
    #Scheduled arrival
    if schArrive:
        schArrive_naive = dt.datetime.combine(flight['origin_date'], schArrive)
        schArrive_destTZ, dstSane = DstSaneTime(schArrive_naive, destTZ)
        schArrive_utc = schArrive_destTZ.astimezone(pytz.utc)
        metadata['missing']['sched_arrive'] = False
        metadata['dst_sane']['sched_arrive'] = dstSane
    else:
        schArrive_utc = None
        metadata['missing']['sched_arrive'] = True
        metadata['dst_sane']['sched_arrive'] = None

    # If a next day arrival, the arrival date needs to be corrected
    if not (metadata['missing']['sched_depart'] or metadata['missing']['sched_arrive']):
        if schArrive_utc < schDepart_utc:
            #print("Next day arrival correction.")
            #print("Depart Local: {}".format(schDepart_orgTZ))
            #print("Arrival Local: {}".format(schArrive_destTZ))
            #print("Depart UTC: {}".format(schDepart_utc))
            #print("Arrival UTC: {}".format(schArrive_utc))
            schArrive_naive = dt.datetime.combine(flight['origin_date']+ dt.timedelta(days=1), schArrive)
            schArrive_destTZ, dstSane = DstSaneTime(schArrive_naive, destTZ)
            schArrive_utc = schArrive_destTZ.astimezone(pytz.utc)
            metadata['missing']['sched_arrive'] = False
            metadata['dst_sane']['sched_arrive'] = dstSane
            metadata['next_day']['sched_arrive'] = True
            #print("Corrected arrival Local: {}".format(schArrive_destTZ))
            #print("Corrected arrival UTC: {}\n".format(schArrive_utc))
        else:
            metadata['next_day']['sched_arrive'] = False

    #### Actual Times
    #
    # Assume the times we have are valid
    # Generate metadata for later decision making
    #
    actDepart = HHMMToTimePart(flight['actual_depart_local_time'])
    actArrive = HHMMToTimePart(flight['actual_arrive_local_time'])
    
    # Arrive and depart times of both midnight are the same as not captured
    if actDepart == actArrive == dt.time(0,0):
        #print("Setting zero actual times to None")
        actDepart = None
        actArrive = None

    #Actual depart
    if actDepart:
        actDepart_naive = dt.datetime.combine(flight['origin_date'], actDepart)
        actDepart_orgTZ, dstSane = DstSaneTime(actDepart_naive, orgTZ)
        actDepart_utc = actDepart_orgTZ.astimezone(pytz.utc)
        metadata['missing']['actual_depart'] = False
        metadata['dst_sane']['actual_depart'] = dstSane
    else:
        actDepart_utc = None
        metadata['missing']['actual_depart'] = True
        metadata['dst_sane']['actual_depart'] = None
    
    #Actual arrival
    if actArrive:
        actArrive_naive = dt.datetime.combine(flight['origin_date'], actArrive)
        actArrive_destTZ, dstSane = DstSaneTime(actArrive_naive, destTZ)
        actArrive_utc = actArrive_destTZ.astimezone(pytz.utc)
        metadata['missing']['actual_arrive'] = False
        metadata['dst_sane']['actual_arrive'] = dstSane
    else:
        actArrive_utc = None
        metadata['missing']['actual_arrive'] = True
        metadata['dst_sane']['actual_arrive'] = None

    # If a next day arrival, the arrival date needs to be corrected
    if not (metadata['missing']['actual_depart'] or metadata['missing']['actual_arrive']):
        if actArrive_utc < actDepart_utc:
            #print("Next day arrival correction.")
            #print("Depart Local: {}".format(actDepart_orgTZ))
            #print("Arrival Local: {}".format(actArrive_destTZ))
            #print("Depart UTC: {}".format(actDepart_utc))
            #print("Arrival UTC: {}".format(actArrive_utc))
            actArrive_naive = dt.datetime.combine(flight['origin_date']+ dt.timedelta(days=1), actArrive)
            actArrive_destTZ, dstSane = DstSaneTime(actArrive_naive, destTZ)
            actArrive_utc = actArrive_destTZ.astimezone(pytz.utc)
            metadata['missing']['actual_arrive'] = False
            metadata['dst_sane']['actual_arrive'] = dstSane
            metadata['next_day']['actual_arrive'] = True
            #print("Corrected arrival Local: {}".format(actArrive_destTZ))
            #print("Corrected arrival UTC: {}\n".format(actArrive_utc))
        else:
            metadata['next_day']['actual_arrive'] = False
    
    #### Elapsed Times
    # 
    # Assume the times we have are valid
    # Generate metadata for later decision making
    # 
    
    schTravelTime_rec = IntMinutesToTimeDelta(flight['sched_travel_time'])
    actTravelTime_rec = IntMinutesToTimeDelta(flight['actual_travel_time'])
    taxiIn = IntMinutesToTimeDelta(flight['taxi_time_in'])
    taxiOut = IntMinutesToTimeDelta(flight['taxi_time_out'])
    airTime = IntMinutesToTimeDelta(flight['air_time'])

    if schTravelTime_rec:
        metadata['missing']['sched_travel_time'] = False
    else:
        metadata['missing']['sched_travel_time'] = True

    if actTravelTime_rec:
        metadata['missing']['actual_travel_time'] = False
    else:
        metadata['missing']['actual_travel_time'] = True

    if taxiIn:
        metadata['missing']['taxi_in_time'] = False
    else:
        metadata['missing']['taxi_in_time'] = True
    if taxiOut:
        metadata['missing']['taxi_out_time'] = False
    else:
        metadata['missing']['taxi_out_time'] = True
    if airTime:
        metadata['missing']['air_time'] = False
    else:
        metadata['missing']['air_time'] = True
    
    if not (metadata['missing']['sched_depart'] or metadata['missing']['sched_arrive']):
        schTravelTime_calc = schArrive_utc - schDepart_utc
    else:
        schTravelTime_calc = None

    if not (metadata['missing']['actual_depart'] or metadata['missing']['actual_arrive']):
        actTravelTime_calc = actArrive_utc - actDepart_utc
    else:
        actTravelTime_calc = None

    flight_times = {
        "sched_depart_utc" : schDepart_utc,
        "sched_arrive_utc" : schArrive_utc,
        "actual_depart_utc" : actDepart_utc,
        "actual_arrive_utc" : actArrive_utc,
        "travel_times" : {
            "recorded_scheduled" : TimeDeltaToIntMinutes(schTravelTime_rec),
            "recorded_actual" : TimeDeltaToIntMinutes(actTravelTime_rec),
            "calculated_scheduled" : TimeDeltaToIntMinutes(schTravelTime_calc),
            "calculated_actual" : TimeDeltaToIntMinutes(actTravelTime_calc),
            "taxi_in" : TimeDeltaToIntMinutes(taxiIn),
            "taxi_out" : TimeDeltaToIntMinutes(taxiOut),
            "air_time" : TimeDeltaToIntMinutes(airTime)
        }
    }

    return flight_times, metadata

CancelReason = {
    'A' : "Carrier", 
    'B' : "Weather", 
    'C' : "NAS", 
    'D' : "security"
}

def GetFlightStats(flight, flight_times):

    missing = {}

    statistics = {
        'schedule_accuracy' : {},
        'cancelled' : {},
        'attributed_delay' : {}
    }

    ##### Schedule Skew
    # 
    # How accurate was the flight schedule?
    # Valid values will convert to timedeltas
    # Mongodb will not store timedeltas
    #
     
    arriveSkew_reported = IntMinutesToTimeDelta(flight['time_delay_arrival'])
    departSkew_reported = IntMinutesToTimeDelta(flight['time_delay_depart'])

    if arriveSkew_reported:
        statistics['schedule_accuracy']['arrive_skew_reported'] = TimeDeltaToIntMinutes(arriveSkew_reported)
        missing['arrive_skew_reported'] = False
    else:
        statistics['schedule_accuracy']['arrive_skew_reported'] = None
        missing['arrive_skew_reported'] = True

    if departSkew_reported:
        statistics['schedule_accuracy']['depart_skew_reported'] = TimeDeltaToIntMinutes(departSkew_reported)
        missing['depart_skew_reported'] = False
    else:
        statistics['schedule_accuracy']['depart_skew_reported'] = None
        missing['depart_skew_reported'] = True

    if flight_times['actual_arrive_utc'] and flight_times['sched_arrive_utc']:
        arriveSkew_calculated = flight_times['actual_arrive_utc'] - flight_times['sched_arrive_utc']
        statistics['schedule_accuracy']['arrive_skew_calculated'] = TimeDeltaToIntMinutes(arriveSkew_calculated)
    else:
        statistics['schedule_accuracy']['arrive_skew_calculated'] = None

    if flight_times['actual_depart_utc'] and flight_times['sched_depart_utc']:
        departSkew_calculated = flight_times['actual_depart_utc'] - flight_times['sched_depart_utc']
        statistics['schedule_accuracy']['depart_skew_calculated'] = TimeDeltaToIntMinutes(departSkew_calculated)
    else:
        statistics['schedule_accuracy']['depart_skew_calculated'] = None

    ##### Attributed Delays
    # 
    # Did someone record why the schedule was skewed?
    # Valid values will convert to timedeltas
    # Mongodb will not store timedeltas
    #

    carrierDelay_reported = IntMinutesToTimeDelta(flight['time_delay_carrier'])
    weatherDelay_reported = IntMinutesToTimeDelta(flight['time_delay_weather'])
    nasDelay_reported = IntMinutesToTimeDelta(flight['time_delay_nas'])
    securityDelay_reported = IntMinutesToTimeDelta(flight['time_delay_security'])
    aircraftDelay_reported = IntMinutesToTimeDelta(flight['time_delay_aircraft'])

    if carrierDelay_reported:
        statistics['attributed_delay']['carrier'] = TimeDeltaToIntMinutes(carrierDelay_reported)
        missing['delay_carrier'] = False
    else: 
        statistics['attributed_delay']['carrier'] = None
        missing['delay_carrier'] = True

    if weatherDelay_reported:
        statistics['attributed_delay']['weather'] = TimeDeltaToIntMinutes(weatherDelay_reported)
        missing['delay_weather'] = False
    else:
        statistics['attributed_delay']['weather'] = None
        missing['delay_weather'] = True

    if nasDelay_reported:
        statistics['attributed_delay']['nas'] = TimeDeltaToIntMinutes(nasDelay_reported)
        missing['delay_nas'] = False
    else:
        statistics['attributed_delay']['nas'] = None
        missing['delay_nas'] = True

    if securityDelay_reported:
        statistics['attributed_delay']['security'] = TimeDeltaToIntMinutes(securityDelay_reported)
        missing['delay_security'] = False
    else:
        statistics['attributed_delay']['security'] = None
        missing['delay_security'] = True

    if aircraftDelay_reported:
        statistics['attributed_delay']['aircraft'] = TimeDeltaToIntMinutes(aircraftDelay_reported)
        missing['delay_aircraft'] = False
    else:
        statistics['attributed_delay']['aircraft'] = None
        missing['delay_aircraft'] = True

    ##### Cancelled Flight
    # 
    #

    if flight['cancelled'] == "0":
        statistics['cancelled'] =  None
    else:
        statistics['cancelled']['reason'] = CancelReason.get(flight['cancel_code'], None)
        statistics['cancelled']['diverted'] = True if flight['diverted'] == 0 else False

    return statistics,missing
