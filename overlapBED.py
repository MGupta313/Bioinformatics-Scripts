#!/usr/bin/env python3


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i1",help="Enter the first file:")
parser.add_argument("-i2",help="Enter the second file:")
parser.add_argument("-m",type=float,help="Enter minimum percent overlap:")
parser.add_argument("-j", action="store_true",
                    help="allows to print member of the first set and the member of the second set that it overlaps with on the same line")
parser.add_argument("-o",help="name of output file")
args = parser.parse_args()

linesFile1 = []
linesFile2 = []
threshold = 0
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
    if args.j:
        for i in range(len(linesFile1)):
            for j in range(len(linesFile2)):
                if linesFile1[i][0] == linesFile2[j][0]: #making sure that comparison is done on the same chromosome
                    if linesFile1[i][1] > linesFile2[j][1]: #checking if start_one > start_two
                        if linesFile1[i][2] < linesFile2[j][2]: #checking if stop_one < stop_two
                            overlap = min(int(linesFile1[i][2]), int(linesFile2[j][2])) - max(int(linesFile1[i][1]), int(linesFile2[j][1]))
                            if overlap >= threshold:
                                outputOverlapFile.write(linesFile1[i])
                                outputOverlapFile.write("\t")
                                outputOverlapFile.write(linesFile2[j])
                        elif linesFile1[i][2] == linesFile2[j][2]: #checking if stop_one < stop_two
                            overlap = min(int(linesFile1[i][2]), int(linesFile2[j][2])) - max(int(linesFile1[i][1]), int(linesFile2[j][1]))
                            if overlap >= threshold:
                                outputOverlapFile.write(linesFile1[i])                                 
                                outputOverlapFile.write("\t")                                 
                                outputOverlapFile.write(linesFile2[j])
                        elif linesFile1[i][2] > linesFile2[j][2]: #checking if stop_one < stop_two
                            overlap = min(int(linesFile1[i][2]), int(linesFile2[j][2])) - max(int(linesFile1[i][1]), int(linesFile2[j][1]))
                            if overlap >= threshold:
                                outputOverlapFile.write(linesFile1[i])                                 
                                outputOverlapFile.write("\t")                                 
                                outputOverlapFile.write(linesFile2[j])
                    elif linesFile1[i][1] == linesFile2[j][1]: #checking if start_one > start_two
                        if linesFile1[i][2] < linesFile2[j][2]: #checking if stop_one < stop_two
                            overlap = min(int(linesFile1[i][2]), int(linesFile2[j][2])) - max(int(linesFile1[i][1]), int(linesFile2[j][1]))
                            if overlap >= threshold:
                                outputOverlapFile.write(linesFile1[i])                                 
                                outputOverlapFile.write("\t")                                 
                                outputOverlapFile.write(linesFile2[j])
                        elif linesFile1[i][2] == linesFile2[j][2]: #checking if stop_one < stop_two
                            overlap = min(int(linesFile1[i][2]), int(linesFile2[j][2])) - max(int(linesFile1[i][1]), int(linesFile2[j][1]))
                            if overlap >= threshold:
                                outputOverlapFile.write(linesFile1[i])                                 
                                outputOverlapFile.write("\t")                                 
                                outputOverlapFile.write(linesFile2[j])
                        elif linesFile1[i][2] > linesFile2[j][2]: #checking if stop_one < stop_two
                            overlap = min(int(linesFile1[i][2]), int(linesFile2[j][2])) - max(int(linesFile1[i][1]), int(linesFile2[j][1]))
                            if overlap >= threshold:
                                outputOverlapFile.write(linesFile1[i])                                 
                                outputOverlapFile.write("\t")                                 
                                outputOverlapFile.write(linesFile2[j])
                    elif linesFile1[i][1] < linesFile2[j][1]: #checking if start_one > start_two
                        if linesFile1[i][2] < linesFile2[j][2]: #checking if stop_one < stop_two
                            overlap = min(int(linesFile1[i][2]), int(linesFile2[j][2])) - max(int(linesFile1[i][1]), int(linesFile2[j][1]))
                            if overlap >= threshold:
                                outputOverlapFile.write(linesFile1[i])                                 
                                outputOverlapFile.write("\t")                                 
                                outputOverlapFile.write(linesFile2[j])
                        elif linesFile1[i][2] == linesFile2[j][2]: #checking if stop_one < stop_two
                            overlap = min(int(linesFile1[i][2]), int(linesFile2[j][2])) - max(int(linesFile1[i][1]), int(linesFile2[j][1]))
                            if overlap >= threshold:
                                outputOverlapFile.write(linesFile1[i])                                 
                                outputOverlapFile.write("\t")                                 
                                outputOverlapFile.write(linesFile2[j])
                        elif linesFile1[i][2] > linesFile2[j][2]: #checking if stop_one < stop_two
                            overlap = min(int(linesFile1[i][2]), int(linesFile2[j][2])) - max(int(linesFile1[i][1]), int(linesFile2[j][1]))
                            if overlap >= threshold:
                                outputOverlapFile.write(linesFile1[i])                                 
                                outputOverlapFile.write("\t")                                 
                                outputOverlapFile.write(linesFile2[j])