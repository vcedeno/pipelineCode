#!/usr/bin/env python
### V. Cedeno
### 06 jul 2017.
### Take experiment 1 output data
### and generate plot files.
### input files:
###     
### output files:
###      Users interaction plot
###     


### Modification History
### --------------------

import sys
import os
import csv
import operator
from datetime import time, datetime, timedelta
from itertools import cycle
#import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import time
import glob
import json

## ------------------------------
def getts(tsevent,tseventP,numseconds):
    """
    	reader: csv file
    	column: the column we want the data from.
        key: for example session_code or participant_code.
    """
    tsxc=np.zeros(numseconds)
    tsreqSent=np.zeros(numseconds)
    tsrepRec=np.zeros(numseconds)
    tsreqRec=np.zeros(numseconds)
    tsrepSent=np.zeros(numseconds)
    s=0
    sentreq=0
    sentreply=0
    count=0
    for row in tsevent:
    	if row!=1:
    		s=0
    	if row==3:
    		sentreq=sentreq+1
    	if row==2:
    		sentreply=sentreply+1
    	tsreqSent[count]=sentreq	
    	tsrepSent[count]=sentreply
    	tsxc[count]=s
    	s=s+1
    	count=count+1
    
    count=0
    recreq=0
    recreply=0
    for row in tseventP:
    	if row==3:
    		recreq=recreq+1
    	if row==2:
    		recreply=recreply+1
    	tsreqRec[count]=recreq	
    	tsrepRec[count]=recreply	
    	count=count+1   	 
    
    return tsxc,tsreqSent,tsrepRec,tsreqRec,tsrepSent
## ------------------------------
def getFormedWords(words,numseconds):
    """
    	reader: csv file
    	column: the column we want the data from.
        key: for example session_code or participant_code.
    """

    sbegin=0
    wordevent=[]
    count=0
    for row in words:
    	point=int(row)
    	if point<numseconds:
    		for ii in range(sbegin,point):
    			wordevent.append(count)
    		count=count+1
    		sbegin=point
    for ii in range(sbegin,numseconds):
    	wordevent.append(count)
    #myString = ",".join(str(x) for x in wordevent)
    #unique = set(words) 
    #uWords=len(unique)	
    return wordevent   
 ## ------------------------------
def getAvailableLetters(reader,timeb,numseconds):
    """
    	reader: csv file
    	column: the column we want the data from.
        key: for example session_code or participant_code.
    """
    letters=[]
    uniquel=[]
    for row in reader:
    	if row[0] not in uniquel:
    		letters.append(float(row[1])-timeb)
    		uniquel.append(row[0])
    letters = sorted(letters, key=lambda a_entry: a_entry)
    sbegin=0
    letterevent=[]
    count=3
    for row in letters:
    	point=int(row)
    	if point<numseconds:
    		for ii in range(sbegin,point):
    			letterevent.append(count)
    		count=count+1
    		sbegin=point
    for ii in range(sbegin,numseconds):
    	letterevent.append(count)
    #myString = ",".join(str(x) for x in letterevent)
    #unique = set(words) 
    #uWords=len(unique)	
    #return myString   
    return letterevent   
    
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
    count=0
    for row in buffer:
    	point=int(row[0])
    	if point<numseconds:
    		for ii in range(sbegin,point):
    			bufferevent.append(count)
    		if row[1]==0:
    			count=count+1
    		if row[1]==1:
    			count=count-1
    		sbegin=point
    for ii in range(sbegin,numseconds):
    	bufferevent.append(count)
    #print(bufferevent)
    #myString = ",".join(str(x) for x in bufferevent)
    #unique = set(words) 
    #uWords=len(unique)	
    #return myString 
    return bufferevent
## ------------------------------
def returnJsonFour(numlines,jreader,jname, rowname, rowid, returnrowid1,returnrowid2,returnrowid3,returnrowid4):
    """
    	ireader: csv file
        session_code: the session_code we want the data from.
    """
    data=[]
    for i in range(numlines):
    	#print(jreader[jname][i][rowname])
    	#print(jreader["CompletedSessionSummary"][i]["experiment_type"])
    	if jreader[jname][i][rowname]==rowid:
    		data.append([jreader[jname][i][returnrowid1],jreader[jname][i][returnrowid2],jreader[jname][i][returnrowid3],jreader[jname][i][returnrowid4]])
    return data

