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
def cdPlot(action,numlines,phases):
	allphases=[]
	averages=[]
	for i in range(numlines):
		x=[]
		y=[]
		averages=phases[i]["average"]
		session=phases[i]["phaseid"]
		begin=phases[i]["begin"]
		n=phases[i]["n"]
		d=phases[i]["d"]
		windowsize=phases[i]["windowsize"]
		if not os.path.exists(os.getcwd()+'/data-analytics-pipeline/test/results/h4/output/'+action+'/'+str(windowsize)+'S'):
			os.makedirs(os.getcwd()+'/data-analytics-pipeline/test/results/h4/output/'+action+'/'+str(windowsize)+'S')
		for index,row in enumerate(averages):
			x.append(averages[index]["second"])
			y.append(averages[index]["value"])
		allphases.append([session,x,y])
		
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
	
	color=iter(cm.rainbow(np.linspace(0,1,len(allphases)+1)))
	marker=itertools.cycle(('+','.','1','2','3','4','_','x','|','1','2','3','4','8','s','>','<','^','v','o','X','P','d','D','H','h','*','p'))
	m=next(marker)
	c=next(color)
	for row in allphases:
		#marker=marker.next()
		#print(row[0])
		#print(row[1])
		#print(row[2])
		ax.plot(row[1], row[2], marker=m, label=row[0],color=c)
		c=next(color)
	legend=ax.legend(loc='upper left',prop={'size':15}, bbox_to_anchor=(1, 1), borderaxespad=0)
	plt.gcf().subplots_adjust(bottom=0.35)
	plt.ylabel(str('Avg. of '+action+'s'),fontsize=40)
	plt.xlabel(str(labelx),fontsize=40)
	plt.xticks(fontsize=40)
	plt.title('CDF for the average number of '+action+'s formed in all sessions',fontsize=40)
	plt.savefig(os.getcwd()+'/data-analytics-pipeline/test/results/h4/output/'+action+'/'+str(windowsize)+'S/'+'averagesW'+str(windowsize)+'S.png')
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
    		if not os.path.exists(os.getcwd()+'/data-analytics-pipeline/test/results/h4/output/'+action):
    			os.makedirs(os.getcwd()+'/data-analytics-pipeline/test/results/h4/output/'+action)
    		phases=actionrequest[index]["phases"]
    		cdPlot(action,len(phases),phases)
    print (" -- h4 --")
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
    