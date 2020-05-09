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
def getEvents(windowsize,allactions,begin,numsecondsvalue):
	featuresplayer=[]
	featurescount=[]
	#timer=windowsize
	timer=0
	value=0
	valueevent=1
	count=0
	for row in allactions:
		upsecond=int(row[2]-begin)
		if upsecond>=0 and upsecond<numsecondsvalue:
			for i in range(timer,upsecond):	
				#if timer%windowsize==0:
				featuresplayer.append(valueevent)
				featurescount.append(count)
				count=count+1
					#print(timer)
					#print(valueevent)
				timer=timer+1
			value=value+1
			count=0
			if row[1]=="requestsent":
				valueevent=3
			if row[1]=="replysent":
				valueevent=2
			if row[1]=="word":
				valueevent=4
			#if timer%windowsize==0:
			featuresplayer.append(valueevent)
			featurescount.append(count)
				#print(timer)
				#print(valueevent)
			timer=timer+1
			value=value+1
			valueevent=1
			count=count+1
	for i in range(timer,numsecondsvalue):
		if timer%windowsize==0:
			featuresplayer.append(valueevent)
			featurescount.append(count)
			count=count+1
		timer=timer+1
		if timer==(numsecondsvalue+1) and timer%windowsize!=0:
			newwindow=int(numsecondsvalue/windowsize)*windowsize+windowsize
			featuresplayer.append(valueevent)
			featurescount.append(count)
	#print("oi")
	#print(featuresplayer)
	return(featuresplayer,featurescount)

 ## ------------------------------
def getBuffer(buffer,numseconds):
    """
    	reader: csv file
    	column: the column we want the data from.
        key: for example session_code or participant_code.
    """
    
    buffer = sorted(buffer, key=lambda a_entry: a_entry[0])
    sbegin=0
    bufferevent=[]	
    xRpyS=[]
    count=0
    countxRpyS=0
    for row in buffer:
    	point=int(row[0])
    	if point<numseconds:
    		for ii in range(sbegin,point):
    			bufferevent.append(count)
    			xRpyS.append(countxRpyS)
    		if row[1]==0:
    			count=count+1
    		if row[1]==1:
    			countxRpyS=countxRpyS+1
    			count=count-1
    		sbegin=point
    for ii in range(sbegin,numseconds):
    	bufferevent.append(count)
    	xRpyS.append(countxRpyS)
    #print(bufferevent)
    #myString = ",".join(str(x) for x in bufferevent)
    #unique = set(words) 
    #uWords=len(unique)	
    #return myString 
    #print(len(xRpyS))
    #print(len(bufferevent))
    return bufferevent,xRpyS
 ## ------------------------------
def getWords(buffer,numseconds):
    """
    	reader: csv file
    	column: the column we want the data from.
        key: for example session_code or participant_code.
    """
    buffer = sorted(buffer, key=lambda a_entry: a_entry[0])
    sbegin=0
    bufferevent=[]
    count=0
    for row in buffer:
    	point=row[0]
    	if point<numseconds:
    		for ii in range(sbegin,point):
    			bufferevent.append(count)
    		sbegin=point
    		count=count+1
    for ii in range(sbegin,numseconds):
    	bufferevent.append(count)
    return bufferevent
 ## ------------------------------
def getrequestsent(buffer,numseconds):
    """
    	reader: csv file
    	column: the column we want the data from.
        key: for example session_code or participant_code.
    """
    buffer = sorted(buffer, key=lambda a_entry: a_entry[0])
    sbegin=0
    bufferevent=[]	
    count=0
    for row in buffer:
    	point=row[0]
    	if point<numseconds:
    		for ii in range(sbegin,point):
    			bufferevent.append(count)
    		sbegin=point
    		count=count+1
    for ii in range(sbegin,numseconds):
    	bufferevent.append(count)
    return bufferevent
 ## ------------------------------
def getrequestreceived(buffer,numseconds):
    """
    	reader: csv file
    	column: the column we want the data from.
        key: for example session_code or participant_code.
    """
    buffer = sorted(buffer, key=lambda a_entry: a_entry[0])
    sbegin=0
    bufferevent=[]	
    count=0
    for row in buffer:
    	point=row[0]
    	if point<numseconds:
    		for ii in range(sbegin,point):
    			bufferevent.append(count)
    		sbegin=point
    		count=count+1
    for ii in range(sbegin,numseconds):
    	bufferevent.append(count)
    return bufferevent
 ## ------------------------------
