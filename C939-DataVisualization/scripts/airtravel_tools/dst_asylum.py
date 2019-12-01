
def IsDstAmbiguousTime(dtime, dtz):
    exitBool = False
    try:
        dtz.localize(dtime, is_dst=None)
    except pytz.exceptions.AmbiguousTimeError:
        exitBool = True
        pass
    finally:
        return exitBool

def IsDstNonExistentTime(dtime, dtz):
    exitBool = False
    try:
        dtz.localize(dtime, is_dst=None)
    except pytz.exceptions.NonExistentTimeError:
        exitBool = True
        pass
    finally:
        return exitBool

def CorrectDstAmbiguousTime(event, dtime, dtz, timeDiff):
    # timeDiff is the expected travel time minus the calculated travel time
    # if the difference is negative, then the depart time was an hour late or the arrive time was an hour early
    # if the difference is positive, then the depart time was an hour early or the arrive time was an hour late

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