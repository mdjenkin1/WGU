# OpenStreetMap Data Case Study - Salt Lake City, Utah

## Overview

In this case study, I have used Python and MongoDB to investigate the structure of XML Data from the Open Street Map Project (OSM). After investigation of XML metadata, further investigation was done into the uniformity of the data.

### Area Of Investigation

The area chosen for investigation is my home city of Salt Lake City, Utah. This area was chosen as I have some familiarity with the area's addressing and landmarks.  

Salt Lake City addresses its streets using a direction based grid system. At the center of the grid, is the LDS Temple. The address provides a distance as a number of city blocks times 100 and a direction of travel away from the temple. For example, 350 East would be three and a half city blocks East of the LDS Temple. The address portions describing the direction of travel away from the LDS Temple will be referred to as "directionals".

The map data was obtained from [https://www.openstreetmap.org/](https://www.openstreetmap.org/). From this site, I performed a search for "Salt Lake City". The first item in the search results was selected as the area of interest. From here, I went to the data's export page. A direct link to this export page has been provided below. Due to the size of the data set, I found it best to utilize the prepared Overpass API source.

Salt Lake City, Utah, United States  
[https://www.openstreetmap.org/export#map=12/40.7765/-111.9206](https://www.openstreetmap.org/export#map=12/40.7765/-111.9206)

Overpass API data source  
[https://overpass-api.de/api/map?bbox=-112.1155,40.6387,-111.7255,40.9140](https://overpass-api.de/api/map?bbox=-112.1155,40.6387,-111.7255,40.9140)

This provided a map dataset approximately 105mb in size.  

```PowerShell
λ  gci map

Directory: C:\Users\mdjen\Documents\GitHub\WGU\C750-MongoDB


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----       10/15/2018   5:40 AM      108017568 map
```

### Included Scripts

The follow list of scripts were used to perform the data investigation. A brief description of each script has been provided. These scripts were written and tested with Python 3.7.

* [element_getter.py](.\element_getter.py): provides a method of element iteration that serves full elements.
* [describe_xml.py](.\describe_xml.py): generates meta-data about an XML data structure.
* [xml_desc_to_mongo.py](.\xml_desc_to_mongo.py): loads the meta-data from describe_xml.py to MongoDB for investigation
* [xml_metadata_inquiries.py](xml_metadata_inquiries.py): A collection of functions for making investigations of xml descriptions.
* [map_to_mongo.py](.\map_to_mongo.py): loads unaltered OSM data to mongodb.
* [slc_street_cleanup.py](.\slc_street_cleanup.py): produces uniform street and house number addressing and loads it to mongodb.

### Questions Asked / Problem Areas

This exploration of XML data from the OSM Project proceeded through many phases. In each phase of exploration a different aspect of the dataset was explored. The following questions were asked and problem areas identified during the exploration.

* XML Metadata Investigation
  * How are XML files constructed?
  * How the elements that comprise XML documents be described?
  * What elements exist within an OSM XML dataset?
  * What are the relationships between elements in the dataset?
  * Which elements show properties that might require cleaning?
* OSM XML Data Investigation

## Investigation

### Parsing and Collecting XML Metadata

To begin my investigation, I took the stance of someone that has no foreknowledge of OSM data. This approach allowed me to view the data in a method of discovery that can be applied to completely foreign data sets. The first step in this discovery process was to obtain information about the XML schema used to structure the data.

XML at its most basic is a structured collection of elements. Therefore, we can structure a description of XML as a list of element descriptions.  

Elements can be described by their name, attributes, text and what elements are nested in them. Element names are unique for each element type. Although elements of the same name do not necessarily need to have the same attributes, nested elements or text. For the other element aspects, we're not interested in actual values yet. We are interested in the data types stored in those aspects.  

This leads to the following data structures for storing XML Metadata.

#### XML Description structure

    {
        elements:[  
            {elem1},  
            ...,  
            {elemN}  
        ]
    }

#### Element Description Structure

    {  
        name: string  
        attribs: {attrib_name:[types...], ...},  
        nested_elements: [types...],  
        text: [types...]  
    }

The reason for targeting metadata in these data structures is for ease of loading it to a MongoDB engine. The describe_xml.py script was written specifically to generate XML metadata in this format. As a companion script, xml_desc_to_mongo.py was created to facilitate the loading of XML metadata to a local MongoDB instance.  

 Structure of data storage was a consideration when writing xml_desc_to_mongo.py. The load_xml_desc_to_mongo method will store the metadata of whichever xml document you pass it into the collection you name. By default, that collection will be stored in a database named "xml_descriptions". The intent is "xml_descriptions" will serve as a library of XML metadata well into the future.

### Investigating OSM XML Metadata

After running xml_desc_to_mongo.py, the metadata was generated and loaded to my local MongoDB engine. There was nothing to do but start investigating. So I fired up a MongoDB client and opened the newly populated xml_descriptions database.


    C:\Users\mdjen>mongo
    MongoDB shell version v4.0.2
    connecting to: mongodb://127.0.0.1:27017
    MongoDB server version: 4.0.2

    > use xml_descriptions
    switched to db xml_descriptions
    >


To begin my investigation, I took a quick look at the metadata in its entirety.

    > db.osm_map.find()
    { "_id" : ObjectId("5bd9aed24aa1033ccc473753"), "name" : "note", "attribs" : null, "nested_elements" : null, "text" : [ "str" ] }
    { "_id" : ObjectId("5bd9aed24aa1033ccc473754"), "name" : "meta", "attribs" : { "osm_base" : [ "datetime" ] }, "nested_elements" : null, "text" : [ null ] }
    { "_id" : ObjectId("5bd9aed24aa1033ccc473755"), "name" : "bounds", "attribs" : { "minlat" : [ "float" ], "minlon" : [ "float" ], "maxlat" : [ "float" ], "maxlon" : [ "float" ] }, "nested_elements" : null, "text" : [ null ] }
    { "_id" : ObjectId("5bd9aed24aa1033ccc473756"), "name" : "node", "attribs" : { "id" : [ "int" ], "lat" : [ "float" ], "lon" : [ "float" ], "version" : [ "int" ], "timestamp" : [ "datetime" ], "changeset" : [ "int" ], "uid" : [ "int" ], "user" : [ "str" ] }, "nested_elements" : [ "tag" ], "text" : [ null, "str" ] }
    { "_id" : ObjectId("5bd9aed24aa1033ccc473757"), "name" : "tag", "attribs" : { "k" : [ "str" ], "v" : [ "str", "datetime", "float", "int" ] }, "nested_elements" : null, "text" : [ null ] }
    { "_id" : ObjectId("5bd9aed24aa1033ccc473758"), "name" : "nd", "attribs" : { "ref" : [ "int" ] }, "nested_elements" : null, "text" : [ null ] }
    { "_id" : ObjectId("5bd9aed24aa1033ccc473759"), "name" : "way", "attribs" : { "id" : [ "int" ], "version" : [ "int" ], "timestamp" : [ "datetime" ], "changeset" : [ "int" ], "uid" : [ "int" ], "user" : [ "str" ] }, "nested_elements" : [ "tag", "nd" ], "text" : [ "str" ] }
    { "_id" : ObjectId("5bd9aed24aa1033ccc47375a"), "name" : "member", "attribs" : { "type" : [ "str" ], "ref" : [ "int" ], "role" : [ "str" ] }, "nested_elements" : null, "text" : [ null ] }
    { "_id" : ObjectId("5bd9aed24aa1033ccc47375b"), "name" : "relation", "attribs" : { "id" : [ "int" ], "version" : [ "int" ], "timestamp" : [ "datetime" ], "changeset" : [ "int" ], "uid" : [ "int" ], "user" : [ "str" ] }, "nested_elements" : [ "member", "tag" ], "text" : [ "str" ] }
    { "_id" : ObjectId("5bd9aed24aa1033ccc47375c"), "name" : "osm", "attribs" : null, "nested_elements" : null, "text" : [ null ] }
    >

What I'm looking for are any values that don't make sense. For instance, the 'v' attribute of the tag element has a variety of data types. This suggests a type of generic element that describes a variety of data or an element that has an attribute in need of cleaning. Context suggests the former. Either way, when it comes time to investigate actual data, it would be beneficial to investigate the data types stored in tag elements.  

Also noted are no elements nested in tag elements. However, tag elements are nested in relation, way and node elements. This may be easier to see by limiting the fields returned by our query.

    > db.osm_map.find({}, {"_id":0, "name":1, "nested_elements":1})
    { "name" : "note", "nested_elements" : null }
    { "name" : "meta", "nested_elements" : null }
    { "name" : "bounds", "nested_elements" : null }
    { "name" : "node", "nested_elements" : [ "tag" ] }
    { "name" : "tag", "nested_elements" : null }
    { "name" : "nd", "nested_elements" : null }
    { "name" : "way", "nested_elements" : [ "tag", "nd" ] }
    { "name" : "member", "nested_elements" : null }
    { "name" : "relation", "nested_elements" : [ "member", "tag" ] }
    { "name" : "osm", "nested_elements" : null }
    >

Looking at the values for nested_elements, I notice there are elements that are not nested in other elements and do not have nested elements. It would be valuable to have a query that identifies such elements.

To create that query, I first found a list of all element tags

    > db.osm_map.aggregate([{$project: {"_id": "$name"}}])
    { "_id" : "note" }
    { "_id" : "meta" }
    { "_id" : "bounds" }
    { "_id" : "node" }
    { "_id" : "tag" }
    { "_id" : "nd" }
    { "_id" : "way" }
    { "_id" : "member" }
    { "_id" : "relation" }
    { "_id" : "osm" }
    >

I then found all elements with nested_elements.

    > db.osm_map.aggregate([{$match: {"nested_elements": {$ne: null}}}, {$group: {"_id": "$name"}}])
    { "_id" : "way" }
    { "_id" : "relation" }
    { "_id" : "node" }
    >

Next, I found all elements that are nested_elements.

    > db.osm_map.aggregate([{$match: {"nested_elements": {$ne: null}}}, {$unwind: "$nested_elements"}, {$group: {"_id": "$nested_elements"}}])
    { "_id" : "member" }
    { "_id" : "nd" }
    { "_id" : "tag" }
    >

It was at this point I hit a limitation of the MongoDB engine that doesn't exist in a traditional SQL based database. There is no way to perform a set operation on multiple aggregation results within the MongoDB client. To work around this limitation, I returned to Python to combine the queries into the dataset I wanted.

    λ  python .\xml_metadata_inquiries.py
    These are the elements that have no nested elements and are not nested elements.
    {'note', 'meta', 'bounds', 'osm'}

*Note: When converting the queries from the Mongo Client to Python Script, it was necessary to encase the aggregation operators in quotes and replace the nulls with Nones.*

### OSM Data Investigation

Investigation of OSM XML metadata directed me to look closer at nested tag elements. To get a good look at the tag data, I first needed to extract actual data from the OSM file. As only way, relation and node elements have nested tags, the extract was limited to these elements.


## Additional Ideas

* Update the loading scripts to enable writing to remote MongoDB engines.
* Update the loading scripts to merge instead of append datasets.
* Valid name abbreviations could be mistaken as abbreviations for street directions by our regex. Additional logic may be necessary to prevent this in other use cases. An investigation of our current data set shows this logic is unnecessary for now.
* The current attitude towards tiger data speaks nothing about its state in the dataset. Is there any value in determining the current state of that data and cleaning as necessary?

## Conclusion

MongoDB is a powerful engine for manipulating and investigating structured data. Although it does have its limitations.
Python and MongoDB are powerful tools for data manipulation.