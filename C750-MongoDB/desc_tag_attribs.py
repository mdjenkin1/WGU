"""
OSM data investigation
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
import element_getter as EG
import pprint

def update_attrib_list(attrib_list, k, v):
    #print("{} : {}".format(k, v))
    not_updated = True
    while not_updated:
        for attr in attrib_list:
            if attr['k'] == k:
                #print('updating {} with {}'.format(k, v))
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
    for element in EG.get_element(infile):
    #    pprint.pprint(element)
        if 'k' in element.attrib.keys():
        #   print(element.attrib['k'])
            if 'v' in element.attrib.keys():
                attrib_list = update_attrib_list(attrib_list, element.attrib['k'], element.attrib['v'])
            else:
                print("XML issue key {} does not have a value".format(element.attrib['k']))
    #pprint.pprint(attrib_list)
    return attrib_list

def test(infile = 'map'):
    get_tag_attrib_list(infile)

if __name__ == "__main__":
    pprint.pprint(test('map'))