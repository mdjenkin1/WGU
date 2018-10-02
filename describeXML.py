"""
Obtain structure data about provided xml. 
What elements exist in the XML?
What types of values are assigned to 
What elements contain nested elements?

Base Element data structure
{
        name: string
        attrib: {attrib_name:set(types...)},
        nested_elements: set()
}

XML Describer structure:
{
    SkippedTags:[],
    elements:[
        {elem1}
        ...,
        {elemn}
    ]
}
"""

import xml.etree.cElementTree as ET
import copy
import pprint

#INFILE = 'map.small.snip'
INFILE = 'map'
xml_description = {'skipped':[], 'elements':[]}

# Returns a dict of all tag names found in our xml doc with a count of the tag's occurance 
def get_elem_types(filename):
    elem_types = {}
    for _, elem in ET.iterparse(filename):
        elem_types[elem.tag] = elem_types.get(elem.tag, 0) + 1
    return elem_types

# element getter from course case study data.py
# This is used to provide full elements, with their nested children for parsing
def get_element(osm_file, tags=None):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    if tags:
        limit_tags = True
    else:
        limit_tags = False

    for event, elem in context:
        if limit_tags:
            if event == 'end' and elem.tag in tags:
                yield elem
                root.clear()
        else:
            if event == 'end':
                yield elem
                root.clear()

# Primary function for scraping values to describe an element
def get_elem_desc(elem):
    desc_elem = {
        'name': elem.tag,
        'attrib': {}, #set(elem.keys()),
        'nested_elements': set()
    }
    if elem.tag == 'osm':
        pprint.pprint(elem)

    for key in elem.keys():
        attrib_types = set()
        if elem.attrib[key]:
            attrib_types.add(guess_type(elem.attrib[key]))


        desc_elem['attrib'].update({key : attrib_types})
        #print("key: {} value: {}".format(key,elem.attrib[key]))

    for child in elem:
        desc_elem['nested_elements'].add(child.tag)
    return desc_elem

# Take an assumed string value and guess at its type.
# if it will convert to an int then it's probably an int
# if it will convert to a float then it's probably a float
# failing all that, it's still a string.
def guess_type(test_value):
    try:
        int(test_value)
        guess = 'int'
    except ValueError:
        try:
            float(test_value)
            guess = 'float'
        except ValueError:
            guess = 'str'
    finally:
        return guess

def merge_elem(elem_orig, new_elem):
    has_change = False

    if elem_orig['attrib'] != new_elem['attrib']:
        for key, val in new_elem['attrib'].items():
            if key in elem_orig['attrib'].keys():
                elem_orig['attrib'][key].update(val)
            else:
                elem_orig['attrib'].update({key: val})
        has_change = True

    if not new_elem['nested_elements'].issubset(elem_orig['nested_elements']):
        elem_orig['nested_elements'].update(new_elem['nested_elements'])
        has_change = True

    return elem_orig, has_change

def get_xml_description(filename):
    elem_types = get_elem_types(filename)

    tagNames = []
    xml_desc = {'skipped':[], 'elements':[]}

    for key in elem_types:
        #print(key)
        # if there's only one of an element then we're not going parse it
        #if elem_types[key] > 1: 
        tagNames.append(key)
        #else:
        #    xml_desc['skipped'].append(key)

    #for element in get_element(filename, tagNames):
    for element in get_element(filename):
            new_elem = get_elem_desc(element)
            # Check if the new element already exists in the list of elements. 
            # If not, add it. 
            # Otherwise, merge it with the existing entry and update the element list.
            existing_elem_desc = list(filter(lambda e: e['name'] == new_elem['name'], xml_desc['elements']))
            if len(existing_elem_desc) == 0:
                print(new_elem['name'])
                xml_desc['elements'].append(new_elem)
            else:
                for elem in existing_elem_desc:
                    merged_elem, has_change = merge_elem(elem, new_elem)
                
                    if has_change:
                        new_elem_list = []
                        new_elem_list[:] = [x for x in xml_desc['elements'] if not (x.get('name') == new_elem['name'])]
                        new_elem_list.append(merged_elem)
                        xml_desc.pop('elements', None)
                        xml_desc.update({'elements': new_elem_list})

    return xml_desc

def test():
    xml_desc = get_xml_description(INFILE)
    pprint.pprint(xml_desc)

if __name__ == "__main__":
    test()