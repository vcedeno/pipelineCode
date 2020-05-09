import sys
import os
import csv
import jsonschema
import json
from datetime import time, datetime, timedelta
from itertools import cycle
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib as mpl
import numpy as np
import validateJson

## ------------------------------
def requestRepliesPlot(actionname,numlines,jreader,sessionid,stime,n,d,numseconds):
	players=[]
	actions=[]
	allrequests=[]
	allrequests2=[]
	actionrequest,actionreply=actionname.split('-')
	for i in range(numlines):
		players.append(jreader[i]["playerid"])
		actions=jreader[i]["actions"]
		for index,row in enumerate(actions):
			if actions[index]["action_id"]==actionrequest+'received':
				allrequests.append([jreader[i]["playerid"],actions[index]["timestampsent"],actions[index]["timestampreceive"]])
			if actions[index]["action_id"]==actionrequest:
				allrequests2.append([jreader[i]["playerid"],actions[index]["timestampsent"],actions[index]["timestampreceive"]])
	#print(players)
	#print(allrequests)
	#print(allrequests2)
	#words_reader = sorted(words_reader, key=lambda a_entry: a_entry[2],reverse=True)
	
	labelx='Replies Requests Analysis'
	x=[]
	y=[]
	xall=[]
	yall=[]
	names=[]
	duration=numseconds
	allsessions='Sessions:'
	playerlabel=[]
	cycol=cycle('bgrcmky')
	colorMe=next(cycol)
	countall=0
	fig, ax = plt.subplots(figsize=(35, 15))
	max=0
	#print("###player###")
	for row in players:
		#print(row)
		count=0
		requests=[]
		requests2=[]
		for all in allrequests:
			if all[0]==row:
				requests.append([all[1],all[2]])
		for all in allrequests2:
			if all[0]==row:
				requests2.append([all[1],all[2]])
		#print(requests)
		#print(requests2)
		#for index,row1 in enumerate(row[1]):
		#	if row[1][index]["action_id"]==actionrequest+'received':
		#		requests.append([row[1][index]["timestampsent"],row[1][index]["timestampreceive"]])
		#for index,row1 in enumerate(row[1]):
		#	if row[1][index]["action_id"]==actionrequest:
		#		requests2.append([row[1][index]["timestampsent"],row[1][index]["timestampreceive"]])
		#print(requests)
		#print("requests2")
		#print(requests2)
		y=[]
		topdata=[]
		bottomdata=[]
		if requests!=[]:
			names.append(row+' - Passive')
			colorMe=next(cycol)
			#print(requests)
			for index,req in enumerate(requests):
				count=count+1
				if float(req[0])>max:
					max=float(req[0])
				countall=countall+1
				if index>0:
					names.append('')
				if req[1]=='':
					topdata.append(0)
					ax.plot([float(req[0])-stime, duration], [countall, countall],color=colorMe,linestyle='dashed')
				else:
					topdata.append(float(req[1])-stime)
					if float(req[1])>max:
						max=float(req[1])
				bottomdata.append(float(req[0])-stime)
				y.append(countall)
				yall.append(countall)
			ax.barh(y,topdata,color=colorMe,align='center',edgecolor="none")   			
			ax.barh(y,bottomdata,color='w',align='center',edgecolor="none") 
    	##
			for x in range(count,6):
				if x>0:
					names.append('')
				countall=countall+1
				yall.append(countall)
				topdata.append(0)
				ax.plot([0, duration], [countall, countall],color='w',linestyle='dashed')
			ax.plot([0.,duration],[countall+0.5,countall+0.5],"k-")
    	
		count=0
    	
		y=[]
		topdata=[]
		bottomdata=[]
    	
		if requests2!=[]:
			names.append(row+' - Active')
			for index,req in enumerate(requests2):
				count=count+1
				if float(req[0])>max:
					max=float(req[0])
				countall=countall+1
				if index>0:
					names.append('')
				if req[1]=='':
					topdata.append(0)
					ax.plot([float(req[0])-stime, duration], [countall, countall],color=colorMe,linestyle='dashed')
				else:
					topdata.append(float(req[1])-stime)
					if float(req[1])>max:
						max=float(req[1])
				bottomdata.append(float(req[0])-stime)
				y.append(countall)
				yall.append(countall)
			ax.barh(y,topdata,color=colorMe,align='center',edgecolor="none")   			
			ax.barh(y,bottomdata,color='w',align='center',edgecolor="none") 
    	##
			for x in range(count,6):
				if x>0:
					names.append('')
				countall=countall+1
				yall.append(countall)
				topdata.append(0)
				ax.plot([0, duration], [countall, countall],color='w',linestyle='dashed')
			ax.plot([0.,duration],[countall+0.5,countall+0.5],"k-")
		#print("countall")
		#print(countall)
	#print("max")
	#print(max)
    #print(y)
    #print(bottomdata)
    #print(topdata)

    #ax.set_ylim(-1,len(yall))
	ax.set_yticks(yall)
	ax.set_yticklabels(names,fontsize=30)
	plt.xticks(fontsize=30)
	ax.set_xlabel('Game time in seconds',fontsize=45)
    					#print("player")
    					#print(row1)
    					#print(requests)
	ax.plot([0, 0], [0, 0], "k-",label='player')
	ax.plot([0, 0], [0, 0],color='black',linestyle='dashed',label='No reply')
	ax.plot([0, 0], [0, 0],color='black',linestyle='solid',label='Reply sent',linewidth=7.0)
	legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
	axes = plt.gca()
    ##axes.margins(0.05)
	axes.set_ylim([0,len(yall)])
	axes.set_xlim([0,duration])
    #plt.yticks(fontsize=8)
    ##plt.show()
	plt.title('Session:'+sessionid+'\nPassive: replies sent/Requests received - Active: replies received/Requests sent',fontsize=40)
	plt.savefig(os.getcwd()+'/data-analytics-pipeline/test/results/h2/visualizationOutput/'+actionname+'/n'+str(n)+'d'+str(d)+'id'+sessionid+'.png')
	plt.cla()
	plt.close(fig)

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
    		action=actionrequest[index]["actionrequest"]
    		if not os.path.exists(os.getcwd()+'/data-analytics-pipeline/test/results/h2/visualizationOutput/'+action):
    			os.makedirs(os.getcwd()+'/data-analytics-pipeline/test/results/h2/visualizationOutput/'+action)
    		phases=actionrequest[index]["phases"]
    		for index2,row in enumerate(phases):
    			session=phases[index2]["phaseid"]
    			#print(session)
    			begin=phases[index2]["begin"]
    			n=phases[index2]["n"]
    			d=phases[index2]["d"]
    			numseconds=phases[index]["duration"]
    			players=phases[index2]["players"]
    			requestRepliesPlot(action,len(players),players,session,begin,n,d,numseconds)
    print (" -- h2 --")
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
    