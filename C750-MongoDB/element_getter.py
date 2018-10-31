"""
element getter from X750-MongoDB course case study data.py
This provides parseable full elements, including nested children
Modified to return all tags unless a subset of tags are requested
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
        test()