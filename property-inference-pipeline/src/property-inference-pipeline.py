#!/usr/bin/env python
### V. Cedeno
### 06 jul 2017.
### Take experiment 1 output data
### and generate plot files.
### input files:
###     
### output files:
###      Users interaction plot
###     


### Modification History
### --------------------

import sys

import os
import csv
import operator
from datetime import time, datetime, timedelta
from itertools import cycle
import numpy as np
import datetime as dt
import time
import glob
import json
import validateJson
sys.path.insert(0, os.getcwd()+'/property-inference-pipeline/src/h1')
sys.path.insert(0, os.getcwd()+'/property-inference-pipeline/src/h2')

import h1Transformation
import h1
import h2Transformation
import h2

### -----------------------------
### Start.
def main():

    if (len(sys.argv) != 2):
    	print ("  Error.  Incorrect usage.")
    	print ("  usage: exec infile outfile.")
    	print ("  Halt.")
    	quit()
    
    configfile=sys.argv[1]
    json_file = open(configfile, 'r')
    json_data = json.load(json_file)
    numlines= (len(json_data))
    #for i in range(numlines):
    schemainputdata=os.getcwd()+'/jsonInputPipeline/schemas/property-inference-pipeline.json'
    inputdata=os.getcwd()+'/jsonInputPipeline/input/property-inference-pipeline.json'
    value=validateJson.validate(schemainputdata,inputdata)
    if value=='False':
    	sys.exit()
    functions=json_data["functions"]
    numlines= (len(functions))
    for i in range(numlines):
    	function=functions[i]["function"]
    	if function=='h1':
    		if os.path.exists(os.getcwd()+'/property-inference-pipeline/json-schema/inputTransformation/datasets/h1.json') and os.path.exists(os.getcwd()+'/property-inference-pipeline/json-schema/inputTransformation/schemas/h1.json'):
    			filename = os.getcwd()+'/property-inference-pipeline/json-schema/inputTransformation/datasets/h1.json'	
    			schemaname = os.getcwd()+'/property-inference-pipeline/json-schema/inputTransformation/schemas/h1.json'	
    			h1Transformation.main(filename,schemaname)
    		foldermodel=functions[i]["foldermodel"]
    		inputpath=os.getcwd()+'/property-inference-pipeline/json-schema/h1/input/datasets/'
    		filename="tsData.csv"
    		#print(groupslist)
    		h1.main(inputpath,filename,foldermodel)
    		#else:
    		#	print("No input of schema for h1")
    	if function=='h2':
    		groupslist=[]
    		groups=functions[i]["groups"]
    		numlinesgroups= (len(groups))
    		for ii in range(numlinesgroups):
    			groupslist.append([groups[ii]["n"],groups[ii]["d"]])
    		if os.path.exists(os.getcwd()+'/property-inference-pipeline/json-schema/inputTransformation/datasets/h1.json') and os.path.exists(os.getcwd()+'/property-inference-pipeline/json-schema/inputTransformation/schemas/h1.json'):
    			filename = os.getcwd()+'/property-inference-pipeline/json-schema/inputTransformation/datasets/h1.json'	
    			schemaname = os.getcwd()+'/property-inference-pipeline/json-schema/inputTransformation/schemas/h1.json'	
    			h2Transformation.main(filename,schemaname,groupslist)
    			inputpath=os.getcwd()+'/property-inference-pipeline/json-schema/h1/input/datasets/'
    			filename="tsData.csv"
    			h2.main(inputpath,filename,groupslist)
    		else:
    			print("No input of schema for h2")
 
    endTime=datetime.now()

    #print (" elapsed time (seconds): ",endTime-startTime)
    #print (" elapsed time (hours): ",(endTime-startTime)/3600.0)

    print (" -- good termination --")

    return	

## --------------------------
## Execution starts.
if __name__ == '__main__':
    main()
    #print (" -- good termination from main --")
