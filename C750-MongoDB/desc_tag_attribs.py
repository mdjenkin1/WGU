"""
Created for OSM data investigation
'k' attributes only exist in tags.
Tags only exist in Nodes, Ways, and Relations.
Which 'k' attributes exist for each parent tag type?

'k' attributes are paired with 'v' attributes.
For 'v' attributes paired to the 'k' attributes, what value types do they contain.

answer these questions with the following data structure:
[
    {
        'k': <value>,
        'v': [<type>, <type>]
    },
    ...
]
"""
import element_getter as eg
import sys
import pprint

def update_attrib_list(attrib_list, k, v):
    not_updated = True
    while not_updated:
        for attr in attrib_list:
            if attr['k'] == k:
                attr['v'].append(v)
                attr['v'] = set(attr['v'])
                attr['v'] = list(attr['v'])
                not_updated = False
        if not_updated:
            attrib_list.append({'k': k, 'v': [v]})
            not_updated = False
    return attrib_list

def get_tag_attrib_list(infile = 'map'):
    attrib_list = []
    for element in eg.get_element(infile):
        if 'k' in element.attrib.keys():
            if 'v' in element.attrib.keys():
                attrib_list = update_attrib_list(attrib_list, element.attrib['k'], element.attrib['v'])
            else:
                print("XML issue key {} does not have a value".format(element.attrib['k']))
    return attrib_list

if __name__ == "__main__":
    if len(sys.argv[1:]) >= 1:
        for infile in sys.argv[1:]:
            pprint.pprint(get_tag_attrib_list(infile))
    else:
        pprint.pprint(get_tag_attrib_list('map'))