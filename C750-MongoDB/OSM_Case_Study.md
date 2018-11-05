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

```json
{
    elements:[  
        {elem1},  
        ...,  
        {elemN}  
    ]
}
```

#### Element Description Structure

```json
{  
    name: string  
    attribs: {attrib_name:[types...], ...},  
    nested_elements: [types...],  
    text: [types...]  
}
```

The reason for targeting metadata in these data structures is for ease of loading it to a MongoDB engine. The describe_xml.py script was written specifically to generate XML metadata in this format. As a companion script, xml_desc_to_mongo.py was created to facilitate the loading of XML metadata to a local MongoDB instance.  

 Structure of data storage was a consideration when writing xml_desc_to_mongo.py. The load_xml_desc_to_mongo method will store the metadata of whichever xml document you pass it into the collection you name. By default, that collection will be stored in a database named "xml_descriptions". The intent is "xml_descriptions" will serve as a library of XML metadata well into the future.

### Investigating OSM XML Metadata

After running xml_desc_to_mongo.py, the metadata was generated and loaded to my local MongoDB engine. There was nothing to do but start investigating. So I fired up a MongoDB client and opened the newly populated xml_descriptions database.


    C:\Users>mongo
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

```
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
```

Looking at the values for nested_elements, I notice there are elements that are not nested in other elements and do not have nested elements. It would be valuable to have a query that identifies such elements.

To create that query, I first found a list of all element tags

```
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
```

I then found all elements with nested_elements.

```
> db.osm_map.aggregate([{$match: {"nested_elements": {$ne: null}}}, {$group: {"_id": "$name"}}])
{ "_id" : "way" }
{ "_id" : "relation" }
{ "_id" : "node" }
>
```

Next, I found all elements that are nested_elements.

```
> db.osm_map.aggregate([{$match: {"nested_elements": {$ne: null}}}, {$unwind: "$nested_elements"}, {$group: {"_id": "$nested_elements"}}])
{ "_id" : "member" }
{ "_id" : "nd" }
{ "_id" : "tag" }
>
```

It was at this point I hit a limitation of the MongoDB engine that doesn't exist in a traditional SQL based database. There is no way to perform a set operation on multiple aggregation results within the MongoDB client. To work around this limitation, I returned to Python to combine the queries into the dataset I wanted.

```
λ  python .\xml_metadata_inquiries.py
These are the elements that have no nested elements and are not nested elements.
{'note', 'meta', 'bounds', 'osm'}
```

*Note: When converting the queries from the Mongo Client to Python Script, it was necessary to encase the aggregation operators in quotes and replace the nulls with Nones.*

### OSM Data Investigation

Investigation of OSM XML metadata directed me to look closer at nested tag elements. To get a good look at the tag data, I first needed to extract actual data from the OSM file. As only the way, relation and node elements have nested elements, the extract was limited to these elements. To facilitate the extract map_to_mongo.py was created. The first step was to determine how to structure our element data.

#### Structuring Data For Investigating

When structuring the actual data, I saw no reason to deviate too far from the structure of the metadata. The base structure would remain the same. Instead of value types, I would store actual values. Instead of one entry to describe all elements of and encountered type, there would be one entry per encountered element. Nested elements needed a bit more to describe. This is one area that could do with more iteration.

To handle nested elements, I decided to store them directly to the parent element as a list of element descriptions. The limitation here was needing a different structure for the three element types being saved. This design requires functions specific for handling the individual element types being handled. I can't help but think there is some way to address this divergence from data structuring. Ultimately, I determined such an exercise is out of scope for this project and must be tabled for future design. I therefore settled on the following data structures to describe our three element types.

```json
nodes: [{
    type: "node"
    id: value,
    lat: value,
    lon: value,
    version: value,
    timestamp: value,
    changeset: value,
    uid: value,
    user: value,
    tags: [
        {"k": k_value, "v": v_value},
        ...
    ],
    text: value
}]

ways: [{
    type: "way"
    id: value,
    version: value,
    timestamp: value,
    changeset: value,
    uid: value,
    user: value,
    tags: [
        {"k": k_value, "v": v_value},
        ...
    ]
    nd_ref:[
        value
    ],
    text: value
}]

relations: [{
    type: "relation"
    id: value,
    version: value,
    timestamp: value,
    changeset: value,
    uid: value,
    user: value,
    tags: [
        {"k": k_value, "v": v_value},
        ...
    ]
    members:[
        {type: value,
        ref: value,
        role: value},
    ],
    text: value
}]
```

