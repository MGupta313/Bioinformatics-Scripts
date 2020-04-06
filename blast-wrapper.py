#!/usr/bin/env python3

'''
Define different blast wrapper functions here.
'''

# Add your code here

import subprocess


def makedb (databasetype, databaseinputfile):
    if databasetype == "n":
        subprocess.run(['makeblastdb', '-dbtype', 'nucl', '-in', databaseinputfile])
    elif databasetype == "p":
        subprocess.run(['makeblastdb', '-dbtype', 'nucl', '-in', databaseinputfile])    

def blast (databasetype, queryinputfile, databasefile, blastoutput):
    if databasetype == 'n':
        subprocess.run(['blastn', '-query', queryinputfile, '-db', databasefile, '-out', blastoutput, '-evalue', '0.05', '-outfmt', '10', '-max_target_seqs', '1'])
    elif databasetype == 'p':
        subprocess.run(['blastn', '-query', queryinputfile, '-db', databasefile, '-out', blastoutput, '-evalue', '0.05', '-outfmt', '10', '-max_target_seqs', '1'])
