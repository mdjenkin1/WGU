#! /bin/python

import re
import datetime as dt
import pytz

def DstSaneTime(naiveTime, timezone):
    try:
        localTime = timezone.localize(naiveTime, is_dst=None)
        dstSane = True
    except pytz.exceptions.AmbiguousTimeError:
        localTime = timezone.localize(naiveTime)
        dstSane = False
    except pytz.exceptions.NonExistentTimeError:
        localTime = timezone.localize(naiveTime)
        dstSane = False
    finally:
        return localTime, dstSane

def IntMinutesToTimeDelta(rawMinutes):
    try:
        intIn = int(rawMinutes)
    except:
        return None
    else:
        return dt.timedelta(minutes = intIn)

def TimeDeltaToIntMinutes(roughTime):
    try:
        asMinutes = int(roughTime.total_seconds() / 60)
    except:
        return None
    else:
        return asMinutes

def HHMMToTimePart(hhmm):
    hhmmMask = re.compile(r'(\d{2})(\d{2})')
    try:
        intIn = int(hhmm)
        if len(str(intIn)) > 4: raise NameError("Too long") 
    except ValueError:
        #print("Received non-integer timestamp: {}".format(hhmm))
        return None
    except NameError:
        #print("Received too many digits for HHMM timestamp: {}".format(hhmm))
        return None
    else:
        timeParts = hhmmMask.match(str(intIn).zfill(4))
        try:
            return dt.time(int(timeParts[1]), int(timeParts[2]))
        except:
            #print("Received invalid HHMM time: {}".format(hhmm))
            return None


if __name__ == "__main__":
    print("Testing 1 digit (1): {}".format(HHMMToTimePart(1)))
    print("Testing 2 digits (12): {}".format(HHMMToTimePart(12)))
    print("Testing 3 digits (123): {}".format(HHMMToTimePart(123)))
    print("Testing 4 digits (1234): {}".format(HHMMToTimePart(1234)))
    print("Testing 5 digits (12345): {}".format(HHMMToTimePart(12345)))
    print("Testing not digit (NaN): {}".format(HHMMToTimePart("NaN")))
    print("Testing > 2400 (3456): {}".format(HHMMToTimePart(3456)))
    print("Testing > 60 min (66): {}".format(HHMMToTimePart(66)))
    print("Testing mil time (1500): {}".format(HHMMToTimePart(1500)))
