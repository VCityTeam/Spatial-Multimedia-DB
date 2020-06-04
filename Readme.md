# UD-Serv

UD-Serv is a collection of server-side tools for converting and analysing urban data.

Note: for the client-side components [refer to UD-Viz](https://github.com/VCityTeam/UD-Viz/).

## Available tools

### API_Enhanced_City
The goal of the 
[API **Enhanced City**](https://github.com/MEPP-team/UD-Serv/blob/master/API_Enhanced_City) 
is to handle, and serve through [web services](https://en.wikipedia.org/wiki/Web_service), 
various types of city related data in the context of 
[UD-SV (Urban Data Services and Vizualisation)](https://github.com/VCityTeam/UD-SV). 

The API currently offers [web service](https://en.wikipedia.org/wiki/Web_service) 
access to few following types of resources :
- Documents (file and metadata)
- Guided tours (sequences of documents with additional texts)
- Links between documents and other (city) objects
- User accounts and rights

### City 3DTiles tilers
3DTiles, as 
[described by Cesium](https://cesium.com/blog/2015/08/10/introducing-3d-tiles/), 
is an open specification for streaming massive heterogeneous 3D 
geospatial datasets. 
UD-Serv offers different kinds of "3DTiles tilers" that take a set of 
CityGML files (version 2.0, XML format) and processes them to yield
3DTiles tilesets. 
For example
[ComputeLyon3DTilesTemporal](https://github.com/VCityTeam/UD-Reproducibility/tree/master/Computations/ComputeLyon3DTilesTemporal)
is a processing pipeline that yields 3D Tiles tilesets extended 
with the temporal extension and capturing the evolutive range of 
the city of Lyon accross various data snapshot vintages ranging 
from 2009 to 2015.

### ExtractCityData
The [ExtractCityData tool](ExtractCityData) allows to process a 
[3DCityDB](https://www.3dcitydb.org/3dcitydb/3dcitydbhomepage/)  
database in order to create a materialized view of buildings (encountered in
the database) constituted by their building id, their geometry and optionnally
their year of construction and year of demolition.

### CityGML utility scripts
Some modest helpers, working at the CityGML (version 2.0) file level like: 
 - [CityGML2Stripper](Utils/CityGML2Stripper/) strips a CityGML (XML)file from
   its "appearences" and generic attributes and serializes the result back
   into a new CityGML (XML) file.
 - [CityGMLBuildingBlender](Utils/CityGMLBuildingBlender/) takes a set 
   of CityGML input files, collects all their buildings and gathers them
   within a single CityGML resulting file.
