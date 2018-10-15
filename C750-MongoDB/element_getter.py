"""
element getter from X750-MongoDB course case study data.py
This is used to provide full elements, with their nested children for parsing
logic added to return all tags unless a set of tags are requested
"""

import xml.etree.cElementTree as ET
import sys
import pprint

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