# Script for UD-CPOV POC  

This script should :  
1. Load tileset.json  
2. Extract information to compile versions and versionTransitions  
3. Create a new tileset.json with the versions and versionTransitions data  

## Hypothesis :  
 * Versions exist at a precise date (ex : 2009) so their startDate equal their endDate
 * A building is in its source state until the transaction is over then it is in its destination state. 
  
## Requirement :  
See the requirement inside the file "requirement.txt"  
You can install them with the command `pip install -r requirement.txt` 

## Execution :  
To execute the script, follow the requirement and then execute  "compute_versiondata_from_py3dfiles.py"

## Data :  
You can find the input data in the "data" folder :  
* tileset.json
* json schema (*.schema.json)  

The output file is named "new_tilset.json".  

## Shortcoming :  
We can't be sure to have all bulding ids reference in the version because   
if a building don't have any transactions, i assume it will not be present there.  