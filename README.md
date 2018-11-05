# WGU

Tracking Projects done for completion of WGU programs

## C750-MongoDB

_note: pymongo is required for this project._

* [Project_Map.docx](.\C750-MongoDB\Project_Map.docx): project outline.
* [OSM_Case_Study.md](.\C750-MongoDB\OSM_Case_Study.md): Markdown version of the project report
* [element_getter.py](.\C750-MongoDB\element_getter.py): provides method of element iteration by serving full elements.
* [describe_xml.py](.\C750-MongoDB\describe_xml.py): gets meta-data about the structure of XML data.
* [xml_desc_to_mongo.py](.\C750-MongoDB\xml_desc_to_mongo.py): loads the meta-data from describe_xml.py to Mongodb for investigation
* [map_to_mongo.py](.\C750-MongoDB\map_to_mongo.py): loads unaltered OSM data to mongodb.
* [slc_street_cleanup.py](.\C750-MongoDB\slc_street_cleanup.py): produces uniform street and house number addressing and loads it to mongodb.

## XML-Describer

Originally C750-MongoDB. This project is now extra-curricular. Will be re-incorporated into the C750-MongoDB project as a dictionary for the XML data.

* [describe_xml.py](.\XML-Describer\describe_xml.py): Given an assumed valid XML file, provide a description of the Elements it contains
* [xml_desc_to_mongo.py](.\XML-Describer\xml_desc_to_mongo.py): wrapper for loading xml descriptions to MongoDB
* [investigate_xml_desc.py](.\XML-Describer\investigate_xml_desc.py): scrap of a script that doesn't do anything. Original Plan: generate a report on potential items of interest in the xml description.

## Trash

Items that didn't make it but don't deserve to be thrown away.

* [tag_attr_desc_to_mongo.py](.\C750-MongoDB\tag_attr_desc_to_mongo.py): loads the structured tag data from desc_tag_attribs.py to Mongodb for investigation
* [desc_tag_attribs.py](.\C750-MongoDB\desc_tag_attribs.py): restructures tag data to facilitate investigation of value consistency.

## Git Ignored Files

* map: XML from Open Street Map
* map.snip: a medium sized snip from the middle of map. (Don't forget to encase them in a root tag)
* map.small.snip: an extra small sized snip from map
* *.pyc: python cache files
* ~*.docx: Word cache files
* *.tmp: temporary files
