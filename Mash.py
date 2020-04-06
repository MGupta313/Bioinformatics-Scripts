#!/usr/bin/env python3

import argparse
import re
import os
import math
import random
import multiprocessing as mp

parser = argparse.ArgumentParser()
parser.add_argument("-a",help="Enter an input genome:")
parser.add_argument("-b",help="Enter another input genome:")
parser.add_argument("-d","--dir",help="Enter a directory of input genomes:")
parser.add_argument("-s",help="Enter the set size:", default = 1000)
parser.add_argument("-S",help="Give seed value for random generation:")
parser.add_argument("-o", help="name of output file", default = "genomeDist.txt")
parser.add_argument("-t",help="Enter the number of threads to run:", default = 1)
args = parser.parse_args()


def calcDist(subset1, subset2):
    s1 = set(subset1)
    s2 = set(subset2)
    jaccintersect = len(s1.intersection(s2))
    jaccunion = len(s1.union(s2))
    jaccindex = jaccintersect/jaccunion
    jaccdist = 1-jaccindex
    var = 2*jaccdist/(1+jaccdist)
    global mashdist
    mashdist = str(-(1/17)*(math.log(var)))
    return mashdist

def kmercounter(kmerinputfile1, kmerinputfile2):
    with open(kmerinputfile1) as f1:
        next(f1) #to skip first line
        lines1 = f1.readlines()
    y1 = ''.join(lines1)
    final1 = y1.replace('\n', '')
    sortList = []
    kmerList1 = []
    kmerLength=17
    rangeOfIndex = len(final1)-kmerLength
    for i in range(rangeOfIndex+1):
        kmerSeq = final1[i:i+kmerLength]
        sortList.append(kmerSeq)
        kmerSeqComp = kmerSeq[::-1]
        sortList.append(kmerSeqComp)
        sortList.sort()
        kmerList1.append(sortList[0])
        
    with open(kmerinputfile2) as f2:
        next(f2) #to skip first line
        lines2 = f2.readlines()
    y2 = ''.join(lines2)
    final2 = y2.replace('\n', '')
    sortList = []
    kmerList2 = []
    kmerLength=17
    rangeOfIndex = len(final2)-kmerLength
    for i in range(rangeOfIndex+1):
        kmerSeq = final1[i:i+kmerLength]
        sortList.append(kmerSeq)
        kmerSeqComp = kmerSeq[::-1]
        sortList.append(kmerSeqComp)
        sortList.sort()
        kmerList2.append(sortList[0])

    #generating random kmers to evaluate
    random.seed(int(args.S))
    random.shuffle(kmerList1)
    random.shuffle(kmerList2)
    setsize = int(args.s)
    subset1 = kmerList1[0:setsize]
    subset2 = kmerList2[0:setsize]
    print(len(subset2))
    
    #for i in range(setsize):
     #   subset1.append(kmerList1[i])
      #  print(len(subset1))
       # subset2.append(kmerList2[i])
        #print(len(subset2))

    calcDist(subset1, subset2)        

    
