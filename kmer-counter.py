#! /usr/bin/python3

import sys

#taking inputs
k=int(sys.argv[1])
filename=sys.argv[2]

#parsing the input file
file=open(filename,'r')
file.readline()

with open(filename) as file
    seqList = []
    for line in file:
        line=line.rstrip()
        seqList+=line

    l=len(seqList)
    kmerDict = {}
    for i in range(l-k):
        key=seqList[i:i+k]
        key="".join(key)
        if key in kmerDict:
            kmerDict[key] += 1
        else:		
            kmerDict[key] = 1	

    for key in sorted(kmerDict):
        print(key,"\t",kmerDict[key])