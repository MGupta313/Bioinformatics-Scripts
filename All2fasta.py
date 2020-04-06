# !/usr/bin/env python3

import sys
import re

inputFileName = sys.argv[1] 
inputfile = open(inputFileName, 'r')
lines = inputfile.readlines()
#check format of the file

if re.search(pattern = '^ID', string = lines[0]):
    print("EMBL")
    fileFormat = "embl"
elif re.search(pattern = '^@', string = lines[0]):
    print("FASTQ")
    fileFormat = "fastq"
elif re.search(pattern = '^LOCUS', string = lines[0]):
    print("GENBANK")
    fileFormat = "genbank"
elif re.search(pattern = '^[(#MEGA)(#mega)]', string = lines[0]):
    print("MEGA")
    fileFormat = "mega"

#multisequence files
eachLine=[]
if fileFormat == "embl":
    for i in range(len(lines)):
        eachLine.append(lines[i])
        if re.findall(pattern = '     [ACGTNacgtn]+', string = eachLine[i]):
            outputFileName = inputFileName+".fna"
        elif re.findall(pattern = '     [^BJOUXZbjouxz]+', string = eachLine[i]):
            outputFileName = inputFileName+".faa"
    outputfile = open(outputFileName, 'w')
    for i in range(len(lines)):
        eachLine.append(lines[i]) #separating each element of the previous list
        if re.findall(pattern = 'AC   ', string= eachLine[i]):
            accNum = eachLine[i]
            accNum = accNum.rstrip(";\n")
            accNum = accNum.split('   ')
            accNum = accNum[1]
            outputfile.write(">" + accNum + "|")
            #print(accNum)
        if re.findall(pattern = 'DE   ', string= eachLine[i]):
            desc = eachLine[i]
            desc = desc.rstrip(";\n")
            desc = desc.split('   ')
            desc = desc[1]
            outputfile.write(desc+"\n")
            #print(desc)
        if re.findall(pattern = '     [ACGTNacgtn]+', string = eachLine[i]):
            seq = eachLine[i]
            seq = seq.split("     ")
            seq = seq[1]
            seq = seq.replace(" ", "")
            outputfile.write(seq+"\n")
            #print(seq)
        elif re.findall(pattern = '     [^BJOUXZbjouxz]+', string = eachLine[i]):
            seq = eachLine[i]
            seq = seq.split("     ")
            seq = seq[1]
            seq = seq.replace(" ", "")
            outputfile.write(seq+"\n")

if fileFormat == "genbank":
    for i in range(len(lines)):
        eachLine.append(lines[i])
        if re.findall(pattern = '^( )+\d+( )[ACGTNacgtn]+', string = eachLine[i]):
            outputFileName = inputFileName+".fna"
        elif re.findall(pattern = '( )+\d+( )[^BJOUXZbjouxz]+', string = eachLine[i]):
            outputFileName = inputFileName+".faa"
    outputfile = open(outputFileName, 'w')
    for i in range(len(lines)):
        eachLine.append(lines[i]) #separating each element of the previous list
        if re.findall(pattern = 'ACCESSION', string= eachLine[i]):
            accNum = eachLine[i]
            accNum = accNum.rstrip(";\n")
            accNum = accNum.split('   ')
            accNum = accNum[1]
            outputfile.write(">" + accNum +"\n")
        #if re.search(pattern = 'DEFINITION', string= eachLine[i]):
         #   desc = eachLine[i]
          #  desc = desc.rstrip(";\n")
           # desc = desc.split('  ')
            #desc = desc[1]
            #outputfile.write(desc + "\n")
        if re.findall(pattern = '^( )+\d+( )[ACGTNacgtn]+', string = eachLine[i]):
            seq = eachLine[i]
            seq = seq.rstrip("\n")
            seq = seq.split("1 ")
            seq = seq[1]
            seq = seq.replace(" ", "")
            outputfile.write(seq +"\n")
       #     print(seq)
        elif re.findall(pattern = '^( )+\d+( )[^BJOUXZbjouxz]+', string = eachLine[i]):
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
            outputFileName = inputFileName + ".fna"
        elif re.findall(pattern = '^[^BJOUXZbjouxz]+$', string = eachLine[i]):
            outputFileName = inputFileName + ".faa"
    outputfile = open('KU325498.mega.fna', 'w')
    for i in range(3, len(lines)):
        eachLine.append(lines[i]) #separating each element of the previous list
        if re.findall(pattern = '#', string= eachLine[i]):
            header = eachLine[i]
            header = header.split("#")
            header = header[1]
            outputfile.write(">"+header+"\n")
      #      print(header)
        if re.findall(pattern = '^[ACGTNacgtn]+$', string= eachLine[i]):
            seq = eachLine[i]
            outputfile.write(seq)
     #       print(seq)
        elif re.findall(pattern = '^[^BJOUXZbjouxz]+$', string = eachLine[i]):
            seq = eachLine[i]
            outputfile.write(seq)
      #      print(seq)


if fileFormat == "fastq":
    for i in range(len(lines)):
        eachLine.append(lines[i])
        if re.findall(pattern = '^[ACGTNacgtn]+$', string = eachLine[i]):
            outputFileName = inputFileName+".fna"
        elif re.findall(pattern = '^[^BJOUXZbjouxz]+$', string = eachLine[i]):
            outputFileName = inputFileName+".faa"
    outputfile = open('example.fastq.fna', 'w')
    for i in range(len(lines)):
        eachLine.append(lines[i]) #separating each element of the previous list
        if re.findall(pattern = '^@', string= eachLine[i]):
            header = eachLine[i]
            header = header.rstrip("\n")
            header = header.split("@")
            header = header[1]
#             outputfile.write(">"+header)
    #        print(header)
        if re.findall(pattern = '^[ACGTNacgtn]+$', string = eachLine[i]):
            seq = eachLine[i]
            outputfile.write(">"+header+"\n"+seq)
     #       print(seq)
        elif re.findall(pattern = '^[^BJOUXZbjouxz]+$', string = eachLine[i]):
            seq = eachLine[i]
            outputfile.write(">"+header+"\n"+seq)
      #      print(seq)