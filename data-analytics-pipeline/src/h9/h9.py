##Time series for categories 1, 2, 3, 4
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
import subprocess

## ------------------------------
def filescsv(n,d,numseconds,numlines,phases,csvfileall,cat1numletters,cat1time,cat2numwords,cat2time):
	nd="n"+str(n)+"d"+str(d)
	#if not os.path.exists(os.getcwd()+'/data-analytics-pipeline/test/results/h9/output/'+nd):
	#	os.makedirs(os.getcwd()+'/data-analytics-pipeline/test/results/h9/output/'+nd)

	#csvfile = open(os.getcwd()+'/data-analytics-pipeline/test/results/h9/output/'+nd+'/tsData.csv', 'w')
	#csvfile.write('session,player,type,time,requestsSent,repliesReceived,requestsReceived,repliesSent,words\n')
	
	#csvfileheat = open(os.getcwd()+'/data-analytics-pipeline/test/results/h8/output/'+nd+'HeatMap.csv', 'w')
	#csvfileheat.write('day\thour\tvalue\n')
	
	countplayer=0
	for i in range(numlines):
		phase=phases[i]["phaseid"]
		players=phases[i]["players"]
		numplayers=len(players)
		for ii in range(numplayers):
			countplayer=countplayer+1
			playerid=players[ii]["playerid"]
			category=players[ii]["category"]
			requestssent=players[ii]["requestsent"]
			repliesreceived=players[ii]["repliesreceived"]
			csvfileall.write(str(phase)+','+str(playerid)+','+str(nd)+','+str(category)+','+str(requestssent)+','+str(repliesreceived)+'\n')

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
    if not os.path.exists(os.getcwd()+'/data-analytics-pipeline/test/results/h9/output/all'):
    	os.makedirs(os.getcwd()+'/data-analytics-pipeline/test/results/h9/output/all')
    csvfileall = open(os.getcwd()+'/data-analytics-pipeline/test/results/h9/output/all/tsData.csv', 'w')
    csvfileall.write('session,player,type,category,requestsSent,repliesReceived\n')
    
    	
    for i in range(numlines):
    	actionrequest=json_data[i]["features"]
    	for index,actions in enumerate(actionrequest):
    		n=actionrequest[index]["n"]
    		d=actionrequest[index]["d"]
    		cat1numletters=actionrequest[index]["cat1numletters"]
    		cat1time=actionrequest[index]["cat1time"]
    		cat2numwords=actionrequest[index]["cat2numwords"]
    		cat2time=actionrequest[index]["cat2time"]
    		numseconds=actionrequest[index]["numseconds"]
    		#if not os.path.exists(os.getcwd()+'/data-analytics-pipeline/test/results/h7/output/'+action):
    		#	os.makedirs(os.getcwd()+'/data-analytics-pipeline/test/results/h7/output/'+action)
    		phases=actionrequest[index]["phases"]

    		filescsv(n,d,numseconds,len(phases),phases,csvfileall,cat1numletters,cat1time,cat2numwords,cat2time)
    csvfileall.close()	
    rpath=os.getcwd()+'/data-analytics-pipeline/src/h9'+'/plot.R'
    subprocess.call (['Rscript',rpath,os.getcwd()+'/data-analytics-pipeline/test/results/h9/output/all/tsData.csv'])
    
    print (" -- h9 --")
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
    