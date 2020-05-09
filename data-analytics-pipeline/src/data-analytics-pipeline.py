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
sys.path.insert(0, os.getcwd()+'/data-analytics-pipeline/src/h1')
sys.path.insert(0, os.getcwd()+'/data-analytics-pipeline/src/h2')
sys.path.insert(0, os.getcwd()+'/data-analytics-pipeline/src/h3')
sys.path.insert(0, os.getcwd()+'/data-analytics-pipeline/src/h4')
sys.path.insert(0, os.getcwd()+'/data-analytics-pipeline/src/h5')
sys.path.insert(0, os.getcwd()+'/data-analytics-pipeline/src/h6')
sys.path.insert(0, os.getcwd()+'/data-analytics-pipeline/src/h7')
sys.path.insert(0, os.getcwd()+'/data-analytics-pipeline/src/h8')
sys.path.insert(0, os.getcwd()+'/data-analytics-pipeline/src/h9')
sys.path.insert(0, os.getcwd()+'/data-analytics-pipeline/src/h10')
sys.path.insert(0, os.getcwd()+'/data-analytics-pipeline/src/h11')
sys.path.insert(0, os.getcwd()+'/data-analytics-pipeline/src/h12')
sys.path.insert(0, os.getcwd()+'/data-analytics-pipeline/src/h13')
sys.path.insert(0, os.getcwd()+'/data-analytics-pipeline/src/h14')
import h1Transformation
import h1
import h2Transformation
import h2
import h3Transformation
import h3
import h4Transformation
import h4
import h5Transformation
import h5
import h6Transformation
import h6
import h7Transformation
import h7
import h8Transformation
import h8
import h9Transformation
import h9
import h10Transformation
import h10
import h11Transformation
import h11
import h12Transformation
import h12
import h13Transformation
import h13
import h14Transformation
import h14
## ------------------------------
def returnJson(numlines,jreader,jname,rowname,rowid,returnrowid):
    """
    	ireader: csv file
        session_code: the session_code we want the data from.
    """
    data=[]
    for i in range(numlines):
    	#print(jreader[jname][i][rowname])
    	#print(jreader["CompletedSessionSummary"][i]["experiment_type"])
    	if jreader[jname][i][rowname]==rowid:
    		if jreader[jname][i][returnrowid] not in data:
    			data.append(jreader[jname][i][returnrowid])
    return data
    
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
    schemainputdata=os.getcwd()+'/jsonInputPipeline/schemas/data-analytics-pipeline.json'
    inputdata=os.getcwd()+'/jsonInputPipeline/input/data-analytics-pipeline.json'
    value=validateJson.validate(schemainputdata,inputdata)
    if value=='False':
    	sys.exit()
    
    experimentfile=os.getcwd()+json_data["experiment"]
    phasedescfile=os.getcwd()+json_data["phasedesc"]
    phasefile=os.getcwd()+json_data["phase"]
    actionfile=os.getcwd()+json_data["action"]
    playerfile=os.getcwd()+json_data["player"]
    functions=json_data["functions"]
    numlines= (len(functions))
    
    for i in range(numlines):
    	actionId=''
    	featureId=''
    	nd=''
    	windowSize=''
    	function=functions[i]["function"]
    	if function=='h1':
    		h1Transformation.main(experimentfile,phasedescfile,phasefile,actionfile,playerfile)
    		if os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h1/input/datasets/h1.json') and os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h1/input/schemas/h1.json'):
    			filename = os.getcwd()+'/data-analytics-pipeline/json-schema/h1/input/datasets/h1.json'	
    			schemaname = os.getcwd()+'/data-analytics-pipeline/json-schema/h1/input/schemas/h1.json'	
    			h1.main(filename,schemaname)
    		else:
    			print("No input of schema for h1")
    	if "actionId" in functions[i]:
    		actionId=functions[i]["actionId"]
    		if function=='h2':
    			h2Transformation.main(experimentfile,phasedescfile,phasefile,actionfile,actionId)
    			if os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h2/input/datasets/h2.json') and os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h2/input/schemas/h2.json'):
    				filename = os.getcwd()+'/data-analytics-pipeline/json-schema/h2/input/datasets/h2.json'	
    				schemaname = os.getcwd()+'/data-analytics-pipeline/json-schema/h2/input/schemas/h2.json'	
    				h2.main(filename,schemaname)
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
    		if function=='h4':
    			if "windowSize" in functions[i]:
    				windowSize=functions[i]["windowSize"]
    				h4Transformation.main(experimentfile,phasedescfile,phasefile,actionfile,actionId,windowSize)
    			if os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h4/input/datasets/h4.json') and os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h4/input/schemas/h4.json'):
    				filename = os.getcwd()+'/data-analytics-pipeline/json-schema/h4/input/datasets/h4.json'	
    				schemaname = os.getcwd()+'/data-analytics-pipeline/json-schema/h4/input/schemas/h4.json'	
    				h4.main(filename,schemaname)
    			else:
    				print("No input of schema for h4")
    		if function=='h5':
    			if "bin" in functions[i]:
    				bin=functions[i]["bin"]
    				h5Transformation.main(experimentfile,phasedescfile,phasefile,actionfile,actionId,bin)
    			if os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h5/input/datasets/h5.json') and os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h5/input/schemas/h5.json'):
    				filename = os.getcwd()+'/data-analytics-pipeline/json-schema/h5/input/datasets/h5.json'	
    				schemaname = os.getcwd()+'/data-analytics-pipeline/json-schema/h5/input/schemas/h5.json'	
    				h5.main(filename,schemaname)
    			else:
    				print("No input of schema for h5")
    		if function=='h6':
    			if "bin" in functions[i]:
    				bin=functions[i]["bin"]
    				h6Transformation.main(experimentfile,phasedescfile,phasefile,actionfile,actionId,bin)
    			if os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h6/input/datasets/h6.json') and os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h6/input/schemas/h6.json'):
    				filename = os.getcwd()+'/data-analytics-pipeline/json-schema/h6/input/datasets/h6.json'	
    				schemaname = os.getcwd()+'/data-analytics-pipeline/json-schema/h6/input/schemas/h6.json'	
    				h6.main(filename,schemaname)
    			else:
    				print("No input of schema for h6")
    	if "featureId" in functions[i]:
    		featureId=functions[i]["featureId"]
    		if function=='h7':
    			if "windowSize" in functions[i]:
    				windowsize=functions[i]["windowSize"]
    			if "nd" in functions[i]:
    				nd=functions[i]["nd"]
    			if "numseconds" in functions[i]:
    				numseconds=functions[i]["numseconds"]
    				h7Transformation.main(experimentfile,phasedescfile,phasefile,actionfile,featureId,windowsize,nd,numseconds)
    			if os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h7/input/datasets/h7.json') and os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h7/input/schemas/h7.json'):
    				filename = os.getcwd()+'/data-analytics-pipeline/json-schema/h7/input/datasets/h7.json'	
    				schemaname = os.getcwd()+'/data-analytics-pipeline/json-schema/h7/input/schemas/h7.json'	
    				h7.main(filename,schemaname)
    			else:
    				print("No input of schema for h7")
    	if function=='h8':
    		if "windowSize" in functions[i]:
    			windowsize=functions[i]["windowSize"]
    		if "nd" in functions[i]:
    			nd=functions[i]["nd"]
    		if "numseconds" in functions[i]:
    			numseconds=functions[i]["numseconds"]
    			h8Transformation.main(experimentfile,phasedescfile,phasefile,actionfile,playerfile,featureId,windowsize,nd,numseconds)
    		if os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h8/input/datasets/h8.json') and os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h8/input/schemas/h8.json'):
    			filename = os.getcwd()+'/data-analytics-pipeline/json-schema/h8/input/datasets/h8.json'	
    			schemaname = os.getcwd()+'/data-analytics-pipeline/json-schema/h8/input/schemas/h8.json'	
    			h8.main(filename,schemaname)
    		else:
    			print("No input of schema for h8")
    	if function=='h9':
    		if "cat1numletters" in functions[i]:
    			cat1numletters=functions[i]["cat1numletters"]
    		if "cat1time" in functions[i]:
    			cat1time=functions[i]["cat1time"]
    		if "cat2numwords" in functions[i]:
    			cat2numwords=functions[i]["cat2numwords"]
    		if "cat2time" in functions[i]:
    			cat2time=functions[i]["cat2time"]
    		if "nd" in functions[i]:
    			nd=functions[i]["nd"]
    		if "numseconds" in functions[i]:
    			numseconds=functions[i]["numseconds"]
    			h9Transformation.main(experimentfile,phasedescfile,phasefile,actionfile,featureId,cat1numletters,cat1time,cat2numwords,cat2time,nd,numseconds)
    		if os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h9/input/datasets/h9.json') and os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h9/input/schemas/h9.json'):
    			filename = os.getcwd()+'/data-analytics-pipeline/json-schema/h9/input/datasets/h9.json'	
    			schemaname = os.getcwd()+'/data-analytics-pipeline/json-schema/h9/input/schemas/h9.json'	
    			h9.main(filename,schemaname)
    		else:
    			print("No input of schema for h9")
    	if function=='h10':
    		if "windowSize" in functions[i]:
    			windowsize=functions[i]["windowSize"]
    		if "nd" in functions[i]:
    			nd=functions[i]["nd"]
    		if "numseconds" in functions[i]:
    			numseconds=functions[i]["numseconds"]
    			h10Transformation.main(experimentfile,phasedescfile,phasefile,actionfile,playerfile,featureId,windowsize,nd,numseconds)
    		if os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h10/input/datasets/h10.json') and os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h10/input/schemas/h10.json'):
    			filename = os.getcwd()+'/data-analytics-pipeline/json-schema/h10/input/datasets/h10.json'	
    			schemaname = os.getcwd()+'/data-analytics-pipeline/json-schema/h10/input/schemas/h10.json'	
    			h10.main(filename,schemaname)
    		else:
    			print("No input of schema for h10")
    	if function=='h11':
    		if "windowSize" in functions[i]:
    			windowsize=functions[i]["windowSize"]
    		if "nd" in functions[i]:
    			nd=functions[i]["nd"]
    		if "numseconds" in functions[i]:
    			numseconds=functions[i]["numseconds"]
    			h11Transformation.main(experimentfile,phasedescfile,phasefile,actionfile,playerfile,featureId,windowsize,nd,numseconds)
    		if os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h11/input/datasets/h11.json') and os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h11/input/schemas/h11.json'):
    			filename = os.getcwd()+'/data-analytics-pipeline/json-schema/h11/input/datasets/h11.json'	
    			schemaname = os.getcwd()+'/data-analytics-pipeline/json-schema/h11/input/schemas/h11.json'	
    			h11.main(filename,schemaname)
    		else:
    			print("No input of schema for h11")
    	if function=='h12':
    		if "windowSize" in functions[i]:
    			windowsize=functions[i]["windowSize"]
    		if "nd" in functions[i]:
    			nd=functions[i]["nd"]
    		if "numseconds" in functions[i]:
    			numseconds=functions[i]["numseconds"]
    			h12Transformation.main(experimentfile,phasedescfile,phasefile,actionfile,playerfile,featureId,windowsize,nd,numseconds)
    		if os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h12/input/datasets/h12.json') and os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h12/input/schemas/h12.json'):
    			filename = os.getcwd()+'/data-analytics-pipeline/json-schema/h12/input/datasets/h12.json'	
    			schemaname = os.getcwd()+'/data-analytics-pipeline/json-schema/h12/input/schemas/h12.json'	
    			h12.main(filename,schemaname)
    		else:
    			print("No input of schema for h12")
    	if function=='h13':
    		if "windowSize" in functions[i]:
    			windowsize=functions[i]["windowSize"]
    		if "nd" in functions[i]:
    			nd=functions[i]["nd"]
    		if "numseconds" in functions[i]:
    			numseconds=functions[i]["numseconds"]
    			h13Transformation.main(experimentfile,phasedescfile,phasefile,actionfile,playerfile,featureId,windowsize,nd,numseconds)
    		if os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h13/input/datasets/h13.json') and os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h13/input/schemas/h13.json'):
    			filename = os.getcwd()+'/data-analytics-pipeline/json-schema/h13/input/datasets/h13.json'	
    			schemaname = os.getcwd()+'/data-analytics-pipeline/json-schema/h13/input/schemas/h13.json'	
    			h13.main(filename,schemaname)
    		else:
    			print("No input of schema for h13")
    	if function=='h14':
    		if "windowSize" in functions[i]:
    			windowsize=functions[i]["windowSize"]
    		if "nd" in functions[i]:
    			nd=functions[i]["nd"]
    		if "numseconds" in functions[i]:
    			numseconds=functions[i]["numseconds"]
    			h14Transformation.main(experimentfile,phasedescfile,phasefile,actionfile,playerfile,featureId,windowsize,nd,numseconds)
    		if os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h14/input/datasets/h14.json') and os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h14/input/schemas/h14.json'):
    			filename = os.getcwd()+'/data-analytics-pipeline/json-schema/h14/input/datasets/h14.json'	
    			schemaname = os.getcwd()+'/data-analytics-pipeline/json-schema/h14/input/schemas/h14.json'	
    			h14.main(filename,schemaname)
    		else:
    			print("No input of schema for h14")
    	
    	#if windowSize!='KeyError':
    	#	print(windowSize)
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
