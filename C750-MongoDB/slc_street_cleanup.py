"""
Expand abbreviated coordinate street directions in SLC map data to full length names 
e.g.
N: North
E: East
S: South
W: West

It appears someone is already using pascal casing for street direction designations.
So we will too.
> db.ways.aggregate([{$unwind: "$tags"}, {$match: {$or: [{"tags.k": /^addr:str/},{"tags.k": /^addr:hou/}]}}, {$match: {$and: [{"tags.v": /\bWest\b|\bEast\b|\bSouth\b|\bNorth\b/}]}}, {$group: {"_id": "tags.k", "count": {$sum: 1}}}])
{ "_id" : "tags.k", "count" : 10172 }
> db.ways.aggregate([{$unwind: "$tags"}, {$match: {$or: [{"tags.k": /^addr:str/},{"tags.k": /^addr:hou/}]}}, {$match: {$and: [{"tags.v": /\bWEST\b|\bEAST\b|\bSOUTH\b|\bNORTH\b/}]}}, {$group: {"_id": "tags.k", "count": {$sum: 1}}}])
>

Structure for map_data:
nodes: [{
    type: "node"
    id: value,
    lat: value,
    lon: value,
    version: value,
    timestamp: value,
    changeset: value,
    uid: value,
    user: value,
    tags: [
        {"k": k_value, "v": v_value},
        ...
    ]
}]

ways: [{
    type: "way"
    id: value,
    version: value,
    timestamp: value,
    changeset: value,
    uid: value,
    user: value,
    tags: [
        {"k": k_value, "v": v_value},
        ...
    ]
    nd_ref:[
        value
    ]
}]

relations: [{
    type: "relation"
    id: value,
    version: value,
    timestamp: value,
    changeset: value,
    uid: value,
    user: value,
    tags: [
        {"k": k_value, "v": v_value},
        ...
    ]
    members:[
        {type: value,
        ref: value,
        role: value},
    ]
}]
"""

import map_to_mongo as m2m
import re

addr_house_re = re.compile(r'^addr:housenumber', re.IGNORECASE)
addr_street_re = re.compile(r'^addr:street', re.IGNORECASE)
direction_abbr_re = re.compile(r'\b[NESW]\b', re.IGNORECASE)
ave_street_re = re.compile(r'^[NESW] Street$', re.IGNORECASE)

def clean_slc_streets(raw_map_data):
    for node in raw_map_data['nodes']:
        for tag in node['tags']:
            if is_street_addr(tag['k']):
                #print("{} is a street or house address".format(tag['k']))
                tag['v'] = expand_street_abbr(tag['v'])
                print("{} should have expanded directions".format(tag['v']))

    for node in raw_map_data['ways']:
        for tag in node['tags']:
            if is_street_addr(tag['k']):
                #print("{} is a street or house address".format(tag['k']))
                tag['v'] = expand_street_abbr(tag['v'])
                print("{} should have expanded directions".format(tag['v']))

    return True

def expand_street_abbr(street):
    if ave_street_re.search(street):
        return street
    elif direction_abbr_re.search(street):
        return street
    else:
        return street

def is_street_addr(street):
    is_street = addr_street_re.search(street)
    is_house = addr_house_re.search(street)
    return (is_street or is_house)

def test(infile = "map"):
    # get raw map data
    raw_map_data = m2m.get_osm_map_data(infile)
    # clean the raw map data
    cln_map_data = clean_slc_streets(raw_map_data)
    # load the clean data to mongodb
    #m2m.load_osm_map_data(cln_map_data, 'localhost', 27017, 'salt_lake_city_clean')
    pass

if __name__ == "__main__":
    test("map")