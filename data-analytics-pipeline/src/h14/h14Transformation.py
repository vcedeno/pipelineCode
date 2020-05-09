import sys
import os
import csv
import jsonschema
import json
from datetime import time, datetime, timedelta

##player neighbors
## ------------------------------
def getNeighbors(numlines,jreader,rowname1,rowname2,rowid1,rowid2):
    """
    	jreader: json file
    """
    neighbors=[]
    neighborslist=[]
    for i in range(numlines):
    	if jreader[i][rowname1]== rowid1 and jreader[i][rowname2]== rowid2:
    		neighbors=jreader[i]["neighbors"]
    		for index,row in enumerate(neighbors):
    			neighborslist.append(neighbors[index]["neighbor"])
    return "-".join(str(x) for x in neighborslist)
##player letters
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
    return "-".join(str(x) for x in letterslist)

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
def getEvents(windowsize,allactions,numsecondsvalue):
	eventsplayer=[]
	#timer=windowsize
	timer=1
	requestsent=[]
	replyreceived=[]
	requestreceived=[]
	replysent=[]
	words=[]
	aftersecond=''
	lenactions = len(allactions)
	for index,row in enumerate(allactions):
		upsecond=int(row[1])
		if upsecond>=0 and upsecond<numsecondsvalue:
			for i in range(timer,upsecond):	
				if index<(lenactions-1):
					aftersecond=allactions[index+1][1]
				else:
					aftersecond=''
				if timer%windowsize==0 and aftersecond!=upsecond:
					requestsentstring="-".join(str(x) for x in requestsent)
					replyreceivedstring="-".join(str(x) for x in replyreceived)
					requestreceivedstring="-".join(str(x) for x in requestreceived)
					replysentstring="-".join(str(x) for x in replysent)
					wordstring="-".join(str(x) for x in words)
					eventsplayer.append([requestsentstring,replyreceivedstring,requestreceivedstring,replysentstring,wordstring])
					requestsent=[]
					replyreceived=[]
					requestreceived=[]
					replysent=[]
					words=[]
				if aftersecond!=upsecond:
					timer=timer+1
			if str(row[0])=='requestSent':
				requestsent.append(row[2])
			if str(row[0])=='replyReceived':
				replyreceived.append(row[2])
			if str(row[0])=='requestReceived':
				requestreceived.append(row[2])
			if str(row[0])=='replySent':
				replysent.append(row[2])
			if str(row[0])=='word':
				words.append(row[2])
			if timer%windowsize==0 and aftersecond!=upsecond:
				requestsentstring="-".join(str(x) for x in requestsent)
				replyreceivedstring="-".join(str(x) for x in replyreceived)
				requestreceivedstring="-".join(str(x) for x in requestreceived)
				replysentstring="-".join(str(x) for x in replysent)
				wordstring="-".join(str(x) for x in words)
				eventsplayer.append([requestsentstring,replyreceivedstring,requestreceivedstring,replysentstring,wordstring])
				requestsent=[]
				replyreceived=[]
				requestreceived=[]
				replysent=[]
				words=[]
			if aftersecond!=upsecond:
				timer=timer+1

	for i in range(timer,numsecondsvalue+1):
		if timer%windowsize==0:
			requestsentstring="-".join(str(x) for x in requestsent)
			replyreceivedstring="-".join(str(x) for x in replyreceived)
			requestreceivedstring="-".join(str(x) for x in requestreceived)
			replysentstring="-".join(str(x) for x in replysent)
			wordstring="-".join(str(x) for x in words)
			eventsplayer.append([requestsentstring,replyreceivedstring,requestreceivedstring,replysentstring,wordstring])	
			requestsent=[]
			replyreceived=[]
			requestreceived=[]
			replysent=[]
			words=[]		
		timer=timer+1

	return(eventsplayer)

## ------------------------------
def returnJson(numlines,jreader,rowname,phasesids,phasefile,experimentfile,windowsize,nvalue,dvalue,numsecondsvalue,playerfile):
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
    
    jsonfilenamep = playerfile	
    json_player = open(jsonfilenamep, 'r')
    player_data = json.load(json_player)
    numlinesplayer= len(player_data)
    
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
    	numsecondsvalue=int(numsecondsvalue)
    	if str(nvalue)==str(n) and str(dvalue)==str(d):
    		#print("yes")
    		json_experiment.seek(0)
    		players=getPlayers(numlinesexperiment,experiment_data,"experimentid",experimentid)
    		#print(players)
    		countplayer=len(players)
    		playersactions=[]
    		for player in players:
    			json_player.seek(0)
    			letterstring=getLetters(numlinesplayer,player_data,"phaseid","playerid",phase,player)
    			json_player.seek(0)
    			neighborstring=getNeighbors(numlinesplayer,player_data,"phaseid","playerid",phase,player)
    			neighborslist=neighborstring.split("-")
    			nletterslist=[]
    			playerneighbors=[]
    			for neigh in neighborslist:
    				json_player.seek(0)
    				lettersn=getLetters(numlinesplayer,player_data,"phaseid","playerid",phase,neigh)
    				nletterstring=lettersn.split("-")
    				for nletter in nletterstring:
    					nletterslist.append(nletter)
    			nlettersS="".join(str(x) for x in nletterslist)
    			#print(player)
    			#print(letterstring)
    			allactions=[]

    			#print(data)
    			for row in data:
    				if row[1]==player and row[2]=="requestsent":
    					allactions.append(['requestReceived',int(float(row[4])-float(begin)),row[5]])
    				if row[0]==player and row[2]=="replysent":
    					allactions.append(['replySent',int(float(row[4])-float(begin)),row[5]])
    				if row[1]==player and row[2]=="replysent":
    					allactions.append(['replyReceived',int(float(row[4])-float(begin)),row[5]])
    				if row[0]==player and row[2]=="requestsent":
    					allactions.append(['requestSent',int(float(row[4])-float(begin)),row[5]])
    				if row[0]==player and row[2]=="word":
    					allactions.append(['word',int(float(row[4])-float(begin)),row[5]])

    			allactions=sorted(allactions,key=lambda x: x[1])
    			#print(allactions)
    			eventssplayer=getEvents(windowsize,allactions,numsecondsvalue)
    			playersactions.append([player,letterstring,nlettersS,eventssplayer])
    			#alleventArray = sorted(alleventArray, key=lambda a_entry: a_entry[2])
    		
    		alldatajson.append([phase,playersactions])
    
    return alldatajson
    