To maintain uniformity when loading data to the MongoDB engine, each element type was loaded to its own collection.

#### Raw Data

With it settled on how to structure the data, it was now time to parse the XML and load it to MongoDB. The map_to_mongo.py script did the heavy lifting for this task. With a loaded database and Mongo client, I was now prepared to investigate the data set.

##### Tag Type Counts
First thing, I took a look at is how many tags actually exist in the dataset.

```
> db.ways.aggregate([{$unwind: "$tags"}, {$project: {"tag_key": "tags.k"}}, {$group: {"_id": "$tag_key", "count": {$sum: 1}}}, {"$sort": {"count" : -1}}])
{ "_id" : "tags.k", "count" : 472374 }
> db.nodes.aggregate([{$unwind: "$tags"}, {$project: {"tag_key": "tags.k"}}, {$group: {"_id": "$tag_key", "count": {$sum: 1}}}, {"$sort": {"count" : -1}}])
{ "_id" : "tags.k", "count" : 46414 }
> db.relations.aggregate([{$unwind: "$tags"}, {$project: {"tag_key": "tags.k"}}, {$group: {"_id": "$tag_key", "count": {$sum: 1}}}, {"$sort": {"count" : -1}}])
{ "_id" : "tags.k", "count" : 3160 }
>
```

For every tag in the relations data, there's more than ten in the node data. There's also ten times as many tags in way data as there is in node data. With so few tags in relation data, it might be best to see what its most common tag types are.

```
> db.relations.aggregate([{$unwind: "$tags"}, {$project: {"tag_key": "$tags.k"}}, {$group: {"_id": "$tag_key", "count": {$sum: 1}}}, {"$sort": {"count" : -1}}]).pretty()
{ "_id" : "type", "count" : 1017 }
{ "_id" : "restriction", "count" : 733 }
{ "_id" : "name", "count" : 130 }
{ "_id" : "building", "count" : 91 }
{ "_id" : "route", "count" : 70 }
{ "_id" : "ref", "count" : 61 }
{ "_id" : "public_transport:version", "count" : 46 }
{ "_id" : "network", "count" : 46 }
{ "_id" : "natural", "count" : 38 }
{ "_id" : "wikidata", "count" : 36 }
{ "_id" : "operator", "count" : 35 }
{ "_id" : "from", "count" : 30 }
{ "_id" : "addr:street", "count" : 29 }
{ "_id" : "addr:postcode", "count" : 29 }
{ "_id" : "addr:housenumber", "count" : 29 }
{ "_id" : "addr:city", "count" : 29 }
{ "_id" : "to", "count" : 29 }
{ "_id" : "wikipedia", "count" : 26 }
{ "_id" : "addr:state", "count" : 24 }
{ "_id" : "boundary", "count" : 21 }
Type "it" for more
>
```

Approximately a third of the tags in relations being of type "type", is a curious thing. This suggests a case for an nested element that might be better served as an attribute. For now, we're instead going to look at the most common tags in node and way elements.

