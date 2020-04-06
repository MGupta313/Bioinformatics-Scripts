#!/usr/bin/env python3

import sys
import re
import random

lineslist = []
countSameAncGene = 0
countInd = 0
geneHomozygosity = []
gene = []
genename = []
Average = []
StdDev = []
newlist = []
with open('ancestryPainting.txt') as file:
    for lines in file:
        lines = lines.rstrip("\n")
        lines = lines.split("\t")
        lineslist.append(lines)
    numberOfGenes = len(lineslist)-1

    for i in range(len(lineslist[0])):
        if re.findall(pattern = "^IND.{2,5}[AB]$", string = lineslist[0][i]):
            countInd = countInd +1
    countInd = countInd/2

    for i in range(1, numberOfGenes+1):
        genename.append(lineslist[i][0])
        countSameAncGene = 0
        for j in range(1, len(lineslist[i]), 2):
            if lineslist[i][j] == lineslist[i][j+1]:
                countSameAncGene = countSameAncGene +1  
                obsvd = round(countSameAncGene/countInd, 2)
        geneHomozygosity.append(obsvd)
    #print(geneHomozygosity)
    
    for i in range(1, numberOfGenes+1):
        lineslist[i].remove(lineslist[i][0])
        newlist.append(lineslist[i])
    #print(newlist[0])

    random.seed(100)
    for s in range(1000):
        for i in range(len(newlist)):
            random.shuffle(newlist[i])
            count = 0
            for j in range(0, len(newlist[i]), 2):
                if newlist[i][j] == newlist[i][j+1]:
                    count = count+1       
            gene.append(count/countInd)
#             print(gene)
    
    for i in range(3):
        sumation = 0
        countnum = 0
        for j in range(i, len(gene), 3):
            sumation += gene[j]
            countnum = countnum +1
        avg = sumation/countnum
        avg = round(avg, 2)
        Average.append(avg)
        print("Avg:",avg)
        sumdiffsq = 0
        for k in range(i, len(gene), 3):
            diff = gene[k] - avg
            diffsq = diff**2
            sumdiffsq += diffsq
            sqrt = sumdiffsq/countnum
        sd = sqrt**(1/2)
        sd = round(sd, 2)
        StdDev.append(sd)
        print("Sd", sd)
 with open('output.txt', 'w') as output:
     output.write("{}\t{}\t{}\t{}\n".format("Gene","Observed","Permuted_Mean","Permuted_sd"))
     for i in range(numberOfGenes):
         output.write("{}\t{}\t{}\t{}\n".format(genename[i],geneHomozygosity[i],Average[i],StdDev[i]))
