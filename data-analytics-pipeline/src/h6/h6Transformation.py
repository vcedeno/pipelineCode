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
def returnJson(actionname,numlines,jreader,rowname,phasesids,phasefile,experimentfile,bin):
    """
    	jreader: json file
    """
    
    data=[]
    alldatajson=[]
    jsonfilename = phasefile
    json_phase = open(jsonfilename, 'r')
    phase_data = json.load(json_phase)
    numlinesphase= len(phase_data)
    
    jsonfilename = experimentfile	
    json_experiment = open(jsonfilename, 'r')
    experiment_data = json.load(json_experiment)
    numlinesexperiment= len(experiment_data)
    
    labelx='CDF for number of '+actionname
    
    actionrequest,actionreply=actionname.split('-')
    
    for i in range(numlines):
    	if jreader[i][rowname]in phasesids:
    		actions=jreader[i]["actionlist"]
    		for index,row in enumerate(actions):
    			data.append([actions[index]["player1"],actions[index]["player2"],actions[index]["actionid"],actions[index]["playerActionSeqid"],actions[index]["timestamp"],actions[index]["payload"]])
    for phase in phasesids:  	
    	json_phase.seek(0)
    	begin,numseconds,n,d,experimentid=getPhase(numlinesphase,phase_data,"phaseid",phase)
    	numseconds=int(numseconds)
    	#print("poi")
    	#print(str(numseconds))
    	allactions=[]
    	json_experiment.seek(0)
    	players=getPlayers(numlinesexperiment,experiment_data,"experimentid",experimentid)
    	#print(players)
    	countplayer=len(players)
    	playersactions=[]
    	for player in players:
    		#json_player.seek(0)
    		#letterstring=getLetters(numlinesplayer,player_data,"phaseid","playerid",phase,player)
    		#print(player)
    		#print(letterstring)
    		#print(data)
    		allrequests=[]
    		allrequests2=[]
    		for row in data:
    			if row[0]==player and row[2]==actionrequest:
    				allrequests.append([row[3],row[2],row[4]])
    			if row[1]==player and row[2]==actionreply:
    				allrequests2.append([row[3],row[2],row[4]])
    		
    		for row in allrequests:
    			t2=''
    			if row[1]==actionrequest:
    				for row1 in allrequests2:
    					if row1[0]==row[0] and row1[1]==actionreply:
    						playersactions.append(row1[2]-row[2])
    			
    		#actions=[]		
    		#value=0	
    		#for row in allactions:
    		#	upsecond=int(row[2]-begin)
    		#	if upsecond>=0 and upsecond<numseconds:
    		#		if row[1]==actionname:
    		#			actions.append(upsecond)
    					
    		#if len(actions)==0:
    		#	allrequests=[['','','']]
    		#playersactions.append([player,actions])
    		#alleventArray = sorted(alleventArray, key=lambda a_entry: a_entry[2])
    	
    	alldatajson.append([phase,begin,n,d,numseconds,countplayer,playersactions])
    	#print(phase)
    	#print(averageactions)
    return alldatajson
    
### -----------------------------
### Start.
def main(experimentfile,phasedescfile,phasefile,actionfile,actionidvisualize,bin):
		
    interactionjson=open(os.getcwd()+'/data-analytics-pipeline/json-schema/h6/input/datasets/h6.json', 'w')
    jsonfilename = phasedescfile
    json_phasedesc = open(jsonfilename, 'r')
    phasedesc_data = json.load(json_phasedesc)
    numlinesphasedesc= len(phasedesc_data)
    allactions=[]
    phases=[]
    phasesids=[]
    for i in range(numlinesphasedesc):
    	actions=phasedesc_data[i]["synchronousactions"]
    	for index,row in enumerate(actions):
    		if actions[index]["actionrequest"]!="":
    			actionrequest=actions[index]["actionrequest"]
    		if actions[index]["actionreply"]!="":
    			allactions.append(actionrequest+'-'+actions[index]["actionreply"])
    			if phasedesc_data[i]["phaseid"] not in phases:
    				phases.append(phasedesc_data[i]["phaseid"])
    
    jsonfilename = phasefile	
    json_phase = open(jsonfilename, 'r')
    phase_data = json.load(json_phase)
    numlinesphase= len(phase_data)		
    allinteractionjsondata=[]
    for i in range(numlinesphase):
    	if phase_data[i]["phasedescriptionid"] in phases:
    		phasesids.append(phase_data[i]["phaseid"])
    
    if actionidvisualize=="all":
    	for action in allactions:
    		jsonfilename = actionfile	
    		json_action = open(jsonfilename, 'r')
    		action_data = json.load(json_action)
    		numlinesaction= len(action_data)
    		#phasesids=["5ydhsfg61"]
    		#print(phasesids)
    		actionsjson=returnJson(action,numlinesaction,action_data,"phaseid",phasesids,phasefile,experimentfile,bin)
    		allinteractionjsondata.append([action,bin,actionsjson])
    elif actionidvisualize in allactions:
    	jsonfilename = actionfile	
    	json_action = open(jsonfilename, 'r')
    	action_data = json.load(json_action)
    	numlinesaction= len(action_data)
    	#phasesids=["5ydhsfg61"]
    	#print(phasesids)
    	actionsjson=returnJson(actionidvisualize,numlinesaction,action_data,"phaseid",phasesids,phasefile,experimentfile,bin)
    	allinteractionjsondata.append([actionidvisualize,bin,actionsjson])

    	#interactionjsondata=[{"phaseid":str(row[0]),"begin":str(row[1]),"n":int(row[2]),"d":int(row[3]),"duration":int(row[4]),"players":[{"timestamp":str(row2[0]),"second":int(row2[1]),"playeridint":int(row2[2]),"payload":str(row2[3]),"playerid":str(row2[4]),"initialparameter":str(row2[5]),"actionid":str(row2[6])} for row2 in row[5]]} for row in alldatajson] 
    #print(allinteractionjsondata)
    interactionjsondata=[{"actions":[{"action":str(row[0]),"bin":int(row[1]),"phases":[{"phaseid":str(row2[0]),"begin":str(row2[1]),"n":int(row2[2]),"d":int(row2[3]),"duration":int(row2[4]),"numplayers":int(row2[5]),"timestamp":[{"value":str(row3)}for row3 in row2[6]]}for row2 in row[2]]}]} for row in allinteractionjsondata]
    json.dump(interactionjsondata,interactionjson,indent=2)
    print (" -- h6 Transformation --")
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
    actionidvisualize=sys.argv[5]
    main(experimentfile,phasedescfile,phasefile,actionfile,actionidvisualize)
    
    