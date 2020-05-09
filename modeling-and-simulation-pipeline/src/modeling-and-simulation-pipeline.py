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

import h1Transformation
import h1


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
    		groupslist=[]
    		if "path" in functions[i] and "filename" in functions[i]:
    			inputpath=os.getcwd()+functions[i]["path"]
    			filename=functions[i]["filename"]
    		else:
    			if os.path.exists(os.getcwd()+'/property-inference-pipeline/json-schema/inputTransformation/datasets/h1.json') and os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h7/input/schemas/h7.json'):
    				filename = os.getcwd()+'/property-inference-pipeline/json-schema/inputTransformation/datasets/h1.json'	
    				schemaname = os.getcwd()+'/property-inference-pipeline/json-schema/inputTransformation/schemas/h1.json'	
    				h1Transformation.main(filename,schemaname)
    			inputpath=os.getcwd()+'/property-inference-pipeline/json-schema/h1/input/datasets/'
    			filename="tsData.csv"
    		groups=functions[i]["groups"]
    		numlinesgroups= (len(groups))
    		for ii in range(numlinesgroups):
    			groupslist.append([groups[ii]["n"],groups[ii]["d"]])
    		
    		h1.main(inputpath,filename,groupslist)
    		#else:
    		#	print("No input of schema for h1")
    	if "actionId" in functions[i]:
    		actionId=functions[i]["actionId"]
    		if function=='h2':
    			#h2Transformation.main(experimentfile,phasedescfile,phasefile,actionfile,actionId)
    			if os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h2/input/datasets/h2.json') and os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h2/input/schemas/h2.json'):
    				filename = os.getcwd()+'/data-analytics-pipeline/json-schema/h2/input/datasets/h2.json'	
    				schemaname = os.getcwd()+'/data-analytics-pipeline/json-schema/h2/input/schemas/h2.json'	
    				#h2.main(filename,schemaname)
    			else:
    				print("No input of schema for h2")
    		if function=='h3':
    			if "windowSize" in functions[i]:
    				windowSize=functions[i]["windowSize"]
    				h3Transformation.main(experimentfile,phasedescfile,phasefile,actionfile,actionId,windowSize)
    			if os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h3/input/datasets/h3.json') and os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h3/input/schemas/h3.json'):
    				filename = os.getcwd()+'/data-analytics-pipeline/json-schema/h3/input/datasets/h3.json'	
    				schemaname = os.getcwd()+'/data-analytics-pipeline/json-schema/h3/input/schemas/h3.json'	
    				h3.main(filename,schemaname)
    			else:
    				print("No input of schema for h3")

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
