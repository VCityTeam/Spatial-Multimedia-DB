# -*- coding: utf-8 -*-
"""

@Author : Thibaut Chataing   
@Date : 12/05/2020
# Script for UD-CPOV POC

This script should :
1. Load tileset.json
2. Extract information to compile versions and versionTransitions
3. Create a new tileset.json with the versions and versionTransitions data

/!\ Requirement :
    pandas (use of dataframe)
    warlock (use to load json schema as template)
"""

import warlock
import argparse
import json
import os
import sys
import pandas as pd


debug = False # By default no log wanted

# Log for debugging purpose
def log(msg):
    if debug:
        print(msg)


# load data
# /!\ The list of transactions are expected to be found in extensions-3DTILES_temporal-transactions
def load_tilesetJSON():
    log("-- Load tileset.json --")
    list_transactions = []
    with open(os.path.join('.', 'data', 'tileset.json')) as json_file:
        data = json.load(json_file)
        startDate = data['extensions']['3DTILES_temporal']['startDate']
        endDate = data['extensions']['3DTILES_temporal']['endDate']
        list_transactions = data['extensions']['3DTILES_temporal']['transactions']

    log(f"startDate = {startDate} \nendDate = {endDate}\nlist_transactions = {list_transactions}")
    return list_transactions

def format_data(list_tr):
    log("-- Formate data --")
    transactions = pd.DataFrame(list_tr, columns=["id", "startDate", "endDate", "source", "destination", "type", "transactions"])

    #Auto detect of type
    transactions = transactions.convert_dtypes()

    log(f"Describe data : {transactions.describe(include=['string', 'Int64'])}")
    
    return transactions


"""
# Extracte from a DataFrame all the IDs of the batiment that should be present in the version.
# The extraction is based on the transactions (transformation of a building between two times)
# A version represents a year (ex: 2009, 2012, 2015)
# When a transactions start at or before the year and end after we take the source id
# When a transactions end at the year we take the destination id
#
# @Param:
#   transaction : DataFrame 
#   millesime : int (year)
# @return: a dictionnary with two set of features ids (unicity is guaranted)
#       "version" holds all buildings' id 
#       "versionTr" holds all transactions' id link to the current version
"""
def get_featuresid(transactions, millesime):
    log(f"-- Get features' ID for {millesime} --")
    ret = {"version":set(), "versionTr":set()}
    
    tr = transactions.loc[(transactions['startDate'] <= millesime) & (transactions['endDate'] > millesime)] # Filter only transactions that start in the millesime or before and end strictly after
    a = get(tr, "source", millesime)
    ret['version'].update(a['version'])
    ret['versionTr'].update(a['versionTr'])
    
    b = len(ret['version'])
    c = len(ret['versionTr'])
    log(f"simple tr : version= {b} - versionTR= {c}")
    
    tr = transactions.loc[(transactions['startDate'] < millesime) & (transactions['endDate'] == millesime)] # Filter only transactions that start striclty before the millesime  and end at it
    a = get(tr, "destination", millesime)
    ret['version'].update(a['version'])
    ret['versionTr'].update(a['versionTr'])
    
    log(f"agg tr : version= {len(ret['version']) - b} - versionTR= {len(ret['versionTr']) - c}")
    
    log(f"featuresIds found :  version= {len(ret['version'])} - versionTR= {len(ret['versionTr'])}")
    log(f"Details : {ret}")
    return ret


"""
# Iterrate on a Dataframe to extract id of transactions for the versionTransation and id of buildings for version
#
# @Param:
#   df : DataFrame
#   row_name : String row_name for the featuresId (ex: "source" or "destination") 
#   millesime : int (year)
# @return: a dictionnary {version:set, versionTr:set}
"""
def get(df, row_name, millesime):
    ret = {'version':set(), 'versionTr':set()} # set for batiment's id and transactions's id to have unicity
    for index, row in df.iterrows():
        ret['versionTr'].add(row['id'])
        for s in row[row_name]:
            ret['version'].add(s) #take the source
    
        if row['transactions']==row['transactions']: # separate simple and aggregate transactions (simple has NaN value in the transactions attribut)
            l = row['transactions']
            for tr in l:
                if (tr['startDate'] <= millesime < tr['endDate']) : # filter by security in the transaction aggregated
                    ret['versionTr'].add(tr['id'])
                    for s in tr['source']:
                        ret['version'].add(s)
                elif (tr['startDate'] < millesime == tr['endDate']):
                    ret['versionTr'].add(tr['id'])
                    for s in tr['destination']:
                        ret['version'].add(s)
    return ret



