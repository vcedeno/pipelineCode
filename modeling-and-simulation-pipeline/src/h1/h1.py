import sys
import os
import csv
import jsonschema
import json
from datetime import time, datetime, timedelta
import itertools
from itertools import cycle
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib as mpl
from matplotlib.pyplot import cm 
import numpy as np
import validateJson

## ------------------------------
def filescsv(n,d,numseconds,numlines,phases,csvfileall):
	allphases=[]
	nd="n"+str(n)+"d"+str(d)
	if not os.path.exists(os.getcwd()+'/property-inference-pipeline/json-schema/h1/input/datasets/'+nd):
		os.makedirs(os.getcwd()+'/property-inference-pipeline/json-schema/h1/input/datasets/'+nd)
	csvfile = open(os.getcwd()+'/property-inference-pipeline/json-schema/h1/input/datasets/'+nd+'/tsData.csv', 'w')
	csvfile.write('session,player,type,')
	for x in range(0,numseconds):
		if x==numseconds-1:
			csvfile.write(str(x)+'\n')
		else:
			csvfile.write(str(x)+',')
    	
	for i in range(numlines):
		phase=phases[i]["phaseid"]
		players=phases[i]["players"]
		numplayers=len(players)
		for ii in range(numplayers):
			playerid=players[ii]["playerid"]
			features=players[ii]["features"]
			numfeatures=len(features)
			for iii in range(numfeatures):
				csvfile.write(str(phase)+',')
				csvfile.write(str(playerid)+',')
				csvfileall.write(str(phase)+',')
				csvfileall.write(str(playerid)+',')
				featureid=features[iii]["featureid"]
				csvfile.write(str(featureid)+',')
				csvfileall.write(str(featureid)+',')
				timeline=features[iii]["timeline"]
				#print(timeline)
				numtimeline=len(timeline)
				for iiii in range(numtimeline):
					value=timeline[iiii]["value"]
					if iiii==(numseconds-1):
						csvfile.write(str(value)+'\n')
						csvfileall.write(str(value)+'\n')
					else:
						csvfile.write(str(value)+',')
						csvfileall.write(str(value)+',')

### -----------------------------
### Start.
def main(filename,schemaname):
    
    value=validateJson.validate(schemaname,filename)
    if value=='False':
    	sys.exit()
    
    json_file = open(filename, 'r')
    json_data = json.load(json_file)
    numlines= (len(json_data))
    #print(numlines)
    if not os.path.exists(os.getcwd()+'/property-inference-pipeline/json-schema/h1/input/datasets/all'):
    	os.makedirs(os.getcwd()+'/property-inference-pipeline/json-schema/h1/input/datasets/all')
    csvfileall = open(os.getcwd()+'/property-inference-pipeline/json-schema/h1/input/datasets/all/tsData.csv', 'w')
    csvfileall.write('session,player,type,')

    for i in range(numlines):
    	actionrequest=json_data[i]["features"]
    	for index,actions in enumerate(actionrequest):
    		n=actionrequest[index]["n"]
    		d=actionrequest[index]["d"]
    		windowsize=actionrequest[index]["windowsize"]
    		numseconds=actionrequest[index]["numseconds"]
    		if i==0 and index==0:
    			for x in range(0,numseconds):
    				if x==numseconds-1:
    					csvfileall.write(str(x)+'\n')
    				else:
    					csvfileall.write(str(x)+',')

    		#if not os.path.exists(os.getcwd()+'/data-analytics-pipeline/test/results/h7/output/'+action):
    		#	os.makedirs(os.getcwd()+'/data-analytics-pipeline/test/results/h7/output/'+action)
    		phases=actionrequest[index]["phases"]
    		filescsv(n,d,numseconds,len(phases),phases,csvfileall)
    print (" -- h1 Transformation --")
    print (" -- good termination --")

    			
    
## --------------------------
## Execution starts.
if __name__ == '__main__':
		
    if (len(sys.argv) != 3):
    	print ("  Error.  Incorrect usage.")
    	print ("  usage: exec infile outfile.")
    	print ("  Halt.")
    	quit()
    	
    filename=sys.argv[1]
    schemaname=sys.argv[2]
    main(filename,schemaname)
    