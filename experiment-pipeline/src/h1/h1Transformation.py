import sys
import os
import csv
import operator
from datetime import time, datetime, timedelta
from itertools import cycle
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime as dt
import time
import glob
import json

def main(inputpath,anagrams,CompletedSessionSummary,InstructionsAnagrams,LetterTransactions,Neighbors,PublicGoods,TeamWords,TimeSpent,UserLetters):

    startTime = datetime.now()
    allfiles=[anagrams,CompletedSessionSummary,InstructionsAnagrams,LetterTransactions,Neighbors,PublicGoods,TeamWords,TimeSpent,UserLetters]
    
    #files=[]
    for row in allfiles:
    	fileconvert=inputpath+'/'+row
    	#files.append(row)
    	with open(fileconvert+'.csv', "r") as f:
    		d_reader = csv.DictReader(f)
    		headers = d_reader.fieldnames
    	fieldnames = headers
    	csvfile = open(fileconvert+'.csv', 'r')
    	jsonfile = open('experiment-pipeline/json-schema/h1/input/datasets/'+row+'.json', 'w')
    	csvfile_reader=csv.reader(csvfile,delimiter=',')
    	#reader = csv.DictReader( csvfile, fieldnames)
    	next(csvfile_reader)
    	jsondata={row:[{fieldnames[index]:str(row1) for index,row1 in enumerate(row)} for row in csvfile_reader]}
    	#print(jsondata)
    	json.dump(jsondata,jsonfile,indent=4)
    
    #dajsonfile = open('dataAnalytics.json', 'w')
    #jsondata={'dataAnalytics':[{'json_file':str(row)} for row in files]}
    #json.dump(jsondata,dajsonfile,indent=4)

    endTime=datetime.now()

    print (" elapsed time (seconds): ",endTime-startTime)
    print (" elapsed time (hours): ",(endTime-startTime)/3600.0)

    print (" -- h1 Transformation --")
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
	print (" -- h1 Transformation --")
	print (" -- good termination from main --")