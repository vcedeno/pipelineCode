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
def cdPlot(action,numlines,jreader,sessionid,stime,n,d,windowsize):
	players=[]
	actions=[]
	
	for i in range(numlines):
		x=[]
		y=[]
		actions=jreader[i]["actions"]
		for index,row in enumerate(actions):
			x.append(actions[index]["second"])
			y.append(actions[index]["value"])
			duration=actions[index]["second"]
		players.append([jreader[i]["playerid"],x,y])
	#print(players)
	#print(allrequests)
	#print(allrequests2)
	#words_reader = sorted(words_reader, key=lambda a_entry: a_entry[2],reverse=True)
	if windowsize>1:
		labelx='Analysis every '+ str(windowsize)+ ' seconds'
	else:
		labelx='Analysis every second'
	names=[]
	#duration=x[len(x)]
	allsessions='Sessions:'
	playerlabel=[]
	#cycol=cycle('bgrcmky')
	countall=0
	#print("###player###")
	#word cdf plot
	fig, ax = plt.subplots(figsize=(20, 10))
	#color=cycle('bgrcmk')
	
	color=iter(cm.rainbow(np.linspace(0,1,len(players)+1)))
	marker=itertools.cycle(('+','.','1','2','3','4','_','x','|','1','2','3','4','8','s','>','<','^','v','o','X','P','d','D','H','h','*','p'))
	m=next(marker)
	c=next(color)
	for row in players:
		#marker=marker.next()
		#print(row[0])
		#print(row[1])
		#print(row[2])
		ax.plot(row[1], row[2], marker=m, label=row[0],color=c)
		c=next(color)
	legend=ax.legend(loc='upper left',prop={'size':15}, bbox_to_anchor=(1, 1), borderaxespad=0)
	plt.gcf().subplots_adjust(bottom=0.35)
	plt.ylabel(str('Count of '+action+'s'),fontsize=40)
	plt.xlabel(str(labelx),fontsize=40)
	plt.xticks(fontsize=40)
	plt.title('CDF of '+action+'s formed in session '+sessionid,fontsize=40)
	plt.savefig(os.getcwd()+'/data-analytics-pipeline/test/results/h3/output/'+action+'/'+str(windowsize)+'S/'+sessionid+'W'+str(windowsize)+'S.png')
	plt.cla()
	plt.close(fig)
    #plt.yticks(fontsize=8)


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

    for i in range(numlines):
    	actionrequest=json_data[i]["actions"]
    	for index,actions in enumerate(actionrequest):
    		action=actionrequest[index]["action"]
    		if not os.path.exists(os.getcwd()+'/data-analytics-pipeline/test/results/h3/output/'+action):
    			os.makedirs(os.getcwd()+'/data-analytics-pipeline/test/results/h3/output/'+action)
    		phases=actionrequest[index]["phases"]
    		for index2,row in enumerate(phases):
    			session=phases[index2]["phaseid"]
    			#print(session)
    			begin=phases[index2]["begin"]
    			n=phases[index2]["n"]
    			d=phases[index2]["d"]
    			windowsize=phases[index]["windowsize"]
    			if not os.path.exists(os.getcwd()+'/data-analytics-pipeline/test/results/h3/output/'+action+'/'+str(windowsize)+'S'):
    				os.makedirs(os.getcwd()+'/data-analytics-pipeline/test/results/h3/output/'+action+'/'+str(windowsize)+'S')
    			players=phases[index2]["players"]
    			cdPlot(action,len(players),players,session,begin,n,d,windowsize)
    print (" -- h3 --")
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
    