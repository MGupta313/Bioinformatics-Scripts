#!/usr/bin/env python3

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i1",help="enter the first file")
parser.add_argument("-i2",help="enter the second file")
parser.add_argument("-m",type=float,help="enter minimum percent overlap")
parser.add_argument("-j", action="store_true",
                    help="allows to print member of the first set and the member of the second set that it overlaps with on the same line")
parser.add_argument("-o",help="name of output file")
args = parser.parse_args()

linesFile1 = []
linesFile2 = []
threshold = args.m
with open(args.i1, 'r') as file1:
    for lines in file1:
        lines = lines.split()
        linesFile1.append(lines)
# print(linesFile1, "\n")
with open(args.i2, 'r') as file2:
    for lines in file2:
        lines = lines.rstrip("\t")
        linesFile2.append(lines.split())
# print(linesFile2)
with open(args.o,'w') as outputOverlapFile:
    for i in range(len(linesFile1)):
        for j in range(len(linesFile2)):
            if linesFile1[i][0] == linesFile2[j][0]: #making sure that comparison is done on the same chromosome
                if linesFile1[i][1] <= linesFile2[j][1]: #checking if start_one > start_two
                    if linesFile1[i][2] >= linesFile2[j][1]: #checking if stop_one < start_two
                        overlap = min(int(linesFile1[i][2]), int(linesFile2[j][2])) - max(int(linesFile1[i][1]), int(linesFile2[j][1]))
                        fragmentLen = int(linesFile1[i][2]) - int(linesFile1[i][1])
                        overlapPercentage = (overlap//fragmentLen)*100
                        if overlapPercentage >= threshold:
                            if args.j: #when join option is given
                                for n in range(len(linesFile1[0])):
                                    outputOverlapFile.write(linesFile1[i][n]+"\t")
                                for m in range(len(linesFile2[0])):
                                    outputOverlapFile.write(linesFile2[j][m]+"\t")
                                outputOverlapFile.write("\n")
                            else: #when join option is not given
                                for n in range(len(linesFile1[0])):
                                    outputOverlapFile.write(linesFile1[i][n]+"\t")
                                outputOverlapFile.write("\n")
                else: #linesFile1[i][1] > linesFile2[j][1]:
                    if linesFile2[j][2] >= linesFile1[i][1]: #checking if stop_two > start_one
                        overlap = min(int(linesFile1[i][2]), int(linesFile2[j][2])) - max(int(linesFile1[i][1]), int(linesFile2[j][1]))
                        fragmentLen = int(linesFile1[i][2]) - int(linesFile1[i][1])
                        overlapPercentage = (overlap//fragmentLen)*100
                        if overlapPercentage >= threshold:
                            if args.j: #when join option is given
                                for n in range(len(linesFile1[0])):
                                    outputOverlapFile.write(linesFile1[i][n]+"\t")
                                for m in range(len(linesFile2[0])):
                                    outputOverlapFile.write(linesFile2[j][m]+"\t")
                                outputOverlapFile.write("\n")
                            else: #when join option is not given
                                for n in range(len(linesFile1[0])):
                                    outputOverlapFile.write(linesFile1[i][n]+"\t")
                                outputOverlapFile.write("\n")