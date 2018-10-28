"""
Load OSM data to MongoDB
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
from pymongo import MongoClient
import xml.etree.cElementTree as ET
import pprint

def get_osm_map_data(infile):
    # Prepare return structures
    nodes = []
    ways = []
    relations = []
    
    # Due to the nature of start/end events...
    # We will capture previous element data when encountering a new element of the same type.
    # To do this, we need to start with null elements of the expected types
    parsed_node = None
    parsed_way = None
    parsed_relation = None
    
    for _, elem in ET.iterparse(infile, events=("start",)):
        if elem.tag == "node":
            if parsed_node:
                nodes.append(parsed_node)
            parsed_node = parse_node_elem(elem)
        if elem.tag == "way":
            if parsed_way:
                ways.append(parsed_way)
            parsed_way = parse_way_elem(elem)
        if elem.tag == "relation":
            if parsed_relation:
                relations.append(parsed_relation)
            parsed_relation = parse_relation_elem(elem)
    
    # Explicitly capture the last elements encountered.
    # We need to do this as there's not another start event to trigger a capture
    nodes.append(parsed_node)
    ways.append(parsed_way)
    relations.append(parsed_relation)

    # Package elements for delivery and deliver
    map_data = {
        'nodes': nodes,
        'ways': ways,
        'relations': relations
    }
    return map_data

def parse_node_elem(elem):
    parsed_node = {"type": "node", "tags": []}
    for key in elem.keys():
        parsed_node[key] = elem.attrib[key]
    for tag in elem.iter("tag"):
        parsed_node["tags"].append({"k": tag.attrib["k"], "v": tag.attrib["v"]})
    return parsed_node

def parse_way_elem(elem):
    parsed_way = {"type": "way", "tags": [], "nd_ref": []}
    for key in elem.keys():
        parsed_way[key] = elem.attrib[key]
    for tag in elem.iter("tag"):
        parsed_way["tags"].append({"k": tag.attrib["k"], "v": tag.attrib["v"]})
    for nd in elem.iter("nd"):
        parsed_way["nd_ref"].append(nd.attrib["ref"])
    return parsed_way

def parse_relation_elem(elem):
    parsed_relation = {"type" : "relation", "tags": [], "members": []}
    for key in elem.keys():
        parsed_relation[key] = elem.attrib[key]
    for mem in elem.iter("member"):
        parsed_relation["members"].append({"type": mem.attrib["type"], "ref": mem.attrib["ref"], "role": mem.attrib["role"]})
        pass
    for tag in elem.iter("tag"):
        parsed_relation["tags"].append({"k": tag.attrib["k"], "v": tag.attrib["v"]})
    return parsed_relation

def load_osm_map_data(data, host, port, db_name):
    client = MongoClient(host, port)
    db = client[db_name]
    db['nodes'].insert_many(data['nodes'])
    db['ways'].insert_many(data['ways'])
    db['relations'].insert_many(data['relations'])

def test(infile, db_name):
    map_data = get_osm_map_data(infile)
    load_osm_map_data(map_data, 'localhost', 27017, 'salt_lake_city_raw')

if __name__ == "__main__":
    test('map', 'salt_lake_city_raw')