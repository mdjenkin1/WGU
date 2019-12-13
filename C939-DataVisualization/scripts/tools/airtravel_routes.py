#!/usr/bin/python

import math

compassPoints = (
    "North", "NorthEast",
    "East", "SouthEast",
    "South", "SouthWest",
    "West", "NorthWest"
)

def GetDirection(bearing, compass=compassPoints):
    """
    Given a degree bearing and a compass with number of points equal to a multiple of 2:
    Return which point on that compass most closely describes that bearing
    """

    # A circle can be divided into N number of compass points of arc N/360
    # Multiplying the bearing by the size of each arc, will determine in which arc the bearing resides
    # If the number of points/arcs is a multiple of 2 then rounding will provide a clean 
    # break between arcs at half values.
    # Finally, taking the modulo will return an index of the corresponding compass arc.
    dirIndex = round(bearing * len(compass) / 360) % len(compass)
    return compass[dirIndex]


def GetRouteDescription(origin, dest, compass=compassPoints):

    """
    Given origin and destination airport records, provide:
    the bearing: 'Bearing'
    the direction of travel: 'DirectionOfTravel'
    the flight distance: 'CalculatedDistance'

    airport records are dictionaries with the following values:
    iata: Three character IATA code
    lat: Latitude in radians
    long: Longitude in radians

    Use the Haversine formula to determine the distance and bearing
    https://www.movable-type.co.uk/scripts/latlong.html
    """

    # Approximate radius of the Earth in miles
    Radius = 3959
    
    # Delta longitude and latitude in radians
    lat_delta = dest['lat'] - origin['lat']
    long_delta = dest['long'] - origin['long']

    # Haversine formula to calculate distance
    a = (math.sin(lat_delta/2))**2 + math.cos(origin['lat']) * math.cos(dest['lat']) * (math.sin(long_delta/2))**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    calcDist = round(Radius * c)

    # Direction
    v1 = math.sin(long_delta) * math.cos(dest['lat'])
    v2 = math.cos(origin['lat']) * math.sin(dest['lat']) - math.sin(origin['lat']) * math.cos(dest['lat']) * math.cos(long_delta)
    degBearing = round(math.atan2(v1, v2) * 180 / math.pi)
    direction = GetDirection(degBearing, compass)

    RouteDescription = {
            "Destination": dest['iata'],
            "Origin": origin['iata'],
            "CalculatedDistance": calcDist,
            "Bearing": degBearing,
            "DirectionOfTravel": direction
    }

    return RouteDescription

def GetTime(timeIn):
    """convert a 4 digit integer or string to time. Return midnight if "NA" or invalid. 
    Include a boorigin['lean'] to flag false midnight return"""
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