```
> db.nodes.aggregate([{$unwind: "$tags"}, {$project: {"tag_key": "$tags.k"}}, {$group: {"_id": "$tag_key", "count": {$sum: 1}}}, {"$sort": {"count" : -1}}]).pretty()
{ "_id" : "highway", "count" : 4985 }
{ "_id" : "name", "count" : 3995 }
{ "_id" : "emergency", "count" : 3598 }
{ "_id" : "ele", "count" : 2434 }
{ "_id" : "amenity", "count" : 1999 }
{ "_id" : "natural", "count" : 1908 }
{ "_id" : "crossing", "count" : 1309 }
{ "_id" : "railway", "count" : 1265 }
{ "_id" : "gnis:Class", "count" : 1249 }
{ "_id" : "gnis:County", "count" : 1248 }
{ "_id" : "gnis:County_num", "count" : 1243 }
{ "_id" : "gnis:ST_alpha", "count" : 1241 }
{ "_id" : "gnis:ST_num", "count" : 1238 }
{ "_id" : "gnis:id", "count" : 1235 }
{ "_id" : "import_uuid", "count" : 1230 }
{ "_id" : "is_in", "count" : 1209 }
{ "_id" : "source", "count" : 1156 }
{ "_id" : "place", "count" : 1044 }
{ "_id" : "power", "count" : 946 }
{ "_id" : "time", "count" : 776 }
Type "it" for more
> it
{ "_id" : "shop", "count" : 674 }
{ "_id" : "cuisine", "count" : 522 }
{ "_id" : "addr:street", "count" : 486 }
{ "_id" : "addr:housenumber", "count" : 478 }
{ "_id" : "gnis:feature_id", "count" : 396 }
{ "_id" : "barrier", "count" : 385 }
{ "_id" : "addr:city", "count" : 366 }
{ "_id" : "gnis:created", "count" : 361 }
{ "_id" : "gnis:county_id", "count" : 349 }
{ "_id" : "gnis:state_id", "count" : 346 }
{ "_id" : "addr:postcode", "count" : 334 }
{ "_id" : "operator", "count" : 309 }
{ "_id" : "addr:state", "count" : 304 }
{ "_id" : "building", "count" : 276 }
{ "_id" : "religion", "count" : 228 }
{ "_id" : "ref", "count" : 221 }
{ "_id" : "denomination", "count" : 188 }
{ "_id" : "opening_hours", "count" : 184 }
{ "_id" : "website", "count" : 178 }
{ "_id" : "access", "count" : 165 }
Type "it" for more
>
```

Node tag data is more diverse in it's key values. Highway is the most common type of node tag and makes up little more than one tenth of all node tags.

```
> db.ways.aggregate([{$unwind: "$tags"}, {$project: {"tag_key": "$tags.k"}}, {$group: {"_id": "$tag_key", "count": {$sum: 1}}}, {"$sort": {"count" : -1}}]).pretty()
{ "_id" : "building", "count" : 87344 }
{ "_id" : "addr:housenumber", "count" : 35200 }
{ "_id" : "addr:postcode", "count" : 35100 }
{ "_id" : "addr:street", "count" : 35072 }
{ "_id" : "addr:city", "count" : 34179 }
{ "_id" : "addr:state", "count" : 33683 }
{ "_id" : "utahagrc:parcelid", "count" : 31214 }
{ "_id" : "highway", "count" : 29062 }
{ "_id" : "name", "count" : 16757 }
{ "_id" : "tiger:county", "count" : 10504 }
{ "_id" : "tiger:cfcc", "count" : 10392 }
{ "_id" : "tiger:name_base", "count" : 9872 }
{ "_id" : "tiger:reviewed", "count" : 9256 }
{ "_id" : "tiger:name_type", "count" : 5947 }
{ "_id" : "tiger:name_direction_prefix", "count" : 5314 }
{ "_id" : "surface", "count" : 5129 }
{ "_id" : "tiger:name_base_1", "count" : 3986 }
{ "_id" : "name:full", "count" : 3870 }
{ "_id" : "name:prefix", "count" : 3743 }
{ "_id" : "service", "count" : 3571 }
Type "it" for more
>
```

Way tags, like relation tags, are a more lopsided. The most common way tag type is building and accounts for approximately 20 percent of all way tags. 

##### Tiger Data

One type of way tag that I found curious are the "tiger:" tags. There seems to be an awful lot of them.

