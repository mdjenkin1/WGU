"""
Obtain structure data about provided xml. 
What elements exist in the XML?
What types of values are assigned to 
What elements contain nested elements?

Element Description structure:
{
    name: string
    attribs: {attrib_name:set(types...)},
    nested_elements: set(),
    text: set()
}

XML Description structure:
{
    elements:[
        {elem1}
        ...,
        {elemn}
    ]
}
"""

import xml.etree.cElementTree as ET
import element_getter as eg
import copy
import sys
import pprint
from datetime import datetime as dt

xml_description = {'skipped':[], 'elements':[]}

# Returns a dict of all tag names found in our xml doc with a count of the tag's occurrence 
def get_elem_type_counts(filename):
    elem_types = {}
    for _, elem in ET.iterparse(filename):
        elem_types[elem.tag] = elem_types.get(elem.tag, 0) + 1
    return elem_types

# Primary function for scraping values to describe an element
def get_elem_desc(elem):
    desc_elem = {
        'name': elem.tag,
        'attribs': {}, 
        'nested_elements': set(),
        'text' : set()
    }

    # Populate the types of attributes with 
    for key in elem.keys():
        attrib_types = set()
        if elem.attrib[key]:
            attrib_types.add(guess_type(elem.attrib[key]))
        desc_elem['attribs'].update({key : attrib_types})
    if len(desc_elem['attribs']) == 0:
        desc_elem['attribs'] = None

    for child in elem:
        desc_elem['nested_elements'].add(child.tag)
    if len(desc_elem['nested_elements']) == 0:
        desc_elem['nested_elements'] = None

    desc_elem['text'].add(guess_type(elem.text))

    return desc_elem

# Take an assumed string value and guess at its type.
# do nothing for nothing
# if it will convert to an int then it's probably an int
# if it will convert to a float then it's probably a float
# if it will cast as a Datetime, then it's probably a datetime
# failing all that, it's must be a string.
def guess_type(test_value):
    if test_value:
        try:
            int(test_value)
            guess = 'int'
        except ValueError:
            try:
                float(test_value)
                guess = 'float'
            except ValueError:
                try:
                    #2018-02-05T03:43:12Z
                    dt.strptime(test_value, '%Y-%m-%dT%H:%M:%SZ')
                    guess = 'datetime'
                except:
                    guess = 'str'
        finally:
            return guess
    else:
        return None

def merge_elem(elem_orig, new_elem):
    # Return boolean in addition to the modified element
    # This is to let us know if there's change to the original element.
    has_change = False

    # merge the attribute list
    if elem_orig['attribs'] != new_elem['attribs']:
        for key, val in new_elem['attribs'].items():
            if elem_orig['attribs'] == None:
                elem_orig['attribs'] = {key: val}
                has_change = True
            elif key in elem_orig['attribs'].keys():
                numTypes = len(elem_orig['attribs'][key])
                elem_orig['attribs'][key].update(val)
                if numTypes != len(elem_orig['attribs'][key]):
                    has_change = True
            else:
                elem_orig['attribs'].update({key: val})
                has_change = True

    # Merge the nested elements sets
    # First check if there's new elements to add
    # If not, do nothing
    if not (new_elem['nested_elements'] == None):
        # if there are not elements in the old set, then the new set is the complete set
        if (elem_orig['nested_elements'] == None):
            elem_orig['nested_elements'] = new_elem['nested_elements']
            has_change = True
        # if there's elements in both sets, check if the new set is a subset of the old set.
        # if it is, then merge the two sets.
        # if not, do nothing
        elif not new_elem['nested_elements'].issubset(elem_orig['nested_elements']):
            elem_orig['nested_elements'].update(new_elem['nested_elements'])
            has_change = True

    # Merge the text type sets following the same logic used for nested elements
    if not (new_elem['text'] == None):
        if (elem_orig['text'] == None):
            elem_orig['text'] = new_elem['text']
            has_change = True
        elif not new_elem['text'].issubset(elem_orig['text']):
            elem_orig['text'].update(new_elem['text'])
            has_change = True

    return elem_orig, has_change

def get_xml_description(filename):
    elem_types = get_elem_type_counts(filename)

    # Using a dictionary for xml descriptions even though there's only element descriptions for now.
    # This is in consideration for future expansion of our xml_descriptions 
    xml_desc = {'elements':[]}

    for element in eg.get_element(filename):
            new_elem = get_elem_desc(element)
            
            # Determine if we've encountered this element type before.
            # If no, add it.
            # Otherwise, check if ther's any change if the new and existing are merged
            existing_elem_desc = list(filter(lambda e: e['name'] == new_elem['name'], xml_desc['elements']))
            if len(existing_elem_desc) == 0:
                xml_desc['elements'].append(new_elem)
            else:
                for elem in existing_elem_desc:
                    merged_elem, has_change = merge_elem(elem, new_elem)
                    if has_change:
                        # To update our list of elements:
                        # Make a copy of the current list minus the modified element
                        # Add the modified element to the copy
                        # Replace the old list with the new list
                        new_elem_list = []
                        new_elem_list[:] = [x for x in xml_desc['elements'] if not (x.get('name') == new_elem['name'])]
                        new_elem_list.append(merged_elem)
                        xml_desc.pop('elements', None)
                        xml_desc.update({'elements': new_elem_list})

    # Convert sets to lists as MongoDB doesn't have a mapping for python sets
    for element in xml_desc['elements']:
        if element['nested_elements'] is not None:
            element['nested_elements'] = list(element['nested_elements'])
        if element['attribs'] is not None:
            for key, val in element['attribs'].items():
                element['attribs'][key] = list(val)
        if element['text'] is not None:
            element['text'] = list(element['text'])

    return xml_desc

def test(infile = 'map'):
    xml_desc = get_xml_description(infile)
    pprint.pprint(xml_desc)

if __name__ == "__main__":
    if len(sys.argv[1:]) >= 1:
        for infile in sys.argv[1:]:
            test(infile)
    else:
        test('map')