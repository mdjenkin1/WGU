
compassPoints = (
    "North", "NorthEast",
    "East", "SouthEast",
    "South", "SouthWest",
    "West", "NorthWest"
)

def GetDirection(degree, compass):
    dirIndex = round(degree * len(compass) / 360) % len(compass)
    return compass[dirIndex]


def DescribeLeg(origin, dest, compass=compassPoints):

    """
    Given an origin and destination airport, provide:
    the bearing: 'Bearing'
    the direction of travel: 'DirectionOfTravel'
    the flight distance: 'CalculatedDistance'

    Use the Haversine formula to determine the distance and bearing
    https://www.movable-type.co.uk/scripts/latlong.html
    """

    if origin not in airports or dest not in airports:
        raise Exception("Unknown airport. Cannot determine direction of travel.")

    # Radius of the earth in miles
    Radius = 3959

    # Origin longitude and latitude in radians
    oLat = airports[origin]["lat"]
    oLong = airports[origin]["long"]

    # Destination longitude and latitude in radians
    dLat = airports[dest]["lat"]
    dLong = airports[dest]["long"]
    
    # Delta longitude and latitude in radians
    deltaLat = dLat - oLat
    deltaLong = dLong - oLong

    # Haversine formula to calculate distance
    a = (math.sin(deltaLat/2))**2 + math.cos(oLat) * math.cos(dLat) * (math.sin(deltaLong/2))**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    calcDist = round(Radius * c)

    # Direction
    v1 = math.sin(deltaLong) * math.cos(dLat)
    v2 = math.cos(oLat) * math.sin(dLat) - math.sin(oLat) * math.cos(dLat) * math.cos(deltaLong)
    degBearing = round(math.atan2(v1, v2) * 180 / math.pi)
    #if degBearing < 0: degBearing += 360 

    direction = GetDirection(degBearing, compass)

    oTz = tf.timezone_at(lng=oLong, lat=oLat)
    dTz = tf.timezone_at(lng=dLong, lat=dLat)

    outDict = {
        origin + "-" + dest : {
            "CalculatedDistance": calcDist,
            "Bearing": degBearing,
            "DirectionOfTravel": direction
        }
    }

    return outDict

def GetTime(timeIn):
    """convert a 4 digit integer or string to time. Return midnight if "NA" or invalid. 
    Include a boolean to flag false midnight return"""
    goodTime = True
    try:
        timeOut = dt.datetime.strptime(timeIn.zfill(4),"%H%M").time()
    except:
        timeOut = dt.time(hour=0, minute=0)
        goodTime = False
    return timeOut, goodTime

def GetTimeDelta(timeIn):
    """convert an integer count of minutes passed to a time delta"""
    goodTime = True
    try:
        timeOut = dt.timedelta(minutes = int(timeIn))
    except:
        timeOut = dt.timedelta(minutes = 0)
        goodTime = False
    return timeOut, goodTime

