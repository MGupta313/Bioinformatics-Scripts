#!/usr/bin/env python3

import argparse
import re
import os
import math

parser = argparse.ArgumentParser()
parser.add_argument("-a",help="Enter an input genome:")
parser.add_argument("-b",help="Enter another input genome:")
parser.add_argument("-d","--dir",help="Enter a directory of input genomes:")
parser.add_argument("-s", "--setsize",help="Enter the set size:", default = 1000)
parser.add_argument("-S", "--seed",help="Give seed value for random generation:")
parser.add_argument("-o", "--output", help="name of output file", default="genomeDist.txt")
parser.add_argument("-t", "--threads",help="Enter the number of threads to run:", default = 1)
args = parser.parse_args()


def calcDist(subset1, subset2):
    jaccintersect = len(subset1.intersection(subset2))
    jaccunion = len(subset1.union(subset2))
    jaccindex = jaccintersect/jaccunion
    
    jaccdist = 1-jaccindex
    natlog = math.log(2(jaccdist)/(1+jaccdist))
    mashdist = -(1/17)*natlog
    return mashdist

def kmercounter(kmerinputfile):
    with open(kmerinputfile) as f:
        next(f) #to skip first line
        lines = f.readlines()
    y = ''.join(lines)
    final = y.replace('\n', '')
    sortList = []
    kmerList1 = []
    kmerList2 = []
    kmerLength=17
    rangeOfIndex = len(final)-kmerLength
    count = 0
    for i in range(rangeOfIndex+1):
        kmerSeq = final[i:i+kmerLength]
        kmerSeqComp = kmerSeq[::-1]
        sorList = [kmerSeq, kmerSeqComp]
        sortList.sort()
        if kmerinputfile == inputfile1:
            kmerList1.append(sortList[0])
        elif kmerinputfile == inputfile2:
            kmerList2.append(sortList[0])

    #generating random kmers to evaluate
    random.seed(args.S)
    random.shuffle(kmerList1)
    subset1 = []
    setsize = arg.s
    for i in range(setsize):
        subset1.append(kmerList1[i])
    random.shuffle(kmerList2)
    subset2 = []
    setsize = arg.s
    for i in range(setsize):
        subset2.append(kmerList2[i])
    calcDist(subset1, subset2)        

    
def all2fasta(checkfile):
    with open(checkfile):
        ext = re.search(pattern = "(.[A-Za-z]+)$", string =checkfile)
        ext = ext.group()
        inputFileName = checkfile.replace(ext, "")
        lines = checkfile.readlines()

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
def checkFasta(inputFile):
    with open(inputFile) as f:
#         header = f.readline()
        lines = f.readlines()
        if re.findall(pattern = '^[^BJOUXZbjouxz]+$', string = lines[1]):
            print("Not a nucleotide file")
            break
        else:
            if re.search(pattern = '^>\w+\d+', string = lines[0]):
                print("input file is in correct format")
                kmercounter(inputFile)
            else:
                all2fasta(inputFile)

                
def main(inputFile1, inputFile2):
    checkFasta(inputFile1)
    checkFasta(inputFile2)

    
genomedistoutputfile = args.o              
with open(genomedistoutputfile, 'w') as of:    
    if args.a and args.b:        
        inputFile1 = args.a
        inputFile2 = args.b 
        main()
        of.write("#"+inputfile1+"\t"+inputfile2+"\t"+mashdist)
    if args.d:
        dirname = args.d
        listOfFiles = []
        mashdict = {}
        for file in os.listdir(dirname):
            listOfFiles.append(file)
            for i in range(len(listOfFiles)):
                for j in range(len(listOfFiles)):
                    inputfile1 = listOfFiles[i]
                    inputfile2 = listOfFiles[j]
                    main()
                    of.write("\t"+listOfFiles+"\n")
                    of.write(listOfFiles[j]+"\t"+mashdist+"\n")
                    
    if args.a and args.d:
        inputFile1 = args.a
        dirname = args.d
        listOfFiles = []
        for file in os.listdir(dirname):
            listOfFiles.append(file)
            for i in range(len(listOfFiles)):
                inputfile2 = listOfFiles[i]
                main()
                of.write("#filename"+"\t"+"genomeDist"+"\n")
                of.write(inputfile2+"\t"+mashdist+"\n")

    

        

            
    