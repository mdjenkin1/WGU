# WGU

Tracking Projects done for completion of WGU programs

## C750-MongoDB

* Project_Map.docx: project outline.
* OSM_Case_Study.md: Markdown version of the project report
* desc_tag_attribs.py: OSM tag elements are using generic 'k', 'v' attributes to hold their data.
* element_getter.py: serves up full elements iteratively.

Lets get better information.

## XML-Describer

Originally C750-MongoDB. This project is now extra-curricular. Will be re-incorporated into the C750-MongoDB project as a dictionary for the XML data.

* describe_xml.py: Given an assumed valid XML file, provide a description of the Elements it contains
* xml_desc_to_mongo.py: wrapper for loading xml descriptions to MongoDB
* investigate_xml_desc.py: generate a report on potential items of interest in the xml description.
* map_to_mongo.py: load actual map information to local mongoDB.

## Git Ignored Files

* map: XML from Open Street Map [https://www.openstreetmap.org/export#map=12/40.7765/-111.9206](https://www.openstreetmap.org/export#map=12/40.7765/-111.9206)
* map.snip: a medium sized snip from the middle of map. (Don't forget to encase them in a root tag)
* map.small.snip: an extra small sized snip from map
* *.pyc: python cache files
* ~*.docx: Word cache files