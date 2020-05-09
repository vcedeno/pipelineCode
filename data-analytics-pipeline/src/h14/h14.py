##Letter reply analysis with time series and accumulated values
import sys
import os
import csv
import subprocess
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
import re
import pandas as pd

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
    
    
def is_allowed_specific_char(letters,word):
      charRe = re.compile(r'[^%s]' % letters)
      string = charRe.search(word)
      return not bool(string)

def count_letter(word, letter):
    count = 0
    for c in word:
        if c == letter:
            count += 1
    return count  
  
## ------------------------------
def filescsv(n,d,numseconds,numlines,phases,csvfileall,windowsize,csvfileallP):
	nd="n"+str(n)+"d"+str(d)
	if not os.path.exists(os.getcwd()+'/data-analytics-pipeline/test/results/h14/output/'+nd):
		os.makedirs(os.getcwd()+'/data-analytics-pipeline/test/results/h14/output/'+nd)

	csvfile = open(os.getcwd()+'/data-analytics-pipeline/test/results/h14/output/'+nd+'/tsData.csv', 'w')
	csvfile.write('session,player,n,d,letters,neighborsLetters,time,requestsSent,repliesReceived,requestsReceived,repliesSent,words,countBuffer,numAllReplies,secondsSpan\n')
	
	
	countplayer=0
	for i in range(numlines):
		phase=phases[i]["phaseid"]
		players=phases[i]["players"]
		numplayers=len(players)
		
		for ii in range(numplayers):
			countplayer=countplayer+1
			allLettersReqCount=0
			allLettersRecCount=0
			playerid=players[ii]["playerid"]
			initialletters=players[ii]["initialLetters"]
			neighbors=players[ii]["neighborsLetters"].lower()
			neighborslist=list(neighbors)
			neighborsLetters=[]
			#for let in neighborslist:
			#	if let not in neighborsLetters:
			#		neighborsLetters.append(let)
			neighborsLetters=neighborslist
			initialneighborsletters=len(neighbors)
			numneighbors=int(d)
			countletterR=0
			
			numanalysis=int(numneighbors*3*0.25)
			timeline=players[ii]["timeline"]
			numtimeline=len(timeline)
			countbin=0
			lastword=0
			bufferRec=[]
			allwords=[]
			
			initiallettersString=initialletters.split("-")
			initiallettersString = "".join(str(valueword) for valueword in initiallettersString)
			allLettersRec= initialletters.split("-")
			
			allLettersRec= initialletters.lower().split("-")
			allLettersRecS="".join(str(x.lower()) for x in allLettersRec)
			neighborsLettersS="".join(str(x.lower()) for x in neighborsLetters)
			
			delta=''
			localrank=''
			countBufferS=''
			allreplies=''
			lastaction=''
			timeend=''
			
			for iii in range(numtimeline):
				if iii<(numseconds):
					countbin=countbin+1
					requestsSent=timeline[iii]["requestsSent"].lower()
					repliesReceived=timeline[iii]["repliesReceived"].lower()
					requestsReceived=timeline[iii]["requestsReceived"].lower()
					repliesSent=timeline[iii]["repliesSent"].lower()
					words=''
					words=timeline[iii]["words"].lower()
					
					if words!='':
						if lastaction=='repliesSent':
							allreplies=onlyreplies
							countBufferS=str(countBuffer)
							timeend=iii-timebegin
						
						lastaction='word'
						if '-' in words:
							listwords=words.split('-')
							for wordrow in listwords:
								allwords.append(wordrow)
								#if wordrow in w2:
								#	w2.remove(wordrow)
						else:
							allwords.append(words)
							#if words in w2:
							#	w2.remove(words)
							
					if requestsReceived!='':
						if lastaction=='repliesSent':
							allreplies=onlyreplies
							countBufferS=str(countBuffer)
							timeend=iii-timebegin
						lastaction='requestsReceived'
						if '-' in requestsReceived:
							listrep=requestsReceived.split('-')
							for rep in listrep:
								bufferRec.append(rep)
								#if rep in neighborsLetters:
								#	neighborsLetters.remove(rep)
						else:
							bufferRec.append(requestsReceived)
							
					
					if repliesSent!='':							
						if lastaction!='repliesSent':
							onlyreplies=1
							countBuffer=len(bufferRec)
							timebegin=iii
						if lastaction=='repliesSent':
							onlyreplies=onlyreplies+1
						
						
						if '-' in repliesSent:
							listrep=repliesSent.split('-')
							for rep in listrep:
								bufferRec.remove(rep)
								#if rep in neighborsLetters:
								#	neighborsLetters.remove(rep)
						else:
							bufferRec.remove(repliesSent)
							
						lastaction='repliesSent'
								
					if repliesReceived!='':
						if '-' in repliesReceived:
							listrep=repliesReceived.split('-')
							for rep in listrep:
								allLettersRec.append(rep)
								allLettersRecCount=allLettersRecCount+1
								#if rep in neighborsLetters:
								#	neighborsLetters.remove(rep)
						else:
							allLettersRec.append(repliesReceived)
							allLettersRecCount=allLettersRecCount+1
						#print(allLettersRec)
						
						allLettersRecS="".join(str(x) for x in allLettersRec)
						allLettersRecS=allLettersRecS.lower()
						
					if requestsSent!='':
						allLettersReqCount=allLettersReqCount+1
						if lastaction=='repliesSent':
							allreplies=onlyreplies
							countBufferS=str(countBuffer)
							timeend=iii-timebegin
						
						lastaction='requestsSent'
						countletterR=countletterR+1
	
					lastwordS=''
					if words!='' and lastword!=0:
						lastwordS=lastword
					
					neighborsLettersS="".join(str(x) for x in neighborsLetters)
					neighborsLettersS=neighborsLettersS.lower()
						
					#allLettersRecCount=len(allLettersRec)
					csvfile.write(str(phase)+','+str(playerid)+','+str(n)+','+str(d)+','+str(allLettersRecS)+','+str(neighborsLettersS)+','+str(iii)+','+str(requestsSent)+','+str(repliesReceived)+','+str(requestsReceived)+','+str(repliesSent)+','+str(words)+','+str(countBufferS)+','+str(allreplies)+','+str(timeend)+'\n')
					csvfileall.write(str(phase)+','+str(playerid)+','+str(n)+','+str(d)+','+str(allLettersRecS)+','+str(neighborsLettersS)+','+str(iii)+','+str(requestsSent)+','+str(repliesReceived)+','+str(requestsReceived)+','+str(repliesSent)+','+str(words)+','+str(countBufferS)+','+str(allreplies)+','+str(timeend)+'\n')
					countrequestsSent=0
					if words!='' and '-' not in words:
						lastword=words
		
					delta=''
					localrank=''
					countBufferS=''
					allreplies=''
					timeend=''
					if '-' in requestsSent:
						listrequestsSent=requestsSent.split('-')
						countrequestsSent=len(listrequestsSent)
					else:
						if requestsSent!='':
							countrequestsSent=1
			
			initiallettersScrabble=scrabble_score(initiallettersString.lower())
			numwords=len(allwords)
			fracReplies=0
			if allLettersRecCount>0:
				fracReplies=allLettersRecCount/allLettersReqCount
			csvfileallP.write(str(phase)+','+str(playerid)+','+str(n)+','+str(d)+','+str(numwords)+','+str(initiallettersString)+','+str(initiallettersScrabble)+','+str(allLettersReqCount)+','+str(allLettersRecCount)+','+str(fracReplies)+'\n')
		
					
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
    if not os.path.exists(os.getcwd()+'/data-analytics-pipeline/test/results/h14/output/all'):
    	os.makedirs(os.getcwd()+'/data-analytics-pipeline/test/results/h14/output/all')
    	
    csvfileall = open(os.getcwd()+'/data-analytics-pipeline/test/results/h14/output/all/tsData.csv', 'w')
    csvfileall.write('session,player,n,d,letters,neighborLetters,time,requestsSent,repliesReceived,requestsReceived,repliesSent,words,countBuffer,numAllReplies,secondsSpan\n')
    csvfileallP = open(os.getcwd()+'/data-analytics-pipeline/test/results/h14/output/all/tsDataParameters.csv', 'w')
    csvfileallP.write('session,player,n,d,numWords,initialLetters,iLScrabbleSco,numRequests,numReplies,fracReplies\n')
    
    #with open(os.getcwd()+'/data-analytics-pipeline/src/h14/all_words.txt', 'r') as f:
    #with open(os.getcwd()+'/data-analytics-pipeline/src/h14/3k.txt', 'r') as f:
    #with open(os.getcwd()+'/data-analytics-pipeline/src/h14/20k.txt', 'r') as f:
    #with open(os.getcwd()+'/data-analytics-pipeline/src/h14/google-10000-english-no-swears.txt', 'r') as f:
    #with open(os.getcwd()+'/data-analytics-pipeline/src/h14/google-10000-english-usa.txt', 'r') as f:
    #with open(os.getcwd()+'/data-analytics-pipeline/src/h14/5k1k.txt', 'r') as f:
    #with open(os.getcwd()+'/data-analytics-pipeline/src/h14/5k.txt', 'r') as f:
    #	all_words_file = f.readlines()
    
    
    for i in range(numlines):
    	actionrequest=json_data[i]["features"]
    	for index,actions in enumerate(actionrequest):
    		n=actionrequest[index]["n"]
    		d=actionrequest[index]["d"]
    		windowsize=actionrequest[index]["windowsize"]
    		numseconds=actionrequest[index]["numseconds"]
    		
    		#if not os.path.exists(os.getcwd()+'/data-analytics-pipeline/test/results/h7/output/'+action):
    		#	os.makedirs(os.getcwd()+'/data-analytics-pipeline/test/results/h7/output/'+action)
    		phases=actionrequest[index]["phases"]

    		filescsv(n,d,numseconds,len(phases),phases,csvfileall,windowsize,csvfileallP)
    print (" -- h14 --")
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
    