```
> db.ways.aggregate([{$unwind: "$tags"}, {$project: {"tag_key": "$tags.k", "tag_value": "$tags.v"}}, {"$match": {"tag_key": {$regex: "^tiger"}}}, {$group: {"_id": "$tag_key", "count": {$sum: 1}}}, {"$sort": {"count" : -1}}])
{ "_id" : "tiger:county", "count" : 10504 }
{ "_id" : "tiger:cfcc", "count" : 10392 }
{ "_id" : "tiger:name_base", "count" : 9872 }
{ "_id" : "tiger:reviewed", "count" : 9256 }
{ "_id" : "tiger:name_type", "count" : 5947 }
{ "_id" : "tiger:name_direction_prefix", "count" : 5314 }
{ "_id" : "tiger:name_base_1", "count" : 3986 }
{ "_id" : "tiger:name_direction_suffix", "count" : 2883 }
{ "_id" : "tiger:name_direction_prefix_1", "count" : 2579 }
{ "_id" : "tiger:name_direction_suffix_1", "count" : 1688 }
{ "_id" : "tiger:name_type_1", "count" : 1138 }
{ "_id" : "tiger:name_base_2", "count" : 899 }
{ "_id" : "tiger:name_direction_prefix_2", "count" : 682 }
{ "_id" : "tiger:tlid", "count" : 426 }
{ "_id" : "tiger:source", "count" : 426 }
{ "_id" : "tiger:separated", "count" : 399 }
{ "_id" : "tiger:upload_uuid", "count" : 258 }
{ "_id" : "tiger:name_type_2", "count" : 255 }
{ "_id" : "tiger:name_base_3", "count" : 213 }
{ "_id" : "tiger:name_direction_suffix_2", "count" : 190 }
Type "it" for more
>
```

Some of these Tiger tags have intuitive types. Others not so much. Maybe a quick look at the values of the "tiger:cfcc" tags will be helpful.

```
> db.ways.aggregate([{$unwind: "$tags"}, {$project: {"tag_key": "$tags.k", "tag_value": "$tags.v"}}, {"$match": {"tag_key": {$regex: "^tiger:cfcc$"}}}, {$group: {"_id": "$tag_value", "count": {$sum: 1}}}, {"$sort": {"count" : -1}}])
{ "_id" : "A41", "count" : 9485 }
{ "_id" : "A21", "count" : 356 }
{ "_id" : "A31", "count" : 179 }
{ "_id" : "A63", "count" : 132 }
{ "_id" : "A11", "count" : 94 }
{ "_id" : "A74", "count" : 67 }
{ "_id" : "B11", "count" : 26 }
{ "_id" : "A15", "count" : 18 }
{ "_id" : "A73", "count" : 10 }
{ "_id" : "B11;B21", "count" : 4 }
{ "_id" : "A25", "count" : 4 }
{ "_id" : "A31:A33", "count" : 3 }
{ "_id" : "A39", "count" : 3 }
{ "_id" : "A31;A41", "count" : 2 }
{ "_id" : "A45", "count" : 2 }
{ "_id" : "A31:A41", "count" : 2 }
{ "_id" : "A15:A63", "count" : 2 }
{ "_id" : "A51", "count" : 2 }
{ "_id" : "C10", "count" : 1 }
>
```

Nope, not helpful at all. That query only left me with more questions. So it's time to take to the internet and find out what the situation is on Tiger data. A quick search and I found answers: [https://wiki.openstreetmap.org/wiki/TIGER](https://wiki.openstreetmap.org/wiki/TIGER)  

Based on the information found in the OSM wiki, Tiger data is a prime candidate for cleaning. There's even a communal effort documenting known issues and methods for correcting it. As is, there's already quite a bit of automation to clean tiger data. Current efforts for cleaning imported Tiger data is of the manual type. Researching the import automation and manual cleaning of Tiger is out of scope for this project.

##### Street Abbreviation Investigation.

A better exercise, in scope with this course, is the addressing of Salt Lake City. Having lived my entire life in Salt Lake, I've found it curious how differently other cities manage addresses. In Salt Lake City, the house and street address can be broken further into two parts; a number and a direction. In other words, Salt Lake uses a coordinate system. Each number and directional combination describes how many blocks, in which direction away from the Mormon temple the address is. To avoid the need of decimals, city blocks are numbered as hundreds. As an example, 200 South is a street that runs East/West and is 2 blocks South of the Mormon Temple. 450 East is half a block between 400 East and 500 East.

What I expect has happened with OSM data is a mixing of directional abbreviations in both house and street addresses. It's common for people to provide a single letter for the directional rather than the full word when handing out an address. As there are "addr:housenumber" and "addr:street" tags exist in all of our parent element types, It would also be a good exercise for applying uniform data cleanup to different data loads.

