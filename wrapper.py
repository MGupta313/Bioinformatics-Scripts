#!/usr/bin/env python3
import os

def makedatabase(databasetype, databaseinputfile):
    os.system('makeblastdb -dbtype databasetype -in inputfile')

def blast(databasetype, queryinputfile, databaseoutputfile, evaluenum):
    if databsetype == 'nucl':
        os.system('blastn -query queryinputfile -db databaseoutputfile -evalue evaluenum')
    elif databsetype == 'prot':
        os.system('blastp -query queryinputfile -db databaseoutputfile -evalue evaluenum')
    
