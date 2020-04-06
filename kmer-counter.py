#!/bin/env python

# Write your code here
import sys

with open(sys.argv[2]) as f:
    next(f) #to skip first line
    lines = f.readlines()
y = ''.join(lines)
final = y.replace('\n', '')

kmerDict = {}
kmerLength=sys.argv[1]
rangeOfIndex = len(final)-kmerLength
count = 0
for i in range(rangeOfIndex+1):
#     kmerLength=3 #arg
    kmerSeq = final[i:i+kmerLength]
#     print(kmer)
    if kmerSeq in kmerDict:
        kmerDict[kmerSeq] +=1
    else:
        kmerDict[kmerSeq] = 1
# print(kmerDict)

keyList = kmerDict.keys()
# print(keyList)
sortedKeyList = sorted(keyList)
# print(a)

for key in sortedKeyList:
    print(key,"\t",kmerDict[key])