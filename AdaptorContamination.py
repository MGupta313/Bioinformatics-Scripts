#!/usr/bin/env python3

# Python script for finding adaptor contamination in raw FastQ file 

import re
import sys

k = sys.argv[1]  #input length of substrings
file = sys.argv[2]    #input input file - FASTQ format

dictKey = {}
kmerList = []

with open(file) as f:
lines = f.readlines()
for i in range(len(lines)):
if re.search(pattern = "^[ATGC]{8}", string = lines[i]): #reading only raw sequences lines and discarding others
for j in range(len(lines[i])-int(k)):
kmer = lines[i][j:5+j]    #producing kmers
if kmer in dictKey:
dictKey[kmer] = dictKey[kmer]+1   #counting kmers
else:
dictKey[kmer] = 1
#sorting dictionary in descending order to give substrings of k length with highest frequency first
sortedDict = sorted(dictKey.items(), key = lambda item:item[1], reverse = True)


#Converting sorted dictionary into a list of substrings with highest to lowest frequencies
for key in sortedDict:
kmerList.append(key[0])
print("Sorted list of substrings based on their frequencies")
print(kmerList) #stdout for list of substrings

#creates a file with a table of substrings and their frequencies
with open(file+"_frequency_output.txt", "w") as fo:
fo.write("Substring"+"\t"+ "Frequency"+"\n")
for key in sortedDict:
fo.write(key[0]+"\t"+str(key[1])+"\n")
