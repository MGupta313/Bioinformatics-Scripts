#!/usr/bin/env python3

'''
Module to find reciprocal hits in a blast search.
'''
from blast_utilities.blast_wrapper import makedb
from blast_utilities.blast_wrapper import blast


def get_reciprocal_hits(inputfile1, inputfile2, seqtype):
    #creating database for inputfile1
    makedb(seqtype, inputfile1)

    #creating databse for inputfile2
    makedb(seqtype, inputfile2)
    
    #running blast for inputfile1 as a query against file2db
    blast(seqtype, inputfile1, inputfile2, "blastoutputfile1")

    #running blast for inputfile2 as a query against file1db
    blast(seqtype, inputfile2, inputfile1, "blastoutputfile2")

    #comparing the blast hits for reciprocal hits
    with open('blastoutputfile1') as f1:
        dict1={}
        for lines in f1:
            lines=lines.split(",")
            dict1[lines[0]]=lines[1]
            #key1=seq1, val1=hit1

    with open('blastoutputfile2') as f2:
        dict2={}
        for lines in f2:
            lines=lines.split(",")
            dict2[lines[0]]=lines[1]
            #key2=seq2, val2=hit2

    listofrechits=[]
    for key1 in dict1:
        for key2 in dict2:
            if key1 == dict2[key2]:
                listelement=key1+"\t"+key2+"\n"
                listofrechits.append(listelement)
    return listofrechits