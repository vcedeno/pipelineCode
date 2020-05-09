import sys
import os
import csv
import jsonschema
import json


def validate(schemaname,dataname):
	schema_json = open(schemaname, 'r')
	schema_data = schema_json.read()
	schema = json.loads(schema_data)
	
	with open(dataname) as json_data:
		d = json.load(json_data)
		result=jsonschema.validate(d, schema)
		if result=='None':
			return True
		else: 
			return False

## --------------------------
## Execution starts.
if __name__ == '__main__':
		
    if (len(sys.argv) != 3):
    	print ("  Error.  Incorrect usage.")
    	print ("  usage: exec infile outfile.")
    	print ("  Halt.")
    	quit()

    schemaname = sys.argv[1]
    dataname = sys.argv[2]
    value=validate(schemaname,dataname)
    
    	
    #json_ts = open(filename, 'r')
    #ts_data = json.load(json_ts)
    #numlinests= (len(ts_data['runPi']))
    #filename=ts_data["runPi"][0]["json_file"]
    #n=ts_data["runPi"][0]["n"]
    #k=ts_data["runPi"][0]["k"]	
    
    #numlines= (len(csv_data['csvToJson']))

