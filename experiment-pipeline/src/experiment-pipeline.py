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
sys.path.insert(0, os.getcwd()+'/experiment-pipeline/src/h1')
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
    schemainputdata=os.getcwd()+'/jsonInputPipeline/schemas/experiment-pipeline.json'
    inputdata=os.getcwd()+'/jsonInputPipeline/input/experiment-pipeline.json'
    value=validateJson.validate(schemainputdata,inputdata)
    if value=='False':
    	sys.exit()
    functions=json_data["functions"]
    numlines= (len(functions))
    for i in range(numlines):
    	function=functions[i]["function"]
    	if function=='h1':
    		if "path" in functions[i]:
    			inputpath=os.getcwd()+functions[i]["path"]
    			anagrams=functions[i]["anagrams"]
    			CompletedSessionSummary=functions[i]["CompletedSessionSummary"]
    			InstructionsAnagrams=functions[i]["InstructionsAnagrams"]
    			LetterTransactions=functions[i]["LetterTransactions"]
    			Neighbors=functions[i]["Neighbors"]
    			PublicGoods=functions[i]["PublicGoods"]
    			TeamWords=functions[i]["TeamWords"]
    			TimeSpent=functions[i]["TimeSpent"]
    			UserLetters=functions[i]["UserLetters"]
    		
    		h1Transformation.main(inputpath,anagrams,CompletedSessionSummary,InstructionsAnagrams,LetterTransactions,Neighbors,PublicGoods,TeamWords,TimeSpent,UserLetters)
    		#if os.path.exists(os.getcwd()+'/experiment-pipeline/json-schema/h1/input/datasets/h6.json') and os.path.exists(os.getcwd()+'/data-analytics-pipeline/json-schema/h6/input/schemas/h6.json'):
    		h1.main(os.getcwd()+'/experiment-pipeline/json-schema/h1/input/datasets',anagrams,CompletedSessionSummary,InstructionsAnagrams,LetterTransactions,Neighbors,PublicGoods,TeamWords,TimeSpent,UserLetters)	

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
