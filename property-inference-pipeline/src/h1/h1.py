import sys
import os
import csv
import subprocess
import json

## ------------------------------
def interaction(numlines,jreader,session,begin,n,d,numseconds):
	words_reader=[]



### -----------------------------
### Start.
def main(path,filename,groupslist):
		
    if not os.path.exists(os.getcwd()+'/property-inference-pipeline/test/results/h1/static_markov/'):
    	os.makedirs(os.getcwd()+'/property-inference-pipeline/test/results/h1/static_markov/')
    if not os.path.exists(os.getcwd()+'/property-inference-pipeline/test/results/h1/dynamic_markov/'):
    	os.makedirs(os.getcwd()+'/property-inference-pipeline/test/results/h1/dynamic_markov/')
    
    rfilename=path+"/all/"+filename
    #print(rfilename)
    rpath=os.getcwd()+'/property-inference-pipeline/src/h1/dynamic_markov_ts.R'
    #subprocess.call (['Rscript',rpath,rfilename])
    staticpath=os.getcwd()+'/property-inference-pipeline/test/results/h1/static_markov/transition_probability_static.csv'
    csvfile = open(staticpath, 'r')
    
    interactionjson=open(os.getcwd()+'/property-inference-pipeline/test/results/h1/static_markov/h1.json', 'w')
    alljsondata=[]
    
    for index,row in enumerate(csvfile):
    	rowlist=row.split(",")
    	allprob=[]
    	for index2,row2 in enumerate(rowlist):
    		if index2==0:
    			rowname=row2
    		if index>0 and index2>0:
    			allprob.append(row2.rstrip("\n"))
    	if index >0:
    		alljsondata.append([rowname,allprob])
    #print(alljsondata)
    
    interactionjsondata=[{"probabilities":[{"initial":str(row[0]),"values":[{"final":str(row2)}for row2 in row[1]]}]} for row in alljsondata]
    json.dump(interactionjsondata,interactionjson,indent=2)
    #for row in groupslist:
    #	print(row[0])
    #	print(row[1])
    #	print(path+"/"+"n"+row[0]+"d"+row[1]+"/"+filename)

    #json_file = open(filename, 'r')
    #json_data = json.load(json_file)
    #numlines= (len(json_data))
    #players=[]
    #for i in range(numlines):
    #	session=json_data[i]["phaseid"]
    #	begin=json_data[i]["begin"]
    #	n=json_data[i]["n"]
    #	d=json_data[i]["d"]
    #	numseconds=json_data[i]["duration"]
    #	players=json_data[i]["players"]
    #	interaction(len(players),players,session,begin,n,d,numseconds)
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
    	
    path=sys.argv[1]
    filename=sys.argv[2]
    groups=sys.argv[3]
    print (" -- oi --")
    main(path,filename,groups)
    