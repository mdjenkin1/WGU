#!/usr/bin/python

import pytz

def DstSaneTime(naiveTime, timezone):
    try:
        localTime = timezone.localize(naiveTime, is_dst=None)
    except pytz.exceptions.AmbiguousTimeError:
        localTime = timezone.localize(naiveTime)
        dstSane = False
    except pytz.exceptions.NonExistentTimeError:
        localTime = timezone.localize(naiveTime)
        dstSane = False
    finally:
        return localTime,dstSane

def IsDstAmbiguousTime(dtime, dtz):
    """ leverage pytz.exceptions to check for anomalous DST time """
    exitBool = False
    try:
        dtz.localize(dtime, is_dst=None)
    except pytz.exceptions.AmbiguousTimeError:
        exitBool = True
        pass
    finally:
        return exitBool

def IsDstNonExistentTime(dtime, dtz):
    """ leverage pytz.exceptions to check for anomalous DST time """
    exitBool = False
    try:
        dtz.localize(dtime, is_dst=None)
    except pytz.exceptions.NonExistentTimeError:
        exitBool = True
        pass
    finally:
        return exitBool

def CorrectDstAmbiguousTime(event, dtime, dtz, timeDiff):
    """ 
    In the case of an error due to ambiguous DST time, elapsed travel time can be corrected by assigning the 
    ambiguous time that results in lesser error.

    timeDiff is the expected travel time minus the calculated travel time
    if the difference is negative, then the depart time was an hour late or the arrive time was an hour early
    if the difference is positive, then the depart time was an hour early or the arrive time was an hour late
    """

    if event == "depart":
        if timeDiff > 0:
            return dtz.localize(dtime, is_dst=True)
        else:
            return dtz.localize(dtime, is_dst=False)
    if event == "arrive":
        if timeDiff > 0:
            return dtz.localize(dtime, is_dst=False)
        else:
            return dtz.localize(dtime, is_dst=True)