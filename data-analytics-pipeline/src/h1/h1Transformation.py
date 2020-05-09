import sys
import os
import csv
import jsonschema
import json
from datetime import time, datetime, timedelta

##player neighbors
## ------------------------------
def getLetters(numlines,jreader,rowname1,rowname2,rowid1,rowid2):
    """
    	jreader: json file
    """
    letters=[]
    letterslist=[]
    for i in range(numlines):
    	if jreader[i][rowname1]== rowid1 and jreader[i][rowname2]== rowid2:
    		letters=jreader[i]["beginparameters"]
    		
    		for index,row in enumerate(letters):
    			if letters[index]["parameter"]=="letter1":
    				letterslist.append(letters[index]["value"])
    			if letters[index]["parameter"]=="letter2":
    				letterslist.append(letters[index]["value"])
    			if letters[index]["parameter"]=="letter3":
    				letterslist.append(letters[index]["value"])
    return ",".join(str(x) for x in letterslist)

## ------------------------------
def getPhase(numlines,jreader,rowname1,rowid1):
    """
    	jreader: json file
    """
    begin=0
    numseconds=0
    n=0
    d=0
    experimentid=0
    for i in range(numlines):
    	if jreader[i][rowname1]== rowid1 :
    		begin=jreader[i]["begin"]
    		numseconds=jreader[i]["duration"]
    		n=jreader[i]["n"]
    		d=jreader[i]["d"]
    		experimentid=jreader[i]["experimentid"]

    return begin,numseconds,n,d,experimentid

## ------------------------------
def getPlayers(numlines,jreader,rowname1,rowid1):
    """
    	jreader: json file
    """
    players=[]
    playerslist=[]
    for i in range(numlines):
    	if jreader[i][rowname1]== rowid1 :
    		players=jreader[i]["activeplayers"]
    for index,row in enumerate(players):
    	playerslist.append(players[index]["player"])

    return playerslist
      
##player interaction json file for visualization
## ------------------------------
def returnJson(numlines,jreader,rowname,phasesids,experimentfile,playerfile,phasefile):
    """
    	jreader: json file
    """
    
    data=[]
    alldatajson=[]
    jsonfilename = phasefile
    json_phase = open(jsonfilename, 'r')
    phase_data = json.load(json_phase)
    numlinesphase= len(phase_data)
    
    jsonfilename = playerfile	
    json_player = open(jsonfilename, 'r')
    player_data = json.load(json_player)
    numlinesplayer= len(player_data)
    interactionjson=open(os.getcwd()+'/data-analytics-pipeline/json-schema/h1/input/datasets/h1.json', 'w')
    
    jsonfilename = experimentfile
    json_experiment = open(jsonfilename, 'r')
    experiment_data = json.load(json_experiment)
    numlinesexperiment= len(experiment_data)
    
    	
    for i in range(numlines):
    	if jreader[i][rowname]in phasesids:
    		actions=jreader[i]["actionlist"]
    		for index,row in enumerate(actions):
    			data.append([actions[index]["player1"],actions[index]["player2"],actions[index]["actionid"],actions[index]["playerActionSeqid"],actions[index]["timestamp"],actions[index]["payload"]])
    for phase in phasesids:
    	#print(phase)
    	json_phase.seek(0)
    	begin,numseconds,n,d,experimentid=getPhase(numlinesphase,phase_data,"phaseid",phase)
    	numseconds=int(numseconds)
    	#print("poi")
    	#print(str(numseconds))
    	countplayer=0
    	sreq=0
    	srep=0
    	json_experiment.seek(0)
    	players=getPlayers(numlinesexperiment,experiment_data,"experimentid",experimentid)
    	#print(players)
    	playersactions=[]
    	for player in players:
    		json_player.seek(0)
    		letterstring=getLetters(numlinesplayer,player_data,"phaseid","playerid",phase,player)
    		#print(player)
    		#print(letterstring)
    		alleventArray=[]
    		#print(data)
    		for row in data:
    			if row[0]==player and row[2]=="requestsent":
    				alleventArray.append([row[5],'requestsent',row[4]])
    			if row[1]==player and row[2]=="replysent":
    				alleventArray.append([row[5],'replyreceived',row[4]])
    			if row[1]==player and row[2]=="requestsent":
    				alleventArray.append([row[5],'requestreceived',row[4]])
    			if row[0]==player and row[2]=="replysent":
    				alleventArray.append([row[5],'replysent',row[4]])
    			if row[0]==player and row[2]=="word":
    				alleventArray.append([row[5],'word',row[4]])
    		alleventArray = sorted(alleventArray, key=lambda a_entry: a_entry[2])
    		bsecond=0		
    		bsecondutc=begin
    		countt=1
    		countplayer=countplayer+1
    		requestSent=0
    		replyRec=0
    		requestRec=0
    		replySent=0
    		#print(alleventArray)
    		for eventRow in alleventArray:
    			asecond=float(eventRow[2])
    			eventtime =int(asecond-begin)
    			aevent=eventRow[1]
    			if aevent=='requestsent':
    				jj=1
    				sreq=sreq+1
    				requestSent=requestSent+1
    			if aevent=='replyreceived':
    				jj=2
    				replyRec=replyRec+1
    			if aevent=='requestreceived':
    				jj=3
    				requestRec=requestRec+1
    			if aevent=='replysent':
    				jj=4
    				replySent=replySent+1
    				srep=srep+1
    			if aevent=='word':
    				jj=5	

    			eventstring=''
    			for ii in range(bsecond,eventtime):
    				if(countt<=numseconds):
    					playersactions.append([str(datetime.utcfromtimestamp(float(bsecondutc))),str(countt),str(countplayer),str(eventstring),str(player),str(letterstring),str('')])
    					countt=countt+1
    					bsecondutc=bsecondutc+1
    			eventstring=eventRow[0]		
    			
    			if(countt<=numseconds):
    				playersactions.append([str(datetime.utcfromtimestamp(float(bsecondutc))),str(countt),str(countplayer),str(eventstring),str(player),str(letterstring),str(jj)])
    				bsecond=eventtime+1
    				countt=countt+1
    				bsecondutc=bsecondutc+1
    		for ii in range(bsecond,numseconds):
    			if(countt<=numseconds):
    				playersactions.append([str(datetime.utcfromtimestamp(float(bsecondutc))),str(countt),str(countplayer),str(''),str(player),str(letterstring),str('')])
    				countt=countt+1
    				bsecondutc=bsecondutc+1
    	alldatajson.append([phase,begin,n,d,numseconds,playersactions])

    interactionjsondata=[{"phaseid":str(row[0]),"begin":str(row[1]),"n":int(row[2]),"d":int(row[3]),"duration":int(row[4]),"players":[{"timestamp":str(row2[0]),"second":int(row2[1]),"playeridint":int(row2[2]),"payload":str(row2[3]),"playerid":str(row2[4]),"initialparameter":str(row2[5]),"actionid":str(row2[6])} for row2 in row[5]]} for row in alldatajson] 
    json.dump(interactionjsondata,interactionjson,indent=2)
    
