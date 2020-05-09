import sys
import os
import csv
import jsonschema
import json
from datetime import time, datetime, timedelta
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib as mpl
import numpy as np
import validateJson


## ------------------------------
def interaction(numlines,jreader,session,begin,n,d,numseconds):
	words_reader=[]
	for i in range(numlines):
		words_reader.append([jreader[i]["timestamp"],int(jreader[i]["second"]),int(jreader[i]["playeridint"]),jreader[i]["payload"],jreader[i]["playerid"],jreader[i]["initialparameter"],jreader[i]["actionid"]])
	words_reader = sorted(words_reader, key=lambda a_entry: a_entry[2],reverse=True)
	wordlabel=[]
	xlabel=[]
	xs=[]
	ys=[]
	sec=0
	j=0
	counter=0
	begin=float(begin)
	begin1=datetime.utcfromtimestamp(float(begin))
	strbegin=str(begin1.time())
	end=datetime.utcfromtimestamp(float(begin)+numseconds)
	strbegin=str(begin1.time())
	strend=str(end.time())
    	
	fig, ax = plt.subplots(figsize=(20, 10))
	start, end = ax.get_xlim()
	ax.xaxis.set_ticks(np.arange(start, end, 3))
	for index,row in enumerate(words_reader):
		id=int(row[2])
		if counter<int(numseconds):
			xs.append(int(row[1]))
		if sec==60 or sec==0:
			if sec==60:
				sec=0
			if counter<int(numseconds):
				xlabel.append(row[0].split(' ')[-1])
			sec=sec+1	
		else:
			if counter<int(numseconds):
				xlabel.append('')
			sec=sec+1
		if row[3]=='':
			ys.append(np.nan)
			wordlabel.append(np.nan)
		if len(row[3])>=1:
			ys.append(int(row[2]))
			if row[6]!='':
				wordlabel.append(row[6]+' '+row[3])
			else:
				wordlabel.append(row[3])
		if j==int(numseconds)-1:
			j=0
			ax.scatter(xs,ys,s=2, label=str(row[2])+'-'+str(row[5])+'-'+str(row[4]))
			for i, txt in enumerate(wordlabel):
				if isinstance(txt, str)== True:
					if ' ' in txt: 
						writetype,writeword=txt.split(" ")
						if writetype=='1':
							ax.annotate(writeword, (xs[i],ys[i]),fontsize=18,color='red', rotation='vertical')
						if writetype=='2':
							ax.annotate(writeword, (xs[i],ys[i]),fontsize=18,color='green', rotation='vertical')
						if writetype=='3':
							ax.annotate(writeword, (xs[i],ys[i]),fontsize=18,color='orange', rotation='vertical')
						if writetype=='4':
							ax.annotate(writeword, (xs[i],ys[i]),fontsize=18,color='blue', rotation='vertical')
						if writetype=='5':
							ax.annotate(writeword, (xs[i],ys[i]),fontsize=18,color='black', rotation='vertical')
					else:
						ax.annotate(txt, (xs[i],ys[i]),fontsize=18, rotation='vertical')
				else:
					ax.annotate(txt, (xs[i],ys[i]),fontsize=18, rotation='vertical')
			ys=[]
			wordlabel=[]
		else:
			j=j+1
		counter=counter+1
	labelx='Analysis by second from game time: '+strbegin+'-'+strend
	legend=ax.legend(loc='upper left',prop={'size':10}, bbox_to_anchor=(1, 0.5))
	plt.gcf().subplots_adjust(bottom=0.35)
	plt.title(str(begin1.date())+' Session:'+session,fontsize=35)
	plt.ylabel(str('Player id'), fontsize=35)
	plt.xlabel(labelx, fontsize=35)
	plt.xticks(xs, xlabel,fontsize=35)#rotation='vertical'
	plt.yticks(fontsize=35)
	plt.savefig(os.getcwd()+'/data-analytics-pipeline/test/results/h1/visualizationOutput/'+session+'.png')
	plt.cla()
	plt.close(fig)


### -----------------------------
### Start.
def main(filename,schemaname):
		
    if not os.path.exists(os.getcwd()+'/data-analytics-pipeline/test/results/h1/visualizationOutput/'):
    	os.makedirs(os.getcwd()+'/data-analytics-pipeline/test/results/h1/visualizationOutput/')
    
    value=validateJson.validate(schemaname,filename)
    if value=='False':
    	sys.exit()
    	
    json_file = open(filename, 'r')
    json_data = json.load(json_file)
    numlines= (len(json_data))
    players=[]
    for i in range(numlines):
    	session=json_data[i]["phaseid"]
    	begin=json_data[i]["begin"]
    	n=json_data[i]["n"]
    	d=json_data[i]["d"]
    	numseconds=json_data[i]["duration"]
    	players=json_data[i]["players"]
    	interaction(len(players),players,session,begin,n,d,numseconds)
    print (" -- h1 --")
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
    print (" -- oi --")
    main(filename,schemaname)
    