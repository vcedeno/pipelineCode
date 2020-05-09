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

def is_allowed_specific_char(letters,word):
      charRe = re.compile(r'[^%s]' % letters)
      string = charRe.search(word)
      return not bool(string)
      
## ------------------------------
def filescsv(n,d,numseconds,numlines,phases,csvfileall,windowsize,all_words_file):
	nd="n"+str(n)+"d"+str(d)
	if not os.path.exists(os.getcwd()+'/data-analytics-pipeline/test/results/h8/output/'+nd):
		os.makedirs(os.getcwd()+'/data-analytics-pipeline/test/results/h8/output/'+nd)

	csvfile = open(os.getcwd()+'/data-analytics-pipeline/test/results/h8/output/'+nd+'/tsData.csv', 'w')
	csvfile.write('session,player,type,letters,time,requestsSent,repliesReceived,requestsReceived,repliesSent,words,LevenshteinDistance,minLevenshteinDistance\n')
	
	csvfileheat = open(os.getcwd()+'/data-analytics-pipeline/test/results/h8/output/'+nd+'HeatMap.csv', 'w')
	csvfileheat.write('day\thour\tvalue\n')
	
	makepath=os.getcwd()+'/data-analytics-pipeline/src/h8'
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
			timeline=players[ii]["timeline"]
			numtimeline=len(timeline)
			countbin=0
			lastword=0
			w1=[]
			w2=[]
			allwords=[]
			allLettersRec= initialletters.split("-")
			for iii in range(numtimeline):
				if iii<(numseconds):
					countbin=countbin+1
					requestsSent=timeline[iii]["requestsSent"]
					repliesReceived=timeline[iii]["repliesReceived"]
					requestsReceived=timeline[iii]["requestsReceived"]
					repliesSent=timeline[iii]["repliesSent"]
					words=timeline[iii]["words"].lower()
					
					if words!='':
						allwords.append(words)
						
					if repliesReceived!='' or iii==0:
						w1=[]
						if iii>0:
							allLettersRec.append(repliesReceived)
						#print(allLettersRec)
						#print(all_words_file[0])
						allLettersRecS="".join(str(x) for x in allLettersRec)
						allLettersRecS=allLettersRecS.lower()
						for rowword in all_words_file:
							wordfile=rowword.lower().strip('\n')
							if wordfile.isalpha()==True and allLettersRecS.isalpha()==True and len(wordfile)>=3:
								#print(allLettersRecS.lower(),wordfile)
								if is_allowed_specific_char(allLettersRecS.lower(),wordfile)==True:				
									w1.append(wordfile)
						w2=w1
						#if len(w1)>0:
							#print(w1)
						for rowword in allwords:
							if rowword in w2:
								w2.remove(rowword.lower())
					
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
								if len(w2)>0:
									minld=9999
									i=0
									while minld>1 and i<len(w2):
										arguments= ' '+str(w2[i]) + ' '+str(wordrow)
										ldvalue=subprocess.call (exepath+' ./main'+arguments,shell=True)
										if ldvalue<minld:
											minld=ldvalue
										i=i+1
									ldlistMin.append(minld)
								else:
									print(w2)
									print(allLettersRec)
								
								lastword=wordrow
							ld = "-".join(str(valueword) for valueword in ldlist)
							minld = "-".join(str(valueword) for valueword in ldlistMin)
						else:
							arguments= ' '+str(lastword) + ' '+str(words)
							ld=subprocess.call (exepath+' ./main'+arguments,shell=True)
							if len(w2)>0:
								minld=9999
								i=0
								while minld>1 and i<len(w2):
									arguments= ' '+str(w2[i]) + ' '+str(words)
									ldvalue=subprocess.call (exepath+' ./main'+arguments,shell=True)
									if ldvalue<minld:
										minld=ldvalue
									i=i+1
								
							
							#lastword=words
						#if playerid=='p4f3glnm':
							#print('ld:'+str(ld))
					if words!='' and '-' not in words:
						lastword=words
					csvfile.write(str(phase)+','+str(playerid)+','+str(nd)+','+str(initialletters)+','+str(iii)+','+str(requestsSent)+','+str(repliesReceived)+','+str(requestsReceived)+','+str(repliesSent)+','+str(words)+','+str(ld)+','+str(minld)+'\n')
					csvfileall.write(str(phase)+','+str(playerid)+','+str(nd)+','+str(initialletters)+','+str(iii)+','+str(requestsSent)+','+str(repliesReceived)+','+str(requestsReceived)+','+str(repliesSent)+','+str(words)+','+str(ld)+','+str(minld)+'\n')
					countrequestsSent=0
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
    if not os.path.exists(os.getcwd()+'/data-analytics-pipeline/test/results/h8/output/all'):
    	os.makedirs(os.getcwd()+'/data-analytics-pipeline/test/results/h8/output/all')
    	
    csvfileall = open(os.getcwd()+'/data-analytics-pipeline/test/results/h8/output/all/tsData.csv', 'w')
    csvfileall.write('session,player,type,letters,time,requestsSent,repliesReceived,requestsReceived,repliesSent,words,LevenshteinDistance,minLevenshteinDistance\n')
    
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

    		filescsv(n,d,numseconds,len(phases),phases,csvfileall,windowsize,all_words_file)
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
    