## ------------------------------
def returnJsonThree(numlines,jreader,jname, rowname, rowid, returnrowid1,returnrowid2,returnrowid3):
    """
    	ireader: csv file
        session_code: the session_code we want the data from.
    """
    data=[]
    for i in range(numlines):
    	#print(jreader[jname][i][rowname])
    	#print(jreader["CompletedSessionSummary"][i]["experiment_type"])
    	if jreader[jname][i][rowname]==rowid:
    		data.append([jreader[jname][i][returnrowid1],jreader[jname][i][returnrowid2],jreader[jname][i][returnrowid3]])
    return data
    
## ------------------------------
def returnJsonTwo(numlines,jreader,jname, rowname, rowid, returnrowid1,returnrowid2):
    """
    	ireader: csv file
        session_code: the session_code we want the data from.
    """
    data=[]
    for i in range(numlines):
    	if jreader[jname][i][rowname]==rowid:
    		data.append([jreader[jname][i][returnrowid1],jreader[jname][i][returnrowid2]])
    return data
    
## ------------------------------
def returnJsonTwoTwo(numlines,jreader,jname, rowname1, rowname2, rowid1, rowid2, returnrowid1,returnrowid2):
    """
    	ireader: csv file
        session_code: the session_code we want the data from.
    """
    data=[]
    for i in range(numlines):
    	#print(jreader[jname][i][rowname])
    	#print(jreader["CompletedSessionSummary"][i]["experiment_type"])
    	if jreader[jname][i][rowname1]==rowid1 and jreader[jname][i][rowname2]==rowid2:
    		data.append([jreader[jname][i][returnrowid1],jreader[jname][i][returnrowid2]])
    return data

##scrabble score
SCORES = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2, 
          "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3, 
          "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1, 
          "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4, 
          "x": 8, "z": 10}

## ------------------------------
def scrabble_score(word):
    """
    	word: word we eant the scrabble score form
    """
    score=sum(SCORES[letter] for letter in word)
    return score


## ------------------------------
def getNeighbors(numlines,jreader,jname,rowname,player):
    """
    	ireader: csv file
        session_code: the session_code we want the data from.
    """
    k=0
    col=0
    
    neighbors=[]
    
    for i in range(numlines):
    	if jreader[jname][i][rowname]==player:
    		ncol=len(jreader[jname][i])
    		while col <(ncol-2):
    			name="neighbor__"+str(col)+"__participant__code"
    			if jreader[jname][i][name] !='':
    				neighbors.append(jreader[jname][i][name])
    			col=col+1
    return neighbors
      
## ------------------------------
def getNumberNeighbors(numlines,jreader,jname,rowname,player):
    """
    	ireader: csv file
        session_code: the session_code we want the data from.
    """
    k=0
    col=0
    count=0
    
    for i in range(numlines):
    	if jreader[jname][i][rowname]==player:
    		ncol=len(jreader[jname][i])
    		while col <(ncol-2):
    			name="neighbor__"+str(col)+"__participant__code"
    			if jreader[jname][i][name] !='':
    				count=count+1
    			col=col+1
    return count
  
## ------------------------------
def returnJson(numlines,jreader,jname,rowname,rowid,returnrowid):
    """
    	ireader: csv file
        session_code: the session_code we want the data from.
    """
    data=[]
    for i in range(numlines):
    	#print(jreader[jname][i][rowname])
    	#print(jreader["CompletedSessionSummary"][i]["experiment_type"])
    	if jreader[jname][i][rowname]==rowid:
    		if jreader[jname][i][returnrowid] not in data:
    			data.append(jreader[jname][i][returnrowid])
    return data
    
  
## ------------------------------
def getPlayersWordsTime(reader, player, begin):
    """
    	ireader: csv file
        session_code: the session_code we want the data from.
    """
    times=[]
    for row in reader:
    	if row[3]==player:
    		value=float(row[6])-float(begin)
    		if value<300:
    			times.append(value)
    return times
    