def getLettersEvent(buffer,numseconds):
    """
    	reader: csv file
    	column: the column we want the data from.
        key: for example session_code or participant_code.
    """
    initialLetters=3
    buffer = sorted(buffer, key=lambda a_entry: a_entry[0])
    sbegin=0
    bufferevent=[]	
    xRpyR=[]	
    count=initialLetters
    countxRpyR=0
    for row in buffer:
    	point=row[0]
    	if point<numseconds:
    		for ii in range(sbegin,point):
    			bufferevent.append(count)
    			xRpyR.append(countxRpyR)
    		sbegin=point
    		count=count+1
    		countxRpyR=countxRpyR+1
    for ii in range(sbegin,numseconds):
    	bufferevent.append(count)
    	xRpyR.append(countxRpyR)
    #print(len(xRpyR))
    #print(len(bufferevent))
    return bufferevent,xRpyR
## ------------------------------
def returnJson(allfeatureslist,numlines,jreader,rowname,phasesids,phasefile,experimentfile,windowsize,nvalue,dvalue,numsecondsvalue):
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

    for i in range(numlines):
    	if jreader[i][rowname]in phasesids:
    		actions=jreader[i]["actionlist"]
    		for index,row in enumerate(actions):
    			data.append([actions[index]["player1"],actions[index]["player2"],actions[index]["actionid"],actions[index]["playerActionSeqid"],actions[index]["timestamp"],actions[index]["payload"]])
    for phase in phasesids:  	
    	json_phase.seek(0)
    	begin,numseconds,n,d,experimentid=getPhase(numlinesphase,phase_data,"phaseid",phase)
    	numseconds=int(numseconds)
    	numsecondsvalue=int(numsecondsvalue)
    	if str(nvalue)==str(n) and str(dvalue)==str(d):
    		json_experiment.seek(0)
    		players=getPlayers(numlinesexperiment,experiment_data,"experimentid",experimentid)
    		#print(players)
    		countplayer=len(players)
    		playersactions=[]
    		for player in players:
    			allfeaturesplayer=[]
    			#json_player.seek(0)
    			#letterstring=getLetters(numlinesplayer,player_data,"phaseid","playerid",phase,player)
    			#print(player)
    			#print(letterstring)
    			allactions=[]
    			buffer=[]
    			requestome=[]
    			replytothem=[]
    			replytome=[]
    			requestsent=[]
    			requestreceived=[]
    			words=[]
    			#print(data)
    			for row in data:
    				if row[0]==player:
    					allactions.append([row[3],row[2],float(row[4])])
    				if row[1]==player and row[2]=="requestsent":
    					requestome.append([row[0],row[2],int(row[3]),float(row[4])])
    					requestreceived.append([int(float(row[4])-float(begin))])
    				if row[0]==player and row[2]=="replysent":
    					replytothem.append([row[1],row[2],int(row[3]),float(row[4])])
    				if row[1]==player and row[2]=="replysent":
    					replytome.append([int(float(row[4])-float(begin))])
    				if row[0]==player and row[2]=="word":
    					words.append([int(float(row[4])-float(begin))])
    				if row[0]==player and row[2]=="requestsent":
    					requestsent.append([int(float(row[4])-float(begin))])
    		
    			for request in requestome:
    				#flag=0
    				for reply in replytothem:
    					if request[0]==reply[0] and request[2]==reply[2]:
    						#flag=1
    						timev=reply[3]-float(begin)
    						if timev<numsecondsvalue:
    							buffer.append([int(timev),1])
    				#if flag==0:
    				timev=request[3]-float(begin)
    				if timev<numsecondsvalue:
    					buffer.append([int(timev),0])
    					
    			allactions=sorted(allactions,key=lambda x: x[2])
    			for row in allfeatureslist:
    				if row =='XE':
    					featuresplayer,featurescount=getEvents(windowsize,allactions,begin,numsecondsvalue)
    					allfeaturesplayer.append([row,featuresplayer])
    				if row =='XB':
    					featuresplayer,xRpyS=getBuffer(buffer,numsecondsvalue)
    					allfeaturesplayer.append([row,featuresplayer])
    				if row =='XL':
    					featuresplayer,xRpyR=getLettersEvent(replytome,numsecondsvalue)
    					allfeaturesplayer.append([row,featuresplayer])
    				if row =='XW':
    					featuresplayer=getWords(words,numsecondsvalue)
    					allfeaturesplayer.append([row,featuresplayer])
    				if row =='XC':
    					allfeaturesplayer.append([row,featurescount])
    				if row =='xReqS':
    					featuresplayer=getrequestsent(requestsent,numsecondsvalue)
    					allfeaturesplayer.append([row,featuresplayer])
    				if row =='xRpyR':
    					allfeaturesplayer.append([row,xRpyR])
    				if row =='xReqR':
    					featuresplayer=getrequestreceived(requestreceived,numsecondsvalue)
    					allfeaturesplayer.append([row,featuresplayer])
    				if row =='xRpyS':
    					allfeaturesplayer.append([row,xRpyS])
    				
    		
    			#if len(actions)==0:
    			#	allrequests=[['','','']]
    			playersactions.append([player,allfeaturesplayer])
    			#alleventArray = sorted(alleventArray, key=lambda a_entry: a_entry[2])
    	
    	alldatajson.append([phase,playersactions])
    	#print(averageactions)
    return alldatajson
    
