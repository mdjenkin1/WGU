# OpenStreetMap Data Case Study

## Map Area

[Salt Lake City, Utah, United States](https://www.openstreetmap.org/export#map=12/40.7765/-111.9206)

## Data Overview

XML Description data here

* [element_getter.py](.\$1): provides method of element iteration by serving full elements.
* [describe_xml.py](.\$1): gets meta-data about the structure of XML data.
* [desc_tag_attribs.py](.\$1): restructures tag data to facilitate investigation of value consistency.
* [xml_desc_to_mongo.py](.\$1): loads the meta-data from describe_xml.py to Mongodb for investigation
* [tag_attr_desc_to_mongo.py](.\$1): loads the structured tag data from desc_tag_attribs.py to Mongodb for investigation
* [map_to_mongo.py](.\$1): loads unaltered OSM data to mongodb.
* [slc_street_cleanup.py](.\$1): produces uniform street and house number addressing and loads it to mongodb.

## Questions Asked / Problem Areas

* What elements exist within that file?
* What attributes do those elements have?
* What data types are found for those attributes?
* Which elements are nested?
* What tag values exist?
* Which tags values are used the most?
* What is 'tiger:' data?
* How common is it for address data to be entered with abbreviated directionals?
* Which casing of address directionals is most used?
* Finally, make street address directionals uniform.

## Additional Ideas

* Valid name abbreviations could be mistaken as abbreviations for street directions by our regex. Additional logic may be necessary to prevent this in other use cases. An investigation of our current data set shows this logic is unnecessary for now.

## Conclusion

Python and MongoDB are powerful tools for data manipulation.