# Hardcoded creation of version and versionTransition
def compile_version_and_versionTr(transactions, version_path, versionTr_path):
    log("-- Compile version and versionTransition --")
    Version = 0
    VersionTransition = 0
    with open(schema_version_path) as json_file:
        data = json.load(json_file)
        Version = warlock.model_factory(data) # Create a class following the model provided by the json schema.
    
    with open(schema_versionTransition_path) as json_file:  
      data = json.load(json_file)
      VersionTransition = warlock.model_factory(data)

    v1 = Version(id="v1",
                 name="2009",
                 description="Limonest state in 2009 for the concurrent point of view",
                 startDate="2009",
                 endDate="2009",
                 tags=["concurrent"],
                 featuresIds=list(get_featuresid(transactions, 2009)['version']))
    
    v2 = Version(id="v2",
                 name="2012",
                 description="Limonest state in 2012 for the concurrent point of view",
                 startDate="2012",
                 endDate="2012",
                 tags=["concurrent"],
                 featuresIds=list(get_featuresid(transactions, 2012)['version']))
    
    v3 = Version(id="v3",
                 name="2015",
                 description="Limonest state in 2015 for the concurrent point of view",
                 startDate="2015",
                 endDate="2015",
                 tags=["concurrent"],
                 featuresIds=list(get_featuresid(transactions, 2015)['version']))
    
    vt_v1_v2 = VersionTransition({"id":"vt1", # attribut passed by a dictionnay because "from" already meaning something. To bypasse the interpretation of it we need to pass it has a string
                                 "name":"v1->v2",
                                 "startDate":"2009",
                                 "endDate":"2012",
                                 "from":"v1",
                                 "to":"v2",
                                 "description":"Transition between v1 and v2",
                                 "type":"realized",
                                 "transactionsIds":list(get_featuresid(transactions, 2009)['versionTr'])})
    
    vt_v2_v3 = VersionTransition({"id":"vt2",
                                 "name":"v2->v3",
                                 "startDate":"2012",
                                 "endDate":"2015",
                                 "from":"v2",
                                 "to":"v3",
                                 "description":"Transition between v2 and v3",
                                 "type":"realized",
                                 "transactionsIds":list(get_featuresid(transactions, 2012)['versionTr'])})
    return (v1, v2, v3, vt_v1_v2, vt_v2_v3)



if __name__ == "__main__":
    # arg parse
    descr = '''This script should :
1. Load tileset.json
2. Extract information to compile versions and versionTransitions
3. Create a new tileset.json with the versions and versionTransitions data'''
    parser = argparse.ArgumentParser(description=descr)

    debug_help = "Mode debug, adds multiple print info to help know what's happenning"
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help=debug_help)

    args = parser.parse_args()
    debug = args.debug
    if debug:
        log("Start with debug (an argument has been passed so debug is ON)")
    else:
        print("Start without debug")
        
    list_transactions = load_tilesetJSON()
    df_transactions = format_data(list_transactions)
    
    schema_version_path = os.path.join('.', 'data', '3DTILES_temporal.version.schema.schema.json')
    schema_versionTransition_path = os.path.join('.', 'data', '3DTILES_temporal.versionTransition.schema.json')

    (v1, v2, v3, vt_v1_v2, vt_v2_v3) = compile_version_and_versionTr(df_transactions, 
                                                                     schema_version_path, 
                                                                     schema_versionTransition_path)
    
    with open(os.path.join('.', 'data', 'tileset.json')) as json_file:
        data = json.load(json_file)

    data['extensions']['3DTILES_temporal']['versions'] = [v1, v2, v3]
    data['extensions']['3DTILES_temporal']['versionTransitions'] = [vt_v1_v2, vt_v2_v3]

    with open(os.path.join('.', 'data', 'new_tileset.json'), "w") as json_file:
        json.dump(data, json_file)

    print('done')