```
> db.ways.aggregate([{$unwind: "$tags"}, {$match: {$or: [{"tags.k": /^addr:str/},{"tags.k": /^addr:hou/}]}}, {$group: {"_id": "tags.k", "count": {$sum: 1}}}])
{ "_id" : "tags.k", "count" : 70296 }
> db.nodes.aggregate([{$unwind: "$tags"}, {$match: {$or: [{"tags.k": /^addr:str/},{"tags.k": /^addr:hou/}]}}, {$group: {"_id": "tags.k", "count": {$sum: 1}}}])
{ "_id" : "tags.k", "count" : 973 }
> db.relations.aggregate([{$unwind: "$tags"}, {$match: {$or: [{"tags.k": /^addr:str/},{"tags.k": /^addr:hou/}]}}, {$group: {"_id": "tags.k", "count": {$sum: 1}}}])
{ "_id" : "tags.k", "count" : 58 }
>
```

A straight count shows the way elements account for a disproportionate number of all street and housenumber address tags. It doesn't tell us how many are using abbreviated directionals.

```
> db.ways.aggregate([{$unwind: "$tags"}, {$match: {$or: [{"tags.k": /^addr:str/},{"tags.k": /^addr:hou/}]}}, {$match: {$and: [{"tags.v": /\b[NESWnesw]\b/}]}}, {$group: {"_id": "tags.k", "count": {$sum: 1}}}])
{ "_id" : "tags.k", "count" : 473 }
> db.nodes.aggregate([{$unwind: "$tags"}, {$match: {$or: [{"tags.k": /^addr:str/},{"tags.k": /^addr:hou/}]}}, {$match: {$and: [{"tags.v": /\b[NESWnesw]\b/}]}}, {$group: {"_id": "tags.k", "count": {$sum: 1}}}])
{ "_id" : "tags.k", "count" : 109 }
> db.relations.aggregate([{$unwind: "$tags"}, {$match: {$or: [{"tags.k": /^addr:str/},{"tags.k": /^addr:hou/}]}}, {$match: {$and: [{"tags.v": /\b[NESWnesw]\b/}]}}, {$group: {"_id": "tags.k", "count": {$sum: 1}}}])
{ "_id" : "tags.k", "count" : 7 }
>
>
```

These numbers are much more manageable, but we haven't yet looked for false positives.

