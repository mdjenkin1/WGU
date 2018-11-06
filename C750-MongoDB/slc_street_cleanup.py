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
direction_abbr_re = re.compile(r'(.*?)\b([NESW])\b(.*$)', re.IGNORECASE)
abutted_direction_re = re.compile(r'([0-9]+)([NESW])', re.IGNORECASE)
possessive_re = re.compile(r'\'\bs\b', re.IGNORECASE)
ave_street_re = re.compile(r'^[NESW] Street$', re.IGNORECASE)
period_first_re = re.compile(r'^\.')

direction_abbr_map = {
    'N': "North",
    'n': "North",
    'E': "East",
    'e': "East",
    'S': "South",
    's': "South",
    'W': "West",
    'w': "West"
}

def clean_slc_raw_data(raw_map_data):
    for node in raw_map_data['nodes']:
        for tag in node['tags']:
            if is_street_addr(tag['k']):
                tag['v'] = process_slc_addr(tag['v'])

    for node in raw_map_data['ways']:
        for tag in node['tags']:
            if is_street_addr(tag['k']):
                tag['v'] = process_slc_addr(tag['v'])
                
    for node in raw_map_data['relations']:
        for tag in node['tags']:
            if is_street_addr(tag['k']):
                tag['v'] = process_slc_addr(tag['v'])

    return raw_map_data

def process_slc_addr(addr):
    
    if ave_street_re.search(addr):
        # Avenue addresses have names that look like abbreviations but aren't. Nothing to do here.
        return addr

    elif direction_abbr_re.search(addr) or abutted_direction_re.search(addr):
        # address an issue where our regex for determining an abbreviated South is catching possessive names.
        # e.g. Saint Mary's Drive should not be changed to Saint Mary'South Drive
        has_possessive = False
        if possessive_re.search(addr):
            has_possessive = True
            addr = addr.replace("'", "&quot")

        # separate any abutted street directions
        while abutted_direction_re.search(addr):
            addr = space_split(addr, abutted_direction_re)
        
        # Fix all directional abbreviations in the address.
        while direction_abbr_re.search(addr):
            addr = expand_abbr(addr, direction_abbr_re, direction_abbr_map)

        # The other half of fixing possessive names
        if has_possessive:
            addr = addr.replace("&quot", "'")

        return addr

    else:
        return addr

# abbr_re is expected to be a regex with 3 match groups:
# 1: everything before the abbreviation (head)
# 2: the abbreviation
# 3: everything after the abbreviation (tail)
def expand_abbr(org_string, abbr_re, expand_map):
    str_sections = abbr_re.search(org_string)
    head = str_sections.group(1)
    expanded = expand_map[str_sections.group(2)]
    
    # Drop any periods left over from the abbreviation
    if period_first_re.search(str_sections.group(3)):
        tail = str_sections.group(3)[1:]
    else:
        tail = str_sections.group(3)

    return head + expanded + tail

# split_re is expected to be a 2 group regex.
# the 2 groups will be returned separated by a space.
def space_split(org_string, split_re):
    matches = split_re.search(org_string)
    out_string = matches.group(1) + " " + matches.group(2)
    return out_string

def is_street_addr(street):
    is_street = addr_street_re.search(street)
    is_house = addr_house_re.search(street)
    return (is_street or is_house)

def test(infile = "map"):
    raw_map_data = m2m.get_osm_map_data(infile)
    cln_map_data = clean_slc_raw_data(raw_map_data)
    m2m.load_osm_map_data(cln_map_data, 'localhost', 27017, 'salt_lake_city_clean')

if __name__ == "__main__":
    test()