### -----------------------------
### Start.
def main(experimentfile,phasedescfile,phasefile,actionfile,playerfile,featureid,windowsize,nd,numseconds):
		
    featurejson=open(os.getcwd()+'/data-analytics-pipeline/json-schema/h14/input/datasets/h14.json', 'w')
    featurejson2=open(os.getcwd()+'/property-inference-pipeline/json-schema/inputTransformation/datasets/h14.json', 'w')
    
    jsonfilename = phasedescfile
    json_phasedesc = open(jsonfilename, 'r')
    phasedesc_data = json.load(json_phasedesc)
    numlinesphasedesc= len(phasedesc_data)
    allfeatures=[]
    phases=[]
    phasesids=[]
    #print(phasedesc_data)
    for i in range(numlinesphasedesc):
    	features=phasedesc_data[i]["features"]
    	for index,row in enumerate(features):
    		if features[index]["feature"]!="":
    			allfeatures.append(features[index]["feature"])
    			if phasedesc_data[i]["phaseid"] not in phases:
    				phases.append(phasedesc_data[i]["phaseid"])
    
    jsonfilename = phasefile	
    json_phase = open(jsonfilename, 'r')
    phase_data = json.load(json_phase)
    numlinesphase= len(phase_data)		
    allfeaturesjsondata=[]
    for i in range(numlinesphase):
    	if phase_data[i]["phasedescriptionid"] in phases:
    		phasesids.append(phase_data[i]["phaseid"])

    ndlist=nd.split(",")
    for ndvalue in ndlist:
    	n,d=ndvalue.split("d")
    	v,n=n.split("n")
    	#print(n)
    	#print(d)
    	jsonfilename = actionfile	
    	json_action = open(jsonfilename, 'r')
    	action_data = json.load(json_action)
    	numlinesaction= len(action_data)
    	#phasesids=["5ydhsfg61"]
    	#print(phasesids)
    	featuresjson=returnJson(numlinesaction,action_data,"phaseid",phasesids,phasefile,experimentfile,windowsize,n,d,numseconds,playerfile)
    	allfeaturesjsondata.append([n,d,windowsize,numseconds,featuresjson])
    		
    	#interactionjsondata=[{"phaseid":str(row[0]),"begin":str(row[1]),"n":int(row[2]),"d":int(row[3]),"duration":int(row[4]),"players":[{"timestamp":str(row2[0]),"second":int(row2[1]),"playeridint":int(row2[2]),"payload":str(row2[3]),"playerid":str(row2[4]),"initialparameter":str(row2[5]),"actionid":str(row2[6])} for row2 in row[5]]} for row in alldatajson] 
    featuresjsondata=[{"features":[{"n":int(row[0]),"d":int(row[1]),"windowsize":int(row[2]),"numseconds":int(row[3]),"phases":[{"phaseid":str(row2[0]),"players":[{"playerid":str(row3[0]),"initialLetters":str(row3[1]),"neighborsLetters":str(row3[2]),"timeline":[{"requestsSent":str(row4[0]),"repliesReceived":str(row4[1]),"requestsReceived":str(row4[2]),"repliesSent":str(row4[3]),"words":str(row4[4])} for row4 in row3[3]]}for row3 in row2[1]]}for row2 in row[4]]}]} for row in allfeaturesjsondata]
    json.dump(featuresjsondata,featurejson,indent=2)
    json.dump(featuresjsondata,featurejson2,indent=2)
    print (" -- h14 Transformation --")
    print (" -- good termination --")

## --------------------------
## Execution starts.
if __name__ == '__main__':
		
    if (len(sys.argv) != 9):
    	print ("  Error.  Incorrect usage.")
    	print ("  usage: exec infile outfile.")
    	print ("  Halt.")
    	quit()
    	
    experimentfile=sys.argv[1]
    phasedescfile=sys.argv[2]
    phasefile=sys.argv[3]
    actionfile=sys.argv[4]
    playerfile=sys.argv[5]
    featureid=sys.argv[6]
    windowsize=sys.argv[7]
    nd=sys.argv[9]
    numseconds=sys.argv[9]
    main(experimentfile,phasedescfile,phasefile,actionfile,featureid,windowsize,nd,numseconds)
    
    