```
> db.ways.aggregate([{$unwind: "$tags"}, {$match: {$or: [{"tags.k": /^addr:str/},{"tags.k": /^addr:hou/}]}}, {$match: {$and: [{"tags.v": /\b[NESWnesw]\b/}]}}, {$project: {"addr": "$tags.v"}}])
{ "_id" : ObjectId("5bdf759186e7792414502bda"), "addr" : "300 N" }
{ "_id" : ObjectId("5bdf759186e7792414502d3e"), "addr" : "239 S Main St" }
{ "_id" : ObjectId("5bdf759186e7792414502e31"), "addr" : "S 1400 East" }
{ "_id" : ObjectId("5bdf759186e7792414502e32"), "addr" : "S 1400 East" }
{ "_id" : ObjectId("5bdf759186e7792414502e36"), "addr" : "S 1400 East" }
{ "_id" : ObjectId("5bdf759186e7792414502e3b"), "addr" : "S 1452 East" }
{ "_id" : ObjectId("5bdf759186e7792414502e87"), "addr" : "N Terrace Hills Drive" }
{ "_id" : ObjectId("5bdf759186e7792414503bc9"), "addr" : "720 N" }
{ "_id" : ObjectId("5bdf759186e77924145040a0"), "addr" : "3289 E" }
{ "_id" : ObjectId("5bdf759186e779241450418c"), "addr" : "2354 S" }
{ "_id" : ObjectId("5bdf759186e779241450418d"), "addr" : "2309 S" }
{ "_id" : ObjectId("5bdf759186e7792414504190"), "addr" : "2375 S" }
{ "_id" : ObjectId("5bdf759186e77924145041ad"), "addr" : "23 E" }
{ "_id" : ObjectId("5bdf759186e77924145041af"), "addr" : "2120 S" }
{ "_id" : ObjectId("5bdf759186e77924145041b4"), "addr" : "2200 S" }
{ "_id" : ObjectId("5bdf759186e77924145041be"), "addr" : "2101 S" }
{ "_id" : ObjectId("5bdf759186e779241450444a"), "addr" : "1255 W" }
{ "_id" : ObjectId("5bdf759186e7792414504b2e"), "addr" : "1840 S" }
{ "_id" : ObjectId("5bdf759186e7792414504c4b"), "addr" : "361/363 N" }
{ "_id" : ObjectId("5bdf759186e7792414504cf4"), "addr" : "4400 S 700 E" }
Type "it" for more
> db.nodes.aggregate([{$unwind: "$tags"}, {$match: {$or: [{"tags.k": /^addr:str/},{"tags.k": /^addr:hou/}]}}, {$match: {$and: [{"tags.v": /\b[NESWnesw]\b/}]}}, {$project: {"addr": "$tags.v"}}])
{ "_id" : ObjectId("5bdf758286e779241442a3b6"), "addr" : "4408 S" }
{ "_id" : ObjectId("5bdf758286e77924144390e6"), "addr" : "2100 S" }
{ "_id" : ObjectId("5bdf758286e779241443985e"), "addr" : "1264 W" }
{ "_id" : ObjectId("5bdf758386e779241444024c"), "addr" : "2211 W" }
{ "_id" : ObjectId("5bdf758386e779241444024c"), "addr" : "2300 S" }
{ "_id" : ObjectId("5bdf758386e779241444024d"), "addr" : "2211 W" }
{ "_id" : ObjectId("5bdf758386e779241444024d"), "addr" : "2300 S" }
{ "_id" : ObjectId("5bdf758386e779241444048f"), "addr" : "W 400 S" }
{ "_id" : ObjectId("5bdf758386e7792414440673"), "addr" : "1320 E." }
{ "_id" : ObjectId("5bdf758386e7792414442834"), "addr" : "344  S" }
{ "_id" : ObjectId("5bdf758386e7792414443b9b"), "addr" : "895 E 4500 S" }
{ "_id" : ObjectId("5bdf758386e7792414444e5d"), "addr" : "3167 E" }
{ "_id" : ObjectId("5bdf758386e7792414448094"), "addr" : "28 S" }
{ "_id" : ObjectId("5bdf758386e77924144482a5"), "addr" : "2227 S" }
{ "_id" : ObjectId("5bdf758386e7792414448593"), "addr" : "1854 S" }
{ "_id" : ObjectId("5bdf758386e7792414448593"), "addr" : "1955 W" }
{ "_id" : ObjectId("5bdf758386e77924144485cb"), "addr" : "836 W" }
{ "_id" : ObjectId("5bdf758386e77924144485cb"), "addr" : "1100 N" }
{ "_id" : ObjectId("5bdf758386e7792414448643"), "addr" : "1309 S" }
{ "_id" : ObjectId("5bdf758386e7792414448b5f"), "addr" : "307 W 600 S" }
Type "it" for more
> db.relations.aggregate([{$unwind: "$tags"}, {$match: {$or: [{"tags.k": /^addr:str/},{"tags.k": /^addr:hou/}]}}, {$match: {$and: [{"tags.v": /\b[NESWnesw]\b/}]}}, {$project: {"addr": "$tags.v"}}])
{ "_id" : ObjectId("5bdf759586e779241451f349"), "addr" : "2210 E" }
{ "_id" : ObjectId("5bdf759586e779241451f34a"), "addr" : "2170 E" }
{ "_id" : ObjectId("5bdf759586e779241451f34b"), "addr" : "2251 E" }
{ "_id" : ObjectId("5bdf759586e779241451f34c"), "addr" : "2159 E" }
{ "_id" : ObjectId("5bdf759586e779241451f34e"), "addr" : "463 S" }
{ "_id" : ObjectId("5bdf759586e779241451f35d"), "addr" : "200 E" }
{ "_id" : ObjectId("5bdf759586e779241451f35e"), "addr" : "307 E" }
>
```

The initial selection looks good. However, false positives can be hiding in deeper . Grabbing a few more entries from the way elements, we've found our first false positives. It appears our regex is improperly retrieving possessives. 

