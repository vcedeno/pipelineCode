##word local rank
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
def filescsv(n,d,numseconds,numlines,phases,csvfileall,windowsize,all_words_file,wordranklist):
	nd="n"+str(n)+"d"+str(d)
	if not os.path.exists(os.getcwd()+'/data-analytics-pipeline/test/results/h13/output/'+nd):
		os.makedirs(os.getcwd()+'/data-analytics-pipeline/test/results/h13/output/'+nd)

	csvfile = open(os.getcwd()+'/data-analytics-pipeline/test/results/h13/output/'+nd+'/tsData.csv', 'w')
	csvfile.write('session,player,n,d,letters,time,requestsSent,repliesReceived,requestsReceived,repliesSent,words,lastWord,LevenshteinDistance,minLevenshteinDistance,w2,wordlocalrank,wordrank,wordlocalrankp\n')
	
	csvfileheat = open(os.getcwd()+'/data-analytics-pipeline/test/results/h13/output/'+nd+'HeatMap.csv', 'w')
	csvfileheat.write('day\thour\tvalue\n')
	
	makepath=os.getcwd()+'/data-analytics-pipeline/src/h13'
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
			w2S=''
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
								if wordrow in w2:
									w2.remove(wordrow)
						else:
							allwords.append(words)
							if words in w2:
								w2.remove(words)
						
						
					if repliesReceived!='' or iii==0:
						
						w1=[]
						if iii>0:
							if '-' in repliesReceived:
								listrep=repliesReceived.split('-')
								for rep in listrep:
									allLettersRec.append(rep)
							else:
								allLettersRec.append(repliesReceived)
						#print(allLettersRec)
						#print(all_words_file[0])
						allLettersRecS="".join(str(x) for x in allLettersRec)
						allLettersRecS=allLettersRecS.lower()
						for rowword in all_words_file:
							wordfile=rowword.strip('\n')
							if wordfile.isalpha()==True and allLettersRecS.isalpha()==True and len(wordfile)>=3 and wordfile not in w1:
								#print(allLettersRecS.lower(),wordfile)
								if is_allowed_specific_char(allLettersRecS.lower(),wordfile)==True:				
									w1.append(wordfile)
						w2=w1
						#if len(w1)>0:
							#print(w1)
						for rowword in allwords:
							if rowword in w2:
								w2.remove(rowword)
						#if playerid=='bvaw6zdw':
						#	print(repliesReceived)
						#	print(w2)
					
					ld=''
					minld=''
					localrank=''
					wordrank=''
					wordlocalrankp=''
					if windowsize==1 and words!='' and lastword!=0:
						#if playerid=='p4f3glnm':
							#print('lastword:'+lastword)
							#print('newword:'+words)
						if '-' in words:
							listwords=words.split('-')
							ldlist=[]
							ldlistMin=[]
							localranklist=[]
							for wordrow in listwords:
								ldwords=[]
								arguments= ' '+str(lastword) + ' '+str(wordrow)
								#flag=0
								#if lastword in w2:
								#	w2.remove(lastword)
								#	flag=1
								ldlist.append(subprocess.call (exepath+' ./main'+arguments,shell=True))
								w2.append(wordrow)
								if len(w2)>0:
									minld=9999
									i=0
									#while minld>1 and i<len(w2):
									while i<len(w2):
										arguments= ' '+str(w2[i]) + ' '+str(lastword)
										ldvalue=subprocess.call (exepath+' ./main'+arguments,shell=True)
										ldwords.append([w2[i],ldvalue])
										if ldvalue<minld:
											minld=ldvalue
										i=i+1
									ldlistMin.append(minld)
								
								minldwords=[]
								for rowld in ldwords:
									if rowld[1]==ld:
										minldwords.append(rowld[0])
								minldwordsrank=[]
								uniquewords=[]
								sumrank=0
								for rowld in minldwords:
									for rowrank in wordranklist:
										if rowld ==rowrank[0] and rowld not in uniquewords:
											uniquewords.append(rowrank[0])
											minldwordsrank.append(rowrank)
											sumrank=sumrank+rowrank[1]
								if words not in uniquewords:
									#minldwordsrank.append([words,99999])
									localrank='99999'
									wordrank='99999'
									wordlocalrankp='99999'
								else:
									df = pd.DataFrame(minldwordsrank,columns=['word','wordrank'])
									df['rank']=df['wordrank'].rank(method='min',ascending=1).astype(int)
									wordrank=df.loc[df['word'] == words, 'wordrank'].iloc[0]
									localrank=df.loc[df['word'] == words, 'rank'].iloc[0]
									wordlocalrankp=0
									if sumrank>0:
										wordlocalrankp=wordrank/sumrank	
								localranklist.append(localrank)
								
								w2S = "-".join(str(valueword) for valueword in w2)	
								w2.remove(wordrow)
								#if flag==1:
								#	w2.append(lastword)
								lastword=wordrow
							ld = "-".join(str(valueword) for valueword in ldlist)
							minld = "-".join(str(valueword) for valueword in ldlistMin)
							localrank = "-".join(str(valueword) for valueword in localranklist)
							
							
						else:
							#flag=0
							#if lastword in w2:
							#	w2.remove(lastword)
							#	flag=1
							arguments= ' '+str(lastword) + ' '+str(words)
							ld=subprocess.call (exepath+' ./main'+arguments,shell=True)
							w2.append(words)
							ldwords=[]
							if len(w2)>0:
								minld=9999
								i=0
								#while minld>1 and i<len(w2):
								while i<len(w2):
									arguments= ' '+str(w2[i]) + ' '+str(lastword)
									ldvalue=subprocess.call (exepath+' ./main'+arguments,shell=True)
									ldwords.append([w2[i],ldvalue])
									if ldvalue<minld:
										minld=ldvalue
									i=i+1
							
							minldwords=[]
							for rowld in ldwords:
								if rowld[1]==ld:
									minldwords.append(rowld[0])
							minldwordsrank=[]
							uniquewords=[]
							sumrank=0
							for rowld in minldwords:
								for rowrank in wordranklist:
									if rowld ==rowrank[0] and rowld not in uniquewords:
										uniquewords.append(rowrank[0])
										minldwordsrank.append(rowrank)
										sumrank=sumrank+rowrank[1]
							if words not in uniquewords:
								#minldwordsrank.append([words,99999])
								localrank='99999'
								wordrank='99999'
								wordlocalrankp='99999'
							else:
								df = pd.DataFrame(minldwordsrank,columns=['word','wordrank'])
								df['rank']=df['wordrank'].rank(method='min',ascending=1).astype(int)
								wordrank=df.loc[df['word'] == words, 'wordrank'].iloc[0]
								localrank=df.loc[df['word'] == words, 'rank'].iloc[0]
								wordlocalrankp=0
								if sumrank>0:
									wordlocalrankp=wordrank/sumrank
								#if playerid=='wvlxzkn5':
								#	print(df)
						
							#print(uniquewords)
							#print(words)
							#print(minldwordsrank)
							#print(df)
							
							#if playerid=='wvlxzkn5':
								#print("hey")
								#print(ldwords)
								#print(uniquewords)
								#print(minldwordsrank)
								#print("ld",ld)
								#print("min",minld)
								#print(lastword)
								#print(words)
								#print(localrank)
								#print(wordrank)
								#print(wordlocalrankp)
							w2S = "-".join(str(valueword) for valueword in w2)
							w2.remove(words)
							
							
							#if flag==1:
							#	w2.append(lastword.lower())
						#if playerid=="pi96dj16":
							#print(minld)
							#print(w2)
						#w2S = "-".join(str(valueword) for valueword in w2)
							#lastword=words
						#if playerid=='p4f3glnm':
							#print('ld:'+str(ld))
					
					lastwordS=''
					if words!='' and lastword!=0:
						lastwordS=lastword
					csvfile.write(str(phase)+','+str(playerid)+','+str(n)+','+str(d)+','+str(allLettersRecS)+','+str(iii)+','+str(requestsSent)+','+str(repliesReceived)+','+str(requestsReceived)+','+str(repliesSent)+','+str(words)+','+str(lastwordS)+','+str(ld)+','+str(minld)+','+str(w2S)+','+str(localrank)+','+str(wordrank)+','+str(wordlocalrankp)+'\n')
					csvfileall.write(str(phase)+','+str(playerid)+','+str(n)+','+str(d)+','+str(allLettersRecS)+','+str(iii)+','+str(requestsSent)+','+str(repliesReceived)+','+str(requestsReceived)+','+str(repliesSent)+','+str(words)+','+str(lastwordS)+','+str(ld)+','+str(minld)+','+str(w2S)+','+str(localrank)+','+str(wordrank)+','+str(wordlocalrankp)+'\n')
					countrequestsSent=0
					if words!='' and '-' not in words:
						lastword=words
					w2S=''
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
    if not os.path.exists(os.getcwd()+'/data-analytics-pipeline/test/results/h13/output/all'):
    	os.makedirs(os.getcwd()+'/data-analytics-pipeline/test/results/h13/output/all')
    	
    csvfileall = open(os.getcwd()+'/data-analytics-pipeline/test/results/h13/output/all/tsData.csv', 'w')
    csvfileall.write('session,player,n,d,letters,time,requestsSent,repliesReceived,requestsReceived,repliesSent,words,lastWord,LevenshteinDistance,minLevenshteinDistance,w2,wordlocalrank,wordrank,wordlocalrankp\n')
    
    #with open(os.getcwd()+'/data-analytics-pipeline/src/h13/all_words.txt', 'r') as f:
    #with open(os.getcwd()+'/data-analytics-pipeline/src/h13/3k.txt', 'r') as f:
    #with open(os.getcwd()+'/data-analytics-pipeline/src/h13/20k.txt', 'r') as f:
    #with open(os.getcwd()+'/data-analytics-pipeline/src/h13/google-10000-english-no-swears.txt', 'r') as f:
    #with open(os.getcwd()+'/data-analytics-pipeline/src/h13/google-10000-english-usa.txt', 'r') as f:
    #with open(os.getcwd()+'/data-analytics-pipeline/src/h13/5k1k.txt', 'r') as f:
    with open(os.getcwd()+'/data-analytics-pipeline/src/h13/20k.txt', 'r') as f:
    	all_words_file = f.readlines()
    seq=1
    wordranklist=[]
    for rowword in all_words_file:
    	wordfile=rowword.strip('\n')
    	wordranklist.append([wordfile,seq])
    	seq=seq+1
    #print(wordranklist)
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

    		filescsv(n,d,numseconds,len(phases),phases,csvfileall,windowsize,all_words_file,wordranklist)
    print (" -- h13 --")
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
    