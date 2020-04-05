#!/usr/bin/env python3
#
# Your code here
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i1",help="enter the first file")
parser.add_argument("-i2",help="enter the second file")
parser.add_argument("-m",type=float,help="enter minimum percent overlap")
parser.add_argument("-j", action="store_true",
                    help="allows to print member of the first set and the member of the second set that it overlaps with on the same line")
parser.add_argument("-o",help="name of output file")
args = parser.parse_args()

chromosome_file_one=[]
fragments_file_one=[]
chromosome_fragment=[]
with open(args.i1,'r') as file_one:
    for line in file_one:
        line=line.rstrip()
        line=line.split("\t")
        if line[0] not in chromosome_file_one:
            chromosome_file_one.append(line[0])
            if len(chromosome_fragment)!=0:
                fragments_file_one.append(chromosome_fragment)
                chromosome_fragment=[]
        chromosome_fragment.append(line)
    fragments_file_one.append(chromosome_fragment)


    
chromosome_file_two=[]
fragments_file_two=[]
chromosome_fragment=[]
with open(args.i2,'r') as file_two:
    for line in file_two:
        line=line.rstrip()
        line=line.split("\t")
        if line[0] not in chromosome_file_two: 
            chromosome_file_two.append(line[0])
            if len(chromosome_fragment)!=0:
                fragments_file_two.append(chromosome_fragment)
                chromosome_fragment=[]
        chromosome_fragment.append(line)
    fragments_file_two.append(chromosome_fragment)
        
duplicate_output_list=[]
with open(args.o,'w') as output_file:
        t=0 
        fragment_overlap=[]
        for j in range(len(fragments_file_one[i])):
            print("at {}th fragment of {}th chromosome in file one".format(j,i))
            flag_overlap=0
            flag_t=0
            for k in range(t,len(fragments_file_two[i])):
                print("comparing {}th fragment of file one with {}th fragment of {}th chromosome in file two".format(j,k,i))

                if int(fragments_file_one[i][j][1])>int(fragments_file_two[i][k][2]):
                    continue
                else:
                    minimum=min(int(fragments_file_one[i][j][2]),int(fragments_file_two[i][k][2]))
                    #print(int(fragments_file_one[i][j][2]))
                    #print(int(fragments_file_two[i][k][2]))
                    #print(minimum)
                    maximum=max(int(fragments_file_one[i][j][1]),int(fragments_file_two[i][k][1]))
                    #print(int(fragments_file_one[i][j][1]))
                    #print(int(fragments_file_two[i][k][1]))
                    #print(maximum)
                    overlap=minimum-maximum
                    if flag_t!=1:
                        t=k
                        flag_t=1
                    if overlap<=0:
                        break
                    else:
                        print(overlap)
                        length=int(fragments_file_one[i][j][2])-int(fragments_file_one[i][j][1])
                        print(length)
                        percent_overlap=(overlap/length)*100
                        print((percent_overlap))
                        if percent_overlap>=args.m:
                            if args.j:
                                with open(args.o,'a') as output_file:
                                    output_file.write(fragments_file_one[i][j][0])
                                    output_file.write("\t")
                                    output_file.write(fragments_file_one[i][j][1])
                                    output_file.write("\t")
                                    output_file.write(fragments_file_one[i][j][2])
                                    output_file.write("\t\t")
                                    output_file.write(fragments_file_two[i][k][0])
                                    output_file.write("\t")
                                    output_file.write(fragments_file_two[i][k][1])
                                    output_file.write("\t")
                                    output_file.write(fragments_file_two[i][k][2])
                                    output_file.write("\n")
                            else:
                                duplicate_output_list.append(fragments_file_one[i][j][0]+fragments_file_one[i][j][1]+fragments_file_one[i][j][2])

                                    
unique_output_list=[]
if not args.j:
    for unique in duplicate_output_list:
        if unique not in unique_output_list:
            unique_output_list.append(unique)


                    
                    

                    

                    
            
            
                

    
    
        

    
        







                                    
                                    
                                    

                                    









