"""
Load OSM data to a local MongoDB
node data:
{
    type: "node"
    id: value,
    lat: value,
    lon: value,
    version: value,
    timestamp: value,
    changeset: value,
    uid: value,
    user: value,
    tags:[
        {k_value: v_value}
    ]
}

way data:
{
    type: "way"
    id: value,
    version: value,
    timestamp: value,
    changeset: value,
    uid: value,
    user: value,
    tags:[
        {k_value: v_value}
    ]
    nd_ref:[
        value
    ]
}

relation data:
{
    type: "relation"
    id: value,
    version: value,
    timestamp: value,
    changeset: value,
    uid: value,
    user: value,
    tags:[
        {k_value: v_value}
    ]
    member:[
        {type: value,
        ref: value,
        role: value},
    ]
}

"""
import pymongo
import xml.etree.cElementTree as ET
import pprint

def load_file(infile):
    # parse elements from file
    nodes = []
    ways = []
    relations = []
    new_node = None
    new_way = None
    new_relation = None
    #for _, elem in ET.iterparse(infile, events=("start",)):
    #    if elem.tag in ("note","meta","bounds","osm",):
    #        print("skipping {}".format(elem.tag))
    for _, elem in ET.iterparse(infile, events=("start",)):
        if elem.tag == "node":
            if new_node:
                nodes.append(new_node)
            new_node = {"type": "node", "tags": []}
            for key in elem.keys():
                new_node[key] = elem.attrib[key]
            for tag in elem.iter("tag"):
                new_node["tags"].append({tag.attrib["v"]: tag.attrib["k"]})

    for _, elem in ET.iterparse(infile, events=("start",)):
        if elem.tag == "way":
            if new_way:
                ways.append(new_way)
            new_way = {"type": "way", "tags": [], "nd_ref": []}
            for key in elem.keys():
                new_way[key] = elem.attrib[key]
            for tag in elem.iter("tag"):
                new_way["tags"].append({tag.attrib["v"]: tag.attrib["k"]})
            for nd in elem.iter("nd"):
                new_way["nd_ref"].append(nd.attrib["ref"])

    for _, elem in ET.iterparse(infile, events=("start",)):
        if elem.tag == "relation":
            new_relation = {"type" : "relation", "tags": [], "members": []}
            for key in elem.keys():
                new_relation[key] = elem.attrib[key]
            for mem in elem.iter("member"):
                #new_relation.append({key : elem.attrib[key]})
                pass
            for tag in elem.iter("tag"):
                new_relation["tags"].append({tag.attrib["v"]: tag.attrib["k"]})
        #else:
        #    print("Unknown Element Found: {}".format(elem.tag))

    # add parse to mongoDB
    for node in nodes:
        if len(node["tags"]) > 0:
            pprint.pprint(node)
    pass

def test(infile):
    load_file(infile)

if __name__ == "__main__":
    test(infile = 'map')