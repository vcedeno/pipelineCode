import sys
import os
import csv
import subprocess
import json


### -----------------------------
### Start.
def main(path,filename,groupslist):
		
    if not os.path.exists(os.getcwd()+'/property-inference-pipeline/test/results/h2/dynamic_word/'):
    	os.makedirs(os.getcwd()+'/property-inference-pipeline/test/results/h2/dynamic_word/')
    
    rfilename=[]
    for row in groupslist:
    	nd='n'+row[0]+'d'+row[1]
    	rfilename.append(path+nd+"/"+filename)
    rfilename1=rfilename[0]
    rfilename2=rfilename[1]
    rfilename3=rfilename[2]
    rfilename4=rfilename[3]
    print(rfilename2)
    rpath=os.getcwd()+'/property-inference-pipeline/src/h2/R_dynamic_matrix_with_k.R'
    subprocess.call (['Rscript',rpath,rfilename1,rfilename2,rfilename3,rfilename4])
    
    print (" -- h2 --")
    print (" -- good termination --")
    
## --------------------------
## Execution starts.
if __name__ == '__main__':
		
    if (len(sys.argv) != 3):
    	print ("  Error.  Incorrect usage.")
    	print ("  usage: exec infile outfile.")
    	print ("  Halt.")
    	quit()
    	
    path=sys.argv[1]
    filename=sys.argv[2]
    groups=sys.argv[3]
    print (" -- oi --")
    main(path,filename,groups)
    