### -----------------------------
### Start.
def main(inputpath,anagrams,CompletedSessionSummary,InstructionsAnagrams,LetterTransactions,Neighbors,PublicGoods,TeamWords,TimeSpent,UserLetters):
	allfiles=[anagrams,CompletedSessionSummary,InstructionsAnagrams,LetterTransactions,Neighbors,PublicGoods,TeamWords,TimeSpent,UserLetters]
	startTime = datetime.now()
	cojson = inputpath+'/'+CompletedSessionSummary+'.json'
	uletter = inputpath+'/'+UserLetters+'.json'
	tspent = inputpath+'/'+TimeSpent+'.json'
	twords = inputpath+'/'+TeamWords+'.json'
	neighbors= inputpath+'/'+Neighbors+'.json'
	letrans= inputpath+'/'+LetterTransactions+'.json'
	pgoods= inputpath+'/'+PublicGoods+'.json'
	ianagrams= inputpath+'/'+InstructionsAnagrams+'.json'
	anagrams= inputpath+'/'+anagrams+'.json'
	sessions=[]
	sessionsphase2=[]
	json_cose = open(cojson, 'r')
	co_data = json.load(json_cose)
	numlinescose= (len(co_data['CompletedSessionSummary']))
	sessions=returnJsonFour(numlinescose,co_data,"CompletedSessionSummary", "experiment_type", "Public Goods Game - IRB.v2", "session_code","n_part_requested","start_time","duration")
	sessionsphase2=returnJsonFour(numlinescose,co_data,"CompletedSessionSummary", "experiment_type", "Public Goods Game - IRB.v2 No Anagrams", "session_code","n_part_requested","start_time","duration")
	json_pgoods = open(pgoods, 'r')
	pg_data = json.load(json_pgoods)
	numlinespg= (len(pg_data['PublicGoods']))
	json_usle = open(uletter, 'r')
	ul_data = json.load(json_usle)
	numlinesusle= (len(ul_data['UserLetters']))
	json_tspent = open(tspent, 'r')
	ts_data = json.load(json_tspent)
	numlinests= (len(ts_data['TimeSpent']))
	json_tw = open(twords, 'r')
	tw_data = json.load(json_tw)
	numlinestw= (len(tw_data['TeamWords']))
	json_ne = open(neighbors, 'r')
	ne_data = json.load(json_ne)
	numlinesne= (len(ne_data['Neighbors']))
	json_lt = open(letrans, 'r')
	lt_data = json.load(json_lt)
	numlineslt= (len(lt_data['LetterTransactions']))
	json_ia = open(ianagrams, 'r')
	ia_data = json.load(json_ia)
	numlinesia= (len(ia_data['InstructionsAnagrams']))
	json_a = open(anagrams, 'r')
	a_data = json.load(json_a)
	numlinesa= (len(a_data['Anagrams']))
	experimentjson=open(os.getcwd()+'/experiment-pipeline/test/results/h1/output/datasets/experiment.json', 'w')	
	phasedescjson=open(os.getcwd()+'/experiment-pipeline/test/results/h1/output/datasets/phasedesc.json', 'w')
	phasejson=open(os.getcwd()+'/experiment-pipeline/test/results/h1/output/datasets/phase.json', 'w')	
	actionjson=open(os.getcwd()+'/experiment-pipeline/test/results/h1/output/datasets/action.json', 'w')	
	playerjson=open(os.getcwd()+'/experiment-pipeline/test/results/h1/output/datasets/player.json', 'w')	
	
	experimentjson2=open(os.getcwd()+'/data-analytics-pipeline/json-schema/inputTransformation/datasets/experiment.json', 'w')	
	phasedescjson2=open(os.getcwd()+'/data-analytics-pipeline/json-schema/inputTransformation/datasets/phasedesc.json', 'w')
	phasejson2=open(os.getcwd()+'/data-analytics-pipeline/json-schema/inputTransformation/datasets/phase.json', 'w')	
	actionjson2=open(os.getcwd()+'/data-analytics-pipeline/json-schema/inputTransformation/datasets/action.json', 'w')	
	playerjson2=open(os.getcwd()+'/data-analytics-pipeline/json-schema/inputTransformation/datasets/player.json', 'w')
	
	alldataexperimentjson=[]
	alldataphasejson=[]
	alldataphasedescjson=[]
	alldataactionjson=[]
	alldataplayerjson=[]
	players=[]
	nexperiment=0
	numseconds=300
	beginparphase1=["letter1","letter2","letter3","difi1distanceScale","difi1overlapScale"]
	endparphase1=["numWords","scrabblescore"]
	beginparphase2=["difi2distanceScale","difi2overlapScale"]
	endparphase2=["contribution","profit","difi3distanceScale","difi3overlapScale"]
	actions=["word","requestsent","replysent"]
	synchronousactions=[["requestsent","replysent"]]
	features=["XE","XB","XL","XW","XC","xReqS","xRpyR","xReqR","xRpyS"]
	alldataphasedescjson.append(["anagrams",beginparphase1,endparphase1,actions,synchronousactions,features])
		
	alldataphasedescjson.append(["publicgoods",beginparphase2,endparphase2,[""],[["",""]],[""]])
	for row in sessionsphase2:
		activeplayers=[]
		phaseid=row[0]
		json_pgoods.seek(0)
		players=returnJson(numlinespg,pg_data,"PublicGoods", "session.code", row[0], "participant.code")
		maxinit=0
		minresta=int(time.time())
		for player in players:
			json_tspent.seek(0)
			lines=returnJsonFour(numlinests,ts_data,"TimeSpent", "participant__code", player, "app_name","page_name","time_stamp","seconds_on_page")
			for line in lines:
				if line[0]=='public_goods' and line[1]=='Results':
					if float(line[2])>maxinit:
						maxinit=float(line[2])
					activeplayers.append(player)
					resta=float(line[2])-int(line[3])
					if resta<minresta:
						minresta=resta
		timeend=maxinit
		duration=maxinit-minresta
		begin=int(timeend)-int(duration)
		end=begin+numseconds
		for player in activeplayers:
			beginparvalues2=[]
			endparvalues2=[]
			json_ia.seek(0)
			difi2=returnJsonTwo(numlinesia,ia_data,"InstructionsAnagrams", "participant.code", player, "player.distanceScale_before","player.overlapScale_before")
			if len(difi2)>0:
				beginparvalues2.append(["difi2distanceScale",difi2[0][0]])
				beginparvalues2.append(["difi2overlapScale",difi2[0][1]])
			json_pgoods.seek(0)
			difi3=returnJsonFour(numlinespg,pg_data,"PublicGoods", "participant.code", player, "player.contribution","player.profit","player.distanceScale","player.overlapScale")
			if len(difi3)>0:
				endparvalues2.append(["contribution",difi3[0][0]])
				endparvalues2.append(["profit",difi3[0][1]])
				endparvalues2.append(["difi3distanceScale",difi3[0][2]])
				endparvalues2.append(["difi3overlapScale",difi3[0][3]])	
			alldataplayerjson.append([phaseid,player,[""],beginparvalues2,endparvalues2])
		if float(row[3])>0:
			nexperiment=nexperiment+1
			alldataexperimentjson.append([int(nexperiment),1,int(float(row[1])),0,row[2],row[3],activeplayers])
			alldataphasejson.append([phaseid,"publicgoods",int(nexperiment),1,int(begin),int(duration),0,int(float(row[1]))])
	for row in sessions:
		activeplayers=[]
		actionsplayer=[]
		phaseid1=row[0]+"1"
		phaseid2=row[0]+"2"
		json_usle.seek(0)
		players=returnJson(numlinesusle,ul_data,"UserLetters", "player__participant__session__code", row[0], "player__participant__code")
		maxinit=0
		minresta=int(time.time())
		maxinit2=0
		minresta2=int(time.time())
		for player in players:
			json_tspent.seek(0)
			lines=returnJsonFour(numlinests,ts_data,"TimeSpent", "participant__code", player, "app_name","page_name","time_stamp","seconds_on_page")
			for line in lines:
				if line[0]=='anagrams' and line[1]=='Anagrams':
					if float(line[2])>maxinit:
						maxinit=float(line[2])
					activeplayers.append(player)
					resta=float(line[2])-int(line[3])
					if resta<minresta:
						minresta=resta
				if line[0]=='public_goods' and line[1]=='Results':
					if float(line[2])>maxinit2:
						maxinit2=float(line[2])
					resta2=float(line[2])-int(line[3])
					if resta2<minresta2:
						minresta2=resta2
		timeend=maxinit
		duration=maxinit-minresta
		begin=int(timeend)-int(duration)
		end=begin+numseconds
		timeend2=maxinit2
		duration2=maxinit2-minresta2
		begin2=int(timeend2)-int(duration2)
		end2=begin2+numseconds
		for player in activeplayers:
			actionplayer=[]
			beginparvalues1=[]
			endparvalues1=[]
			beginparvalues2=[]
			endparvalues2=[]
			json_tw.seek(0)
			events=returnJsonTwo(numlinestw,tw_data,"TeamWords", "player__participant__code", player, "timestamp","word")
			numwords=len(events)
			scrabblescore=0
			for wordevent in events:
				scrabblescore=scrabblescore+scrabble_score(wordevent[1])
			endparvalues1.append(["numWords",numwords])
			endparvalues1.append(["scrabblescore",scrabblescore])
			if len(events)>0:
				for eventitem in events:
					actionplayer.append([eventitem[0],eventitem[1]])
			json_lt.seek(0)
			events=returnJsonTwo(numlineslt,lt_data,"LetterTransactions", "player__participant__code", player, "timestamp","letter__letter")
			if len(events)>0:
				for eventitem in events:
					actionplayer.append([eventitem[0],eventitem[1]])
			json_ne.seek(0)
			neighborsvalues=getNeighbors(numlinesne,ne_data,"Neighbors","player__participant__code",player)
			json_usle.seek(0)
			letters=returnJson(numlinesusle,ul_data,"UserLetters", "player__participant__code", player, "letter")
			beginparvalues1.append(["letter1",letters[0]])
			beginparvalues1.append(["letter2",letters[1]])
			beginparvalues1.append(["letter3",letters[2]])
			
			json_ia.seek(0)
			difi1=returnJsonTwo(numlinesia,ia_data,"InstructionsAnagrams", "participant.code", player, "player.distanceScale_before","player.overlapScale_before")
			if len(difi1)>0:
				beginparvalues1.append(["difi1distanceScale",difi1[0][0]])
				beginparvalues1.append(["difi1overlapScale",difi1[0][1]])
			json_a.seek(0)
			difi2=returnJsonTwo(numlinesa,a_data,"Anagrams", "participant.code", player, "player.distanceScale_after","player.overlapScale_after")
			if len(difi2)>0:
				beginparvalues2.append(["difi2distanceScale",difi2[0][0]])
				beginparvalues2.append(["difi2overlapScale",difi2[0][1]])
			json_pgoods.seek(0)
			difi3=returnJsonFour(numlinespg,pg_data,"PublicGoods", "participant.code", player, "player.contribution","player.profit","player.distanceScale","player.overlapScale")
			if len(difi3)>0:
				endparvalues2.append(["contribution",difi3[0][0]])
				endparvalues2.append(["profit",difi3[0][1]])
				endparvalues2.append(["difi3distanceScale",difi3[0][2]])
				endparvalues2.append(["difi3overlapScale",difi3[0][3]])
			alldataplayerjson.append([phaseid1,player,neighborsvalues,beginparvalues1,endparvalues1])
			alldataplayerjson.append([phaseid2,player,[""],beginparvalues2,endparvalues2])
			actionplayer=sorted(actionplayer, key=lambda x: float(x[0]))
			actioncount=0
			for actionitem in actionplayer:
				actioncount=actioncount+1
				if len(actionitem[1])==1:
					json_lt.seek(0)
					events=returnJsonTwoTwo(numlineslt,lt_data,"LetterTransactions", "player__participant__code","timestamp", player,actionitem[0], "letter__player__participant__code","approve_time")
					actionsplayer.append([player,events[0][0],"requestsent",actioncount,float(actionitem[0]),actionitem[1]])
					if events[0][1]!="":
						actionsplayer.append([events[0][0],player,"replysent",actioncount,float(events[0][1]),actionitem[1]])
				else:
					actionsplayer.append([player,"","word",actioncount,float(actionitem[0]),actionitem[1]])
		json_ne.seek(0)
		k=getNumberNeighbors(numlinesne,ne_data,"Neighbors","player__participant__code",activeplayers[0])
		if float(row[3])>0:
			nexperiment=nexperiment+1
			alldataexperimentjson.append([int(nexperiment),2,int(float(row[1])),k,row[2],row[3],activeplayers])
			alldataphasejson.append([str(phaseid1),"anagrams",int(nexperiment),1,int(begin),int(duration),k,int(float(row[1]))])
			alldataphasejson.append([str(phaseid2),"publicgoods",int(nexperiment),2,int(begin2),int(duration2),0,int(float(row[1]))])
			alldataactionjson.append([phaseid1,int(float(row[1])),k,actionsplayer])
	experimentjsondata=[{"experimentid":int(row[0]),"p":int(row[1]),"n":int(row[2]),"starttime":str(row[4]),"duration":float(row[5]),"activeplayers":[{"player":str(row2)} for row2 in row[6]]} for row in alldataexperimentjson]
	json.dump(experimentjsondata,experimentjson,indent=2)
	json.dump(experimentjsondata,experimentjson2,indent=2)
	phasejsondata=[{"phaseid":str(row[0]),"phasedescriptionid":str(row[1]),"experimentid":int(row[2]),"phaseorder":int(row[3]),"begin":float(row[4]),"duration":int(row[5]),"d":int(row[6]),"n":int(row[7])} for row in alldataphasejson]
	json.dump(phasejsondata,phasejson,indent=2)
	json.dump(phasejsondata,phasejson2,indent=2)
	phasedescjsondata=[{"phaseid":str(row[0]),"beginparameters":[{"parameter":str(row2)} for row2 in row[1]],"endparameters":[{"parameter":str(row3)} for row3 in row[2]],"actions":[{"action":str(row4)} for row4 in row[3]],"synchronousactions":[{"actionrequest":str(row5[0]),"actionreply":str(row5[1])} for row5 in row[4]],"features":[{"feature":str(row6)} for row6 in row[5]]} for row in alldataphasedescjson]
	json.dump(phasedescjsondata,phasedescjson,indent=2)
	json.dump(phasedescjsondata,phasedescjson2,indent=2)
	actionjsondata=[{"phaseid":str(row[0]),"n":int(row[1]),"d":int(row[2]),"actionlist":[{"player1":str(row2[0]),"player2":str(row2[1]),"actionid":str(row2[2]),"playerActionSeqid":int(row2[3]),"timestamp":float(row2[4]),"payload":str(row2[5])} for row2 in row[3]]} for row in alldataactionjson]
	json.dump(actionjsondata,actionjson,indent=2)
	json.dump(actionjsondata,actionjson2,indent=2)
	playerjsondata=[{"phaseid":str(row[0]),"playerid":str(row[1]),"neighbors":[{"neighbor":str(row2)} for row2 in row[2]],"beginparameters":[{"parameter":str(row3[0]),"value":str(row3[1])} for row3 in row[3]],"endparameters":[{"parameter":str(row4[0]),"value":str(row4[1])} for row4 in row[4]]} for row in alldataplayerjson]
	json.dump(playerjsondata,playerjson,indent=2)
	json.dump(playerjsondata,playerjson2,indent=2)
	endTime=datetime.now()
	print (" elapsed time (seconds): ",endTime-startTime)
	print (" -- h1 --")
	print (" -- good termination --")
	return	

## --------------------------
## Execution starts.
if __name__ == '__main__':
    if (len(sys.argv) != 11):
    	print ("  Error.  Incorrect usage.")
    	print ("  usage: exec infile outfile.")
    	print ("  Halt.")
    	quit()
    	
    inputpath=sys.argv[1]
    anagrams=sys.argv[2]
    CompletedSessionSummary=sys.argv[3]
    InstructionsAnagrams=sys.argv[4]
    LetterTransactions=sys.argv[5]
    Neighbors=sys.argv[6]
    PublicGoods=sys.argv[7]
    TeamWords=sys.argv[8]
    TimeSpent=sys.argv[9]
    UserLetters=sys.argv[10]
    main(inputpath,anagrams,CompletedSessionSummary,InstructionsAnagrams,LetterTransactions,Neighbors,PublicGoods,TeamWords,TimeSpent,UserLetters)
    print (" -- good termination from main --")