def all2fasta(checkfile):
    with open(checkfile) as f:
        ext = re.search(pattern = "(.[A-Za-z]+)$", string =checkfile)
        ext = ext.group()
        inputFileName = checkfile.replace(ext, "")
        lines = f.readlines()

    if re.search(pattern = '^ID', string = lines[0]):
        #print("EMBL")
        fileFormat = "embl"
    if re.search(pattern = '^@', string = lines[0]):
        #print("FASTQ")
        fileFormat = "fastq"
    if re.search(pattern = '^LOCUS', string = lines[0]):
        #print("GENBANK")
        fileFormat = "genbank"
    if re.search(pattern = '^[(#MEGA)(#mega)]', string = lines[0]):
        #print("MEGA")
        fileFormat = "mega"

    #multisequence files
    eachLine=[]
    if fileFormat == "embl":
        for i in range(len(lines)):
            eachLine.append(lines[i])
            if re.findall(pattern = '     [ACGTNacgtn]+', string = eachLine[i]):
                outputFileName = inputFileName+".fasta"
                outputfile = open(outputFileName, 'w')
                for i in range(len(lines)):
                    eachLine.append(lines[i]) #separating each element of the previous list
                    if re.findall(pattern = 'AC   ', string= eachLine[i]):
                        accNum = eachLine[i]
                        accNum = accNum.rstrip(";\n")
                        accNum = accNum.split('   ')
                        accNum = accNum[1]
                        outputfile.write(">" + accNum + "\n")
                    if lines[i].startswith('SQ'):
                        for j in range(i+1, len(lines)-1):
                            seq = lines[j]
                            seq = seq.split("     ")
                            seq = seq[1]
                            if re.findall(pattern = " ", string=seq):
                                seq = seq.replace(" ", "")
                                outputfile.write(seq+"\n")


    if fileFormat == "genbank":
        for i in range(len(lines)):
            eachLine.append(lines[i])
            if re.findall(pattern = '^( )+\d+( )[ACGTNacgtn]+', string = eachLine[i]):
                outputFileName = inputFileName+".fasta"
                outputfile = open(outputFileName, 'w')
                for i in range(len(lines)):
                    eachLine.append(lines[i]) #separating each element of the previous list
                    if re.findall(pattern = 'ACCESSION', string= eachLine[i]):
                        accNum = eachLine[i]
                        accNum = accNum.rstrip(";\n")
                        accNum = accNum.split('   ')
                        accNum = accNum[1]
                        accNum = accNum.split(" ")
                        accNum = accNum[0]
                        outputfile.write(">" + accNum +"\n")
                    if re.findall(pattern = '^( )+\d+( )[ACGTNacgtn]+', string = eachLine[i]):
                        seq = eachLine[i]
                        seq = seq.rstrip("\n")
                        seq = seq.split("1 ")
                        seq = seq[1]
                        seq = seq.replace(" ", "")
                        outputfile.write(seq +"\n")        


    if fileFormat == "mega":
        for i in range(len(lines)):
            eachLine.append(lines[i])
            if re.findall(pattern = '^[ACGTNacgtn]+$', string= eachLine[i]):
                outputFileName = inputFileName + ".fasta"
                outputfile = open(outputFileName, 'w')
                for i in range(3, len(lines)):
                    eachLine.append(lines[i]) #separating each element of the previous list
                    if re.findall(pattern = '#', string= eachLine[i]):
                        header = eachLine[i]
                        header = header.split("#")
                        header = header[1]
                        header = ">"+header
                        outputfile.write(header)
                    if re.findall(pattern = '^[ACGTNacgtn]+$', string= eachLine[i]):
                        seq = eachLine[i]
                        outputfile.write(seq)
           
           

    if fileFormat == "fastq":
        for i in range(len(lines)):
            eachLine.append(lines[i])
            if re.findall(pattern = '^[ACGTNacgtn]+$', string = eachLine[i]):
                outputFileName = inputFileName+".fna"
        outputfile = open(outputFileName, 'w')
        for i in range(len(lines)):
            eachLine.append(lines[i]) #separating each element of the previous list
            if re.findall(pattern = '^@', string= eachLine[i]):
                header = eachLine[i]
                header = header.rstrip("\n")
                header = header.split("@")
                header = header[1]
            if re.findall(pattern = '^[ACGTNacgtn]+$', string = eachLine[i]):
                seq = eachLine[i]
                outputfile.write(">"+header+"\n"+seq)
    
    kmercounter(outputfile)

#checking the correct file format
def checkFasta(inputFile1, inputFile2):
    with open(inputFile1) as f1:
        header1 = f1.readline()
    with open(inputFile2) as f2:
        header2 = f2.readline()
        if re.search(pattern = '^>', string = header1):
            if re.search(pattern = '^>', string = header2):
                print("input file is in correct format")
                kmercounter(inputFile1, inputFile2)
        else:
            all2fasta(inputFile)
        

                
def main(inputFile1, inputFile2):
    checkFasta(inputFile1, inputFile2)

if args.o:
    print("ok")
    
with open(args.o, 'w') as of:    
    if args.a and args.b:        
        inputfile1 = args.a
        inputfile2 = args.b 
        main(inputfile1, inputfile2)
        of.write("#"+inputfile1+"\t"+inputfile2+"\t"+mashdist)
    elif args.d:
        if args.t:
            dirname = args.d
            listOfFiles = []
            tuplist= []
            mashdict = {}
            for file in os.listdir(dirname):
                listOfFiles.append(file)
                for i in listOfFiles:
                    for j in listOfFiles:
                        tupfile = (i,j)
                        tuplist.append(tupfile)
                p = mp.Pool(args.t)
                m = starmap(main, tuplist)
        if not args.t:
            dirname = args.d
            listOfFiles = []
            mashdict = {}
            for file in os.listdir(dirname):
                listOfFiles.append(file)
                for i in range(len(listOfFiles)):
                    for j in range(len(listOfFiles)):
                        inputfile1 = listOfFiles[i]
                        inputfile2 = listOfFiles[j]
                        main(inputfile1, inputfile2)
                        of.write("\t"+listOfFiles+"\n")
                        of.write(listOfFiles[j]+"\t"+mashdist+"\n")
                    
    elif args.a and args.d:
        inputfile1 = args.a
        dirname = args.d
        listOfFiles = []
        for file in os.listdir(dirname):
            listOfFiles.append(file)
            for i in range(len(listOfFiles)):
                inputfile2 = listOfFiles[i]
                main(inputfile1, inputfile2)
                of.write("#filename"+"\t"+"genomeDist"+"\n")
                of.write(inputfile2+"\t"+mashdist+"\n")

    elif args.a:
        if not args.b and args.d:
            print("Only one input file given")
            exit
    elif args.b:
        if not args.a and args.d:
            print("Only one input file given")
            exit