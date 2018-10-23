"""
Load OSM data to a local MongoDB
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
    # parse elements from file
    nodes = []
    ways = []
    relations = []
    new_node = None
    new_way = None
    new_relation = None
    
    for _, elem in ET.iterparse(infile, events=("start",)):
        if elem.tag == "node":
            if new_node:
                nodes.append(new_node)
            new_node = {"type": "node", "tags": []}
            for key in elem.keys():
                new_node[key] = elem.attrib[key]
            for tag in elem.iter("tag"):
                new_node["tags"].append({"k": tag.attrib["k"], "v": tag.attrib["v"]})
    nodes.append(new_node)

    for _, elem in ET.iterparse(infile, events=("start",)):
        if elem.tag == "way":
            if new_way:
                ways.append(new_way)
            new_way = {"type": "way", "tags": [], "nd_ref": []}
            for key in elem.keys():
                new_way[key] = elem.attrib[key]
            for tag in elem.iter("tag"):
                new_way["tags"].append({"k": tag.attrib["k"], "v": tag.attrib["v"]})
            for nd in elem.iter("nd"):
                new_way["nd_ref"].append(nd.attrib["ref"])
    ways.append(new_way)

    for _, elem in ET.iterparse(infile, events=("start",)):
        if elem.tag == "relation":
            if new_relation:
                relations.append(new_relation)
            new_relation = {"type" : "relation", "tags": [], "members": []}
            for key in elem.keys():
                new_relation[key] = elem.attrib[key]
            for mem in elem.iter("member"):
                new_relation["members"].append({"type": mem.attrib["type"], "ref": mem.attrib["ref"], "role": mem.attrib["role"]})
                pass
            for tag in elem.iter("tag"):
                new_relation["tags"].append({"k": tag.attrib["k"], "v": tag.attrib["v"]})
    relations.append(new_relation)

    map_data = {
        'nodes': nodes,
        'ways': ways,
        'relations': relations
    }
    return map_data

def load_osm_map_data(data, host, port, db_name):
    client = MongoClient(host, port)
    db = client[db_name]
    db['nodes'].insert_many(data['nodes'])
    db['ways'].insert_many(data['ways'])
    db['relations'].insert_many(data['relations'])

def load_file(infile, db_name = 'salt_lake_city_raw'):
    map_data = get_osm_map_data(infile)
    load_osm_map_data(map_data, 'localhost', 27017, db_name)

if __name__ == "__main__":
    load_file(infile = 'map')