### -----------------------------
### Start.
def main(experimentfile,phasedescfile,phasefile,actionfile,playerfile):
		
    jsonfilename = phasedescfile	
    json_phasedesc = open(jsonfilename, 'r')
    phasedesc_data = json.load(json_phasedesc)
    numlinesphasedesc= len(phasedesc_data)
    synchronousactions=[]
    phases=[]
    phasesids=[]
    for i in range(numlinesphasedesc):
    	actions=phasedesc_data[i]["synchronousactions"]
    	for index,row in enumerate(actions):
    		if actions[index]["actionrequest"]!="" and actions[index]["actionreply"]!="":
    			synchronousactions.append([actions[index]["actionrequest"],actions[index]["actionreply"]])
    			if phasedesc_data[i]["phaseid"] not in phases:
    				phases.append(phasedesc_data[i]["phaseid"])
    
    jsonfilename = phasefile	
    json_phase = open(jsonfilename, 'r')
    phase_data = json.load(json_phase)
    numlinesphase= len(phase_data)		
    
    for i in range(numlinesphase):
    	if phase_data[i]["phasedescriptionid"] in phases:
    		phasesids.append(phase_data[i]["phaseid"])
    		
    #print(phasesids)
    #phasesids=["5ydhsfg61","gbwspag31"]
    jsonfilename = actionfile
    json_action = open(jsonfilename, 'r')
    action_data = json.load(json_action)
    numlinesaction= len(action_data)
    returnJson(numlinesaction,action_data,"phaseid",phasesids,experimentfile,playerfile,phasefile)
    print (" -- h1 Transformation --")
    print (" -- good termination --")

## --------------------------
## Execution starts.
if __name__ == '__main__':
	if (len(sys.argv) != 6):
		print ("  Error.  Incorrect usage.")
		print ("  usage: exec infile outfile.")
		print ("  Halt.")
		quit()
	
	experimentfile=sys.argv[1]
	phasedescfile=sys.argv[2]
	phasefile=sys.argv[3]
	actionfile=sys.argv[4]
	playerfile=sys.argv[5]
	main(experimentfile,phasedescfile,phasefile,actionfile,playerfile)
	
    
    	
