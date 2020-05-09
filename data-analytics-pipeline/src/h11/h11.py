##method 1 for letter request, delta and rank
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

def is_allowed_specific_char(letters,word):
      charRe = re.compile(r'[^%s]' % letters)
      string = charRe.search(word)
      return not bool(string)
      
## ------------------------------
def filescsv(n,d,numseconds,numlines,phases,csvfileall,windowsize,all_words_file):
	nd="n"+str(n)+"d"+str(d)
	if not os.path.exists(os.getcwd()+'/data-analytics-pipeline/test/results/h11/output/'+nd):
		os.makedirs(os.getcwd()+'/data-analytics-pipeline/test/results/h11/output/'+nd)

	csvfile = open(os.getcwd()+'/data-analytics-pipeline/test/results/h11/output/'+nd+'/tsData.csv', 'w')
	csvfile.write('session,player,n,d,letters,neighborsLetters,time,requestsSent,repliesReceived,requestsReceived,repliesSent,words,lastWord,wih,delta\n')
	
	csvfileheat = open(os.getcwd()+'/data-analytics-pipeline/test/results/h11/output/'+nd+'HeatMap.csv', 'w')
	csvfileheat.write('day\thour\tvalue\n')
	
	makepath=os.getcwd()+'/data-analytics-pipeline/src/h11'
	exepath='cd '+makepath+';'
	subprocess.Popen(["make"], cwd=makepath)
	
	countplayer=0
	for i in range(numlines):
		phase=phases[i]["phaseid"]
		players=phases[i]["players"]
		numplayers=len(players)
		for ii in range(numplayers):
			countplayer=countplayer+1
			playerid=players[ii]["playerid"]
			initialletters=players[ii]["initialLetters"]
			neighbors=players[ii]["neighborsLetters"].lower()
			neighborslist=list(neighbors)
			neighborsLetters=[]
			#for let in neighborslist:
			#	if let not in neighborsLetters:
			#		neighborsLetters.append(let)
			neighborsLetters=neighborslist
			numneighbors=int(d)
			countletterR=0
			
			numanalysis=int(numneighbors*3*0.25)
			timeline=players[ii]["timeline"]
			numtimeline=len(timeline)
			countbin=0
			lastword=0
			w1=[]
			w2=[]
			wih=[]
			allwords=[]
			
			allLettersRec= initialletters.lower().split("-")
			allLettersRecS="".join(str(x.lower()) for x in allLettersRec)
			neighborsLettersS="".join(str(x.lower()) for x in neighborsLetters)
			w2S=''
			wihS=''
			delta=''
			rankingc=''
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
							
					if repliesReceived!='':
						if '-' in repliesReceived:
							listrep=repliesReceived.split('-')
							for rep in listrep:
								allLettersRec.append(rep)
								#if rep in neighborsLetters:
								#	neighborsLetters.remove(rep)
						else:
							allLettersRec.append(repliesReceived)
						#print(allLettersRec)
						#print(all_words_file[0])
						allLettersRecS="".join(str(x) for x in allLettersRec)
						allLettersRecS=allLettersRecS.lower()
						
						
					if requestsSent!='':
						letterw=[]
						countletterR=countletterR+1
						if requestsSent in neighborsLetters:
							neighborsLetters.remove(requestsSent)
						neighborsLettersS="".join(str(x) for x in neighborsLetters)
						neighborsLettersS=neighborsLettersS.lower()
						wihS=''
						if countletterR<=numanalysis:
							wih=[]
							wihC=[]
							#print(neighborsLetters)
							for rowl in neighborsLetters:
								wihl=[]
								#print("allLettersRec")
								#print(allLettersRec)
								allLettersRecL=list(allLettersRec)
								allLettersRecL.append(rowl)
								#print(allLettersRecL)
								allLettersRecLS="".join(str(x) for x in allLettersRecL)
								for rowword in all_words_file:
									wordfile=rowword.strip('\n')
									if wordfile.isalpha()==True and allLettersRecLS.isalpha()==True and len(wordfile)>=3 and wordfile not in wihl:
										#print(allLettersRecS.lower(),wordfile)
										if is_allowed_specific_char(allLettersRecLS,wordfile)==True:				
											wihl.append(wordfile)
								letterw.append([rowl,len(wihl)])
								#if playerid=='6ccyzsaq':
								#	print(rowl)
								#	print(wihl)
								#	print(neighborsLetters)
								
							allLettersRecL=list(allLettersRec)
							allLettersRecL.append(requestsSent)
							allLettersRecLS="".join(str(x) for x in allLettersRecL)
							for rowword in all_words_file:
								wordfile=rowword.strip('\n')
								if wordfile.isalpha()==True and allLettersRecLS.isalpha()==True and len(wordfile)>=3 and wordfile not in wihC:
									#print(allLettersRecS.lower(),wordfile)
									if is_allowed_specific_char(allLettersRecLS,wordfile)==True:				
										wihC.append(wordfile)
							letterw.append([requestsSent,len(wihC)])
							#if playerid=='6ccyzsaq':
							#	print(allLettersRecLS)
							#	print(wihC)
							#	print(len(wihC))
							
							for rowword in all_words_file:
								wordfile=rowword.strip('\n')
								if wordfile.isalpha()==True and allLettersRecS.isalpha()==True and len(wordfile)>=3 and wordfile not in wih:
									#print(allLettersRecS.lower(),wordfile)
									if is_allowed_specific_char(allLettersRecS,wordfile)==True:				
										wih.append(wordfile)
							wihS = "-".join(str(valueword) for valueword in wih)
							df = pd.DataFrame(letterw,columns=['letter','wihl'])
							df['rank']=df['wihl'].rank(method='average',ascending=0).astype(int)
							#df = df.values
							optimall=df.at[df['rank'].idxmin(),'wihl']
							rankingc=df.loc[df['letter'] == requestsSent, 'rank'].iloc[0]
							#if playerid=='6ccyzsaq':
							#	print(df)
							#	print(optimall)
							#	print(rankingc)
							delta=0
							if len(wih)>0:
								delta=abs((abs(optimall-len(wih))/len(wih))-(abs(len(wihC)-len(wih))/len(wih)))
							#print(wih)
							#print("delta")
							#print(delta)
						#if playerid=='6ccyzsaq':
						#	print(requestsSent)	
						#	print(wih)
						#	print(countletterR)
						#	print(wihS)
					lastwordS=''
					if words!='' and lastword!=0:
						lastwordS=lastword
					
					csvfile.write(str(phase)+','+str(playerid)+','+str(n)+','+str(d)+','+str(allLettersRecS)+','+str(neighborsLettersS)+','+str(iii)+','+str(requestsSent)+','+str(repliesReceived)+','+str(requestsReceived)+','+str(repliesSent)+','+str(words)+','+str(lastwordS)+','+str(wihS)+','+str(delta)+','+str(rankingc)+'\n')
					csvfileall.write(str(phase)+','+str(playerid)+','+str(n)+','+str(d)+','+str(allLettersRecS)+','+str(neighborsLettersS)+','+str(iii)+','+str(requestsSent)+','+str(repliesReceived)+','+str(requestsReceived)+','+str(repliesSent)+','+str(words)+','+str(lastwordS)+','+str(wihS)+','+str(delta)+','+str(rankingc)+'\n')
					countrequestsSent=0
					if words!='' and '-' not in words:
						lastword=words
					w2S=''
					wihS=''
					delta=''
					rankingc=''
					if '-' in requestsSent:
						listrequestsSent=requestsSent.split('-')
						countrequestsSent=len(listrequestsSent)
					else:
						if requestsSent!='':
							countrequestsSent=1
					csvfileheat.write(str(countplayer)+'\t'+str(countbin)+'\t'+str(countrequestsSent)+'\n')
	
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
    if not os.path.exists(os.getcwd()+'/data-analytics-pipeline/test/results/h11/output/all'):
    	os.makedirs(os.getcwd()+'/data-analytics-pipeline/test/results/h11/output/all')
    	
    csvfileall = open(os.getcwd()+'/data-analytics-pipeline/test/results/h11/output/all/tsData.csv', 'w')
    csvfileall.write('session,player,n,d,letters,neighborLetters,time,requestsSent,repliesReceived,requestsReceived,repliesSent,words,lastWord,wih,delta,rankingChosen\n')
    
    #with open(os.getcwd()+'/data-analytics-pipeline/src/h11/all_words.txt', 'r') as f:
    #with open(os.getcwd()+'/data-analytics-pipeline/src/h11/3k.txt', 'r') as f:
    #with open(os.getcwd()+'/data-analytics-pipeline/src/h11/20k.txt', 'r') as f:
    #with open(os.getcwd()+'/data-analytics-pipeline/src/h11/google-10000-english-no-swears.txt', 'r') as f:
    #with open(os.getcwd()+'/data-analytics-pipeline/src/h11/google-10000-english-usa.txt', 'r') as f:
    #with open(os.getcwd()+'/data-analytics-pipeline/src/h11/5k1k.txt', 'r') as f:
    with open(os.getcwd()+'/data-analytics-pipeline/src/h11/5k.txt', 'r') as f:
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

    		filescsv(n,d,numseconds,len(phases),phases,csvfileall,windowsize,all_words_file)
    print (" -- h11 --")
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
    