##Time series data by players, with letters in hand
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
from collections import Counter
from math import log

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
      
## ------------------------------
def filescsv(n,d,numseconds,numlines,phases,csvfileall,windowsize,all_words_file,csvfileallP,csvfileallW):
	nd="n"+str(n)+"d"+str(d)
	if not os.path.exists(os.getcwd()+'/data-analytics-pipeline/test/results/h8/output/'+nd):
		os.makedirs(os.getcwd()+'/data-analytics-pipeline/test/results/h8/output/'+nd)

	csvfile = open(os.getcwd()+'/data-analytics-pipeline/test/results/h8/output/'+nd+'/tsData.csv', 'w')
	csvfile.write('session,player,type,letters,time,requestsSent,repliesReceived,requestsReceived,repliesSent,words,LevenshteinDistance\n')
	
	csvfileheat = open(os.getcwd()+'/data-analytics-pipeline/test/results/h8/output/'+nd+'HeatMap.csv', 'w')
	csvfileheat.write('day\thour\tvalue\n')
	
	makepath=os.getcwd()+'/data-analytics-pipeline/src/h8'
	exepath='cd '+makepath+';'
	subprocess.Popen(["make"], cwd=makepath)
	
	countplayer=0
	allwordsGameList=[]
	uniqueWords=[]
	for i in range(numlines):
		phase=phases[i]["phaseid"]
		players=phases[i]["players"]
		numplayers=len(players)
		allwordsGame=[]
		for ii in range(numplayers):
			countplayer=countplayer+1
			playerid=players[ii]["playerid"]
			initialletters=players[ii]["initialLetters"]
			timeline=players[ii]["timeline"]
			numtimeline=len(timeline)
			countbin=0
			lastword=0
			w1=[]
			w2=[]
			allwords=[]
			initiallettersString=initialletters.split("-")
			initiallettersString = "".join(str(valueword) for valueword in initiallettersString)
			allLettersRec= initialletters.split("-")
			iScrabble1=0
			iScrabble2=0
			iScrabble3=0
			iScrabble4=0
			iScrabble5=0
			for iii in range(numtimeline):
				if iii<(numseconds):
					countbin=countbin+1
					requestsSent=timeline[iii]["requestsSent"]
					repliesReceived=timeline[iii]["repliesReceived"]
					requestsReceived=timeline[iii]["requestsReceived"]
					repliesSent=timeline[iii]["repliesSent"]
					words=timeline[iii]["words"].lower()
					
					if words!='':
						if '-' in words:
							listwords=words.split('-')
							for wordrow in listwords:
								allwords.append(wordrow)
								allwordsGame.append(wordrow)
								if [i,wordrow] not in uniqueWords:
									uniqueWords.append([i,wordrow])
						else:
							allwords.append(words)
							allwordsGame.append(words)
							if [i,words] not in uniqueWords:
								uniqueWords.append([i,words])
						
					if repliesReceived!='':
						if '-' in repliesReceived:
							listrep=repliesReceived.split('-')
							for rep in listrep:
								allLettersRec.append(rep)
						else:
							allLettersRec.append(repliesReceived)
					
					
					ld=''
					minld=''
					
					if windowsize==1 and words!='' and lastword!=0:
						#if playerid=='p4f3glnm':
							#print('lastword:'+lastword)
							#print('newword:'+words)
						if '-' in words:
							listwords=words.split('-')
							ldlist=[]
							ldlistMin=[]
							for wordrow in listwords:
								arguments= ' '+str(lastword) + ' '+str(wordrow)
								ldlist.append(subprocess.call (exepath+' ./main'+arguments,shell=True))
								lastword=wordrow
							ld = "-".join(str(valueword) for valueword in ldlist)
						else:
							arguments= ' '+str(lastword) + ' '+str(words)
							ld=subprocess.call (exepath+' ./main'+arguments,shell=True)
								
							
							#lastword=words
						#if playerid=='p4f3glnm':
							#print('ld:'+str(ld))
					if words!='' and '-' not in words:
						lastword=words
					allLettersRecS="".join(str(valueword) for valueword in allLettersRec)
					
					if iii==59:
						iScrabble1=scrabble_score(allLettersRecS.lower())
					if iii==119:
						iScrabble2=scrabble_score(allLettersRecS.lower())
					if iii==179:
						iScrabble3=scrabble_score(allLettersRecS.lower())
					if iii==239:
						iScrabble4=scrabble_score(allLettersRecS.lower())
					if iii==299:
						iScrabble5=scrabble_score(allLettersRecS.lower())
					csvfile.write(str(phase)+','+str(playerid)+','+str(nd)+','+str(allLettersRecS)+','+str(iii)+','+str(requestsSent)+','+str(repliesReceived)+','+str(requestsReceived)+','+str(repliesSent)+','+str(words)+','+str(ld)+'\n')
					csvfileall.write(str(phase)+','+str(playerid)+','+str(nd)+','+str(allLettersRecS)+','+str(iii)+','+str(requestsSent)+','+str(repliesReceived)+','+str(requestsReceived)+','+str(repliesSent)+','+str(words)+','+str(ld)+'\n')
					
					countrequestsSent=0
					if '-' in requestsSent:
						listrequestsSent=requestsSent.split('-')
						countrequestsSent=len(listrequestsSent)
					else:
						if requestsSent!='':
							countrequestsSent=1
					csvfileheat.write(str(countplayer)+'\t'+str(countbin)+'\t'+str(countrequestsSent)+'\n')
			countOwnWords=0
			for rowword in allwords:
				wordfile=rowword.lower()
				if is_allowed_specific_char(initiallettersString.lower(),wordfile)==True:
					countOwnWords=countOwnWords+1	
			numwords=len(allwords)
			fracWords=0
			initiallettersScrabble=scrabble_score(initiallettersString.lower())
			if numwords>0:
				fracWords=float(countOwnWords/numwords)
			csvfileallP.write(str(phase)+','+str(playerid)+','+str(n)+','+str(d)+','+str(numwords)+','+str(fracWords)+','+str(initiallettersString)+','+str(initiallettersScrabble)+','+str(iScrabble1)+','+str(iScrabble2)+','+str(iScrabble3)+','+str(iScrabble4)+','+str(iScrabble5)+'\n')
		allwordsGameList.append([i,allwordsGame])
	for rowcount in allwordsGameList:
		countW=Counter(rowcount[1])
		numwordsGame=len(rowcount[1])
		for rowword in countW:
			key=rowword
			value=countW[key]
			countword=0
			for row in uniqueWords:
				if str(key)==str(row[1]):
					countword=countword+1
			tf=0
			if numwordsGame!=0:
				tf=int(value)/int(numwordsGame)
			idf=0
			if countword!=0:
				idf=int(numlines)/int(countword)
				if idf!=0:
					idf=log(idf,10)
			tfidf=tf*idf
			csvfileallW.write(str(n)+','+str(d)+','+str(key)+','+str(value)+','+str(numwordsGame)+','+str(tf)+','+str(numlines)+','+str(countword)+','+str(idf)+','+str(tfidf)+'\n')
								
				
	
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
    if not os.path.exists(os.getcwd()+'/data-analytics-pipeline/test/results/h8/output/all'):
    	os.makedirs(os.getcwd()+'/data-analytics-pipeline/test/results/h8/output/all')
    
    csvfileallW = open(os.getcwd()+'/data-analytics-pipeline/test/results/h8/output/all/tsDataWords.csv', 'w')	
    csvfileallP = open(os.getcwd()+'/data-analytics-pipeline/test/results/h8/output/all/tsDataParameters.csv', 'w')
    csvfileall = open(os.getcwd()+'/data-analytics-pipeline/test/results/h8/output/all/tsData.csv', 'w')
    csvfileall.write('session,player,type,letters,time,requestsSent,repliesReceived,requestsReceived,repliesSent,words,LevenshteinDistance\n')
    csvfileallP.write('session,player,neighbors,n,numWords,fracWordsOwnL,initialLetters,iLScrabbleSco,iLScrabbleSco1,iLScrabbleSco2,iLScrabbleSco3,iLScrabbleSco4,iLScrabbleSco5\n')
    csvfileallW.write('n,d,word,numAppears,numWords,tf,numGames,numGamesWord,idf,tfidf\n')
    with open(os.getcwd()+'/data-analytics-pipeline/src/h8/all_words.txt', 'r') as f:
    	all_words_file = f.readlines()
    
    print("num words:",len(all_words_file))
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

    		filescsv(n,d,numseconds,len(phases),phases,csvfileall,windowsize,all_words_file,csvfileallP,csvfileallW)
    print (" -- h8 --")
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
    