```
{ "_id" : ObjectId("5bdf759186e7792414504f08"), "addr" : "Carl's Jr." }
...
{ "_id" : ObjectId("5bdf759186e779241450f928"), "addr" : "Saint Mary's Drive" }
{ "_id" : ObjectId("5bdf759186e779241450f92a"), "addr" : "Saint Mary's Drive" }
{ "_id" : ObjectId("5bdf759186e779241450f92b"), "addr" : "Saint Mary's Drive" }
{ "_id" : ObjectId("5bdf759186e779241450f92c"), "addr" : "Saint Mary's Drive" }
{ "_id" : ObjectId("5bdf759186e779241450f92d"), "addr" : "Saint Mary's Drive" }
{ "_id" : ObjectId("5bdf759186e779241450f92e"), "addr" : "Saint Mary's Drive" }
{ "_id" : ObjectId("5bdf759186e779241450f92f"), "addr" : "Saint Mary's Drive" }
{ "_id" : ObjectId("5bdf759186e779241450f930"), "addr" : "Saint Mary's Drive" }
```

Not satisfied that we've found all the false positives, I continue my scan of the hits retrieved. My diligence is met with success. There are streets in an area known as 'The Avenues'. The streets running North and South in 'The Avenues' are named with letters. Some of these streets have been caught in our search.

```
{ "_id" : ObjectId("5bdf759186e779241451780c"), "addr" : "N Street" }
{ "_id" : ObjectId("5bdf759186e779241451781c"), "addr" : "N Street" }
{ "_id" : ObjectId("5bdf759186e7792414517826"), "addr" : "S Street" }
{ "_id" : ObjectId("5bdf759186e7792414517835"), "addr" : "N Street" }
{ "_id" : ObjectId("5bdf759186e77924145178a6"), "addr" : "S Street" }
{ "_id" : ObjectId("5bdf759186e77924145178b4"), "addr" : "N Street" }
```

Finishing our scan for false positives doesn't find any more. There's now enough information to modify our selection of values to clean by excluding our false positives. Adding the exclusions to our query provides the latest counts.

```
> db.ways.aggregate([{$unwind: "$tags"}, {$match: {$or: [{"tags.k": /^addr:str/},{"tags.k": /^addr:hou/}]}}, {$match: {$and: [{"tags.v": /\b[NESWnesw]\b/}, {"tags.v": {$not: /[NESWnesw] Street$/}}, {"tags.v": {$not: /'[NESWnesw]/}}]}}, {$group: {"_id": "tags.k", "count": {$sum: 1}}}])
{ "_id" : "tags.k", "count" : 206 }
> db.nodes.aggregate([{$unwind: "$tags"}, {$match: {$or: [{"tags.k": /^addr:str/},{"tags.k": /^addr:hou/}]}}, {$match: {$and: [{"tags.v": /\b[NESWnesw]\b/}, {"tags.v": {$not: /[NESWnesw] Street$/}}, {"tags.v": {$not: /'[NESWnesw]/}}]}}, {$group: {"_id": "tags.k", "count": {$sum: 1}}}])
{ "_id" : "tags.k", "count" : 108 }
> db.relations.aggregate([{$unwind: "$tags"}, {$match: {$or: [{"tags.k": /^addr:str/},{"tags.k": /^addr:hou/}]}}, {$match: {$and: [{"tags.v": /\b[NESWnesw]\b/}, {"tags.v": {$not: /[NESWnesw] Street$/}}, {"tags.v": {$not: /'[NESWnesw]/}}]}}, {$group: {"_id": "tags.k", "count": {$sum: 1}}}])
{ "_id" : "tags.k", "count" : 7 }
>
```

It's worth noting that there are abbreviated directionals utilizing periods. These will also need to be handled when it comes time to clean the data.

Another consideration are abbreviations that are abutted to the number portion of the address. These will need to be separated from the number with a space and expanded. 

There is one decision to make in regards to expanding the directional abbreviations, casing. Should the directionals be all caps or title cased? I think it best to follow what is most common in the unmodified dataset. A quick look into the way tags shows there is only one all caps entry in the nodes dataset. The convention is to use title case for the directionals.

