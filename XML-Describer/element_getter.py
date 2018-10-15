"""
Obtain structure data about provided xml. 
What elements exist in the XML?
What types of values are assigned to 
What elements contain nested elements?

Element Description structure
{
        name: string
        attribs: {attrib_name:set(types...)},
        nested_elements: set(),
        is_root = boolean
}

XML Description structure:
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
import sys
import pprint
from datetime import datetime as dt

# element getter from course case study data.py
# This is used to provide full elements, with their nested children for parsing
# logic added to return all tags unless a set of tags are requested
def get_element(filename, tags=None):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(filename, events=('start', 'end'))
    _, root = next(context)

    for event, elem in context:
        if event == 'end':
            yield elem
            root.clear()

def test(infile = 'map.small.snip'):
    for element in get_element(infile):
        pprint.pprint(element)

if __name__ == "__main__":
    if len(sys.argv[1:]) >= 1:
        for infile in sys.argv[1:]:
            test(infile)
    else:
        test('map.small.snip')