### -----------------------------
### Start.
def main(experimentfile,phasedescfile,phasefile,actionfile,featureid,windowsize,nd,numseconds):
		
    featurejson=open(os.getcwd()+'/data-analytics-pipeline/json-schema/h7/input/datasets/h7.json', 'w')
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
    
    if featureid=="all":
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
    		featuresjson=returnJson(allfeatures,numlinesaction,action_data,"phaseid",phasesids,phasefile,experimentfile,windowsize,n,d,numseconds)
    		allfeaturesjsondata.append([n,d,windowsize,numseconds,featuresjson])
    else:
    	allfeatureslist=[]
    	n=0
    	d=0
    	featurelist=actionidvisualize.split(",")
    	for feature in featurelist:
    		if feature in allfeatures:
    			allfeatureslist.append(feature)
    	ndlist=nd.split(",")
    	for ndvalue in ndlist:
    		n,d=ndvalue.split("d")
    		v,n=n.split("n")
    		print(n)
    		print(d)
    		jsonfilename = actionfile	
    		json_action = open(jsonfilename, 'r')
    		action_data = json.load(json_action)
    		numlinesaction= len(action_data)
    		#phasesids=["5ydhsfg61"]
    		#print(phasesids)
    		featuresjson=returnJson(allfeatureslist,numlinesaction,action_data,"phaseid",phasesids,phasefile,experimentfile,windowsize,n,d,numseconds)
    		allfeaturesjsondata.append([n,d,windowsize,numseconds,featuresjson])
    #print(allfeaturesjsondata)
    		
    	#interactionjsondata=[{"phaseid":str(row[0]),"begin":str(row[1]),"n":int(row[2]),"d":int(row[3]),"duration":int(row[4]),"players":[{"timestamp":str(row2[0]),"second":int(row2[1]),"playeridint":int(row2[2]),"payload":str(row2[3]),"playerid":str(row2[4]),"initialparameter":str(row2[5]),"actionid":str(row2[6])} for row2 in row[5]]} for row in alldatajson] 
    featuresjsondata=[{"features":[{"n":int(row[0]),"d":int(row[1]),"windowsize":int(row[2]),"numseconds":int(row[3]),"phases":[{"phaseid":str(row2[0]),"players":[{"playerid":str(row3[0]),"features":[{"featureid":str(row4[0]),"timeline":[{"value":int(row5)}for row5 in row4[1]]} for row4 in row3[1]]}for row3 in row2[1]]}]}for row2 in row[4]]} for row in allfeaturesjsondata]
    json.dump(featuresjsondata,featurejson,indent=2)
    print (" -- h7 Transformation --")
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
    featureid=sys.argv[5]
    windowsize=sys.argv[6]
    nd=sys.argv[7]
    numseconds=sys.argv[8]
    main(experimentfile,phasedescfile,phasefile,actionfile,featureid,windowsize,nd,numseconds)
    
    