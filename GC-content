#!/usr/bin/env python3
import sys
filedict={}
with open(sys.argv[1],'r') as file:
	for line in file:
		line=line.strip("\n")

		if line[0]=='>':
			seqnumber=line[1:len(line)]
		else:
			if seqnumber not in filedict:
				filedict[seqnumber]=str(line[0:len(line)])
			else:
				filedict[seqnumber]+=line[0:len(line)]
	GCdict={}
	for key,value in filedict.items():

		freq=[]
		for i in range(0,len(value),25):
			GCCount=0
			for j in range(len(value[i:i+50])):
				if value[i+j]=='G' or value[i+j] == 'C':
					GCCount+=1
			GCCount=(GCCount/len(value[i:i+50]))*100
			freq.append(GCCount)
			GCdict[key]=freq
			#print(len(value[i:i+50]))
	GCContent={}
	for key,value in GCdict.items():
		GCContent={}
		print("{0}".format(key))
		print("{0}\t{1}".format("%GC","Frequency"))
		for row in value:
			range1=(row//5)*5
			if range1 in GCContent:
				GCContent[range1]+=1
			else:
				GCContent[range1]=1
		
		for i in sorted(GCContent.keys()):
			print("{0}-{1}\t{2}".format(int(i),int(i+5),GCContent[i]/len(value)))



		
			
    	
    			

    		
    			
    		
    		
    	
    		
    		


    