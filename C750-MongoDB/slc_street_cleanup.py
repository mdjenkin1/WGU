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

def clean_slc_streets(street):
    return True

def test(infile = "map"):
    # get raw map data
    raw_map_data = m2m.get_osm_map_data(infile)
    # clean the raw map data
    cln_map_data = clean_slc_streets(raw_map_data)
    # load the clean data to mongodb
    m2m.load_osm_map_data(cln_map_data, 'localhost', 27017, 'salt_lake_city_clean')
    pass

if __name__ == "__main__":
    test("map")