```
> db.ways.aggregate([{$unwind: "$tags"}, {$match: {$or: [{"tags.k": /^addr:str/},{"tags.k": /^addr:hou/}]}}, {$match: {$and: [{"tags.v": /\bSouth|North|East|West\b/}]}}, {$group: {"_id": "tags.k", "count": {$sum: 1}}}])
{ "_id" : "tags.k", "count" : 11294 }
> db.nodes.aggregate([{$unwind: "$tags"}, {$match: {$or: [{"tags.k": /^addr:str/},{"tags.k": /^addr:hou/}]}}, {$match: {$and: [{"tags.v": /\bSouth|North|East|West\b/}]}}, {$group: {"_id": "tags.k", "count": {$sum: 1}}}])
{ "_id" : "tags.k", "count" : 353 }
> db.relations.aggregate([{$unwind: "$tags"}, {$match: {$or: [{"tags.k": /^addr:str/},{"tags.k": /^addr:hou/}]}}, {$match: {$and: [{"tags.v": /\bSouth|North|East|West\b/}]}}, {$group: {"_id": "tags.k", "count": {$sum: 1}}}])
{ "_id" : "tags.k", "count" : 21 }
> db.ways.aggregate([{$unwind: "$tags"}, {$match: {$or: [{"tags.k": /^addr:str/},{"tags.k": /^addr:hou/}]}}, {$match: {$and: [{"tags.v": /\bSOUTH|NORTH|EAST|WEST\b/}]}}, {$group: {"_id": "tags.k", "count": {$sum: 1}}}])
> db.nodes.aggregate([{$unwind: "$tags"}, {$match: {$or: [{"tags.k": /^addr:str/},{"tags.k": /^addr:hou/}]}}, {$match: {$and: [{"tags.v": /\bSOUTH|NORTH|EAST|WEST\b/}]}}, {$group: {"_id": "tags.k", "count": {$sum: 1}}}])
{ "_id" : "tags.k", "count" : 1 }
> db.relations.aggregate([{$unwind: "$tags"}, {$match: {$or: [{"tags.k": /^addr:str/},{"tags.k": /^addr:hou/}]}}, {$match: {$and: [{"tags.v": /\bSOUTH|NORTH|EAST|WEST\b/}]}}, {$group: {"_id": "tags.k", "count": {$sum: 1}}}])
>
```

##### Street Abbreviation Clean Up

Now that we have an idea of what addressing data exists and plan on how to clean it, there's nothing left to do but do it. Extracting and loading the data is something we've solved with the map_to_mongo.py script. I could reinvent those processes. Instead, I've expanded on them with the transformation script: slc_street_cleanup.py. Running this script produces a new, cleaner dataset with expanded street directionals.

```
> db.ways.aggregate([{$unwind: "$tags"}, {$match: {$or: [{"tags.k": /^addr:str/},{"tags.k": /^addr:hou/}]}}, {$match: {$and: [{"tags.v": /\bSouth|North|East|West\b/}]}}, {$group: {"_id": "tags.k", "count": {$sum: 1}}}])
{ "_id" : "tags.k", "count" : 11914 }
> db.nodes.aggregate([{$unwind: "$tags"}, {$match: {$or: [{"tags.k": /^addr:str/},{"tags.k": /^addr:hou/}]}}, {$match: {$and: [{"tags.v": /\bSouth|North|East|West\b/}]}}, {$group: {"_id": "tags.k", "count": {$sum: 1}}}])
{ "_id" : "tags.k", "count" : 498 }
> db.relations.aggregate([{$unwind: "$tags"}, {$match: {$or: [{"tags.k": /^addr:str/},{"tags.k": /^addr:hou/}]}}, {$match: {$and: [{"tags.v": /\bSouth|North|East|West\b/}]}}, {$group: {"_id": "tags.k", "count": {$sum: 1}}}])
{ "_id" : "tags.k", "count" : 28 }
>
```

## Additional Ideas

* Update the loading scripts to enable writing to remote MongoDB engines.
* Update the loading scripts to merge instead of append datasets.
* Investigate the nested element "type" tags of relation elements for abstraction.
* Valid name abbreviations could be mistaken as abbreviations for street directions by our regex. Additional logic may be necessary to prevent this in other use cases. An investigation of our current data set shows this logic is unnecessary for now.
* Investigate how Tiger data is currently being cleaned and imported. 

## Conclusion

MongoDB is a powerful engine for manipulating and investigating structured data. Although it does have its limitations.
Python and MongoDB are powerful tools for data manipulation.