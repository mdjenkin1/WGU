
## C750-MongoDB

### Open Street Map Data Project Files.

_note: pymongo is required for this project._

* [describe_xml.py](.\describe_xml.py): gets meta-data about the structure of XML data.
* [element_getter.py](.\element_getter.py): provides method of element iteration by serving full elements.
* [map_to_mongo.py](.\map_to_mongo.py): loads unaltered OSM data to mongodb.
* [OSM_Case_Study.md](.\OSM_Case_Study.md): Markdown version of the project report
* [slc_street_cleanup.py](.\C750-MongoDB\slc_street_cleanup.py): produces uniform street and house number addressing and loads it to mongodb.
* [xml_desc_to_mongo.py](.\xml_desc_to_mongo.py): loads the meta-data from describe_xml.py to Mongodb for investigation
* [xml_metadata_inquiries.py](.\xml_metadata_inquiries.py): A collection of scripts for investigating XML metadata generated and stored by the xml_desc_to_mongo.py script

A copy of this project is available on GitHub at: [https://github.com/mdjenkin1/WGU/tree/master/C750-MongoDB](https://github.com/mdjenkin1/WGU/tree/master/C750-MongoDB)