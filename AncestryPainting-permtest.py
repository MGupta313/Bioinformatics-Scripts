#!/usr/bin/env python3
import sys
import re
import random

lineslist = []
countSameAncGene = 0
countInd = 0
geneHomozygosity = []
count = 0
gene = []
genename = []
newList = []
Average = []
StdDev = []
with open(sys.argv[1]) as file:
    for lines in file:
        lines = lines.rstrip("\n")
        lines = lines.split("\t")
        lineslist.append(lines) #making a list of lists with each row as a separate list
    numberOfGenes = len(lineslist)-1 #getting the number of genes present in the file

    #getting total number of individuals
    for i in range(len(lineslist[0])):
        if re.findall(pattern = "^IND.{2,5}[AB]$", string = lineslist[0][i]): 
            countInd = countInd +1
    countInd = countInd/2

    #calculating homozygosity for each gene
    for i in range(1, numberOfGenes+1):
        genename.append(lineslist[i][0])
        countSameAncGene = 0
        for j in range(1, len(lineslist[i]), 2):
            if lineslist[i][j] == lineslist[i][j+1]: #checking if ancestry codes on the two chromosomes match, for a single gene
                countSameAncGene = countSameAncGene +1  #counting number of same ancestry in individuals of one gene
                obsvd = round(countSameAncGene/countInd, 2)
        geneHomozygosity.append(obsvd)
   
    #shuffling the ancestry codes for each gene
    for i in range(1, numberOfGenes+1):
        lineslist[i].remove(lineslist[i][0]) #removing gene name to shuffle ancestry codes
        newList.append(lineslist[i])
    random.seed(sys.argv[3])
    for s in range(int(sys.argv[4])):
        for i in range(len(newList)):
            random.shuffle(newList[i]) #produces n number of replicates, n is input by the user
            count = 0
            for j in range(0, len(newList[i]), 2):
                if newList[i][j] == newList[i][j+1]: #checking if ancestry codes on the two chromosomes match, for a single gene
                    count = count+1       
            gene.append(count/countInd) #getting homozygosity of the shuffled population

    #calculating permuted average and permuted standard deviation
    for i in range(3):
        sumation = 0
        countnum = 0
        for j in range(i, len(gene), 3):
            sumation += gene[j] #gene is a list containing homozygosity for each gene, for each replicate
            countnum = countnum +1
        avg = sumation/countnum
        avg = round(avg, 2)
        Average.append(avg)
        
        sumdiffsq = 0
        for k in range(i, len(gene), 3):
            diff = gene[k] - avg
            diffsq = diff**2
            sumdiffsq += diffsq
            sqrt = sumdiffsq/countnum
        sd = sqrt**(1/2)
        sd = round(sd, 2)
        StdDev.append(sd)
        
with open(sys.argv[2], 'w') as output:
    output.write("{}\t{}\t{}\t{}\n".format("Gene","Observed","Permuted_Mean","Permuted_sd"))
    for i in range(numberOfGenes):
        output.write("{}\t{}\t{}\t{}\n".format(genename[i],geneHomozygosity[i],Average[i],StdDev[i]))