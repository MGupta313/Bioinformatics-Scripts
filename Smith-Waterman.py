#!/usr/bin/env python

#Smith Waterman Algo

import sys

#open both files and read the sequences
with open(sys.argv[1],'r') as file1:
    next(file1)
    for line in file1:
        seq1 = line
        print(seq1)
        m=len(seq1)+1 #plus one to add row for gap penalties

with open(sys.argv[2],'r') as file2:
    next(file2)
    for line in file2:
        seq2 = line
        print(seq2)
        n=len(seq2)+1 #plus one to add column for gap penalties
    
    
#initializing an alignment matrix and a pointer matrix
alignMat = []
for row in range(n):
    j=[]
    alignMat.append(j)
for column in range(m):
    for row in range(n):
        i=0
        alignMat[row].append(i)
pointer = []
for row in range(n):
    j=[]
    pointer.append(j)
for column in range(m):
    for row in range(n):
        i=0
        pointer[row].append(i)

#adding gap penalties to the first row and column of the alignemnt matrix
for i in range(n):
    alignMat[i][0] = 0*i #for first column
for j  in range(m):
    alignMat[0][j] = 0*j #for first row

#checking for match/mismatch
def match(b1, b2):
    if b1 == b2:
        score = 1 #match score = 1
        return score
    else:
        score = -1 #mismatch score = -1
        return score


#filling up the cells using the surrounding 3 cells
max_score = 0
for i in range(1,n):
    for j in range(1,m):
        diag = alignMat[i-1][j-1] + match(seq1[j-1],seq2[i-1])
        up = alignMat[i-1][j] -1       #gap penalty = -1
        left = alignMat[i][j-1] -1     #gap penalty = -1
        alignMat[i][j] = max(0,diag,left,up) #maximum of the scores from the surrounding 3 cells goes into the current cell
       # if diag == up:
        #    alignMat[i][j] == diag
       # if up == left:
        #    alignMat[i][j] == up
            
        if alignMat[i][j] == diag:
            pointer[i][j] = 1
        elif alignMat[i][j] == up:
            pointer[i][j] = 2
        elif alignMat[i][j] == left:
            pointer[i][j] = 3
        elif alignMat[i][j] == 0:
            pointer[i][j] = 0
        if alignMat[i][j] >=max_score:
            max_i = i
            max_j = j
            max_score = alignMat[i][j] #backtracking starts from the cell with max score

#backtracking

align1, align2 = "", "" #initial alignment
i = max_i
j = max_j

while pointer[i][j] != 0: #backtracking/alignment is continued till a cell containing zero is encountered
    if pointer[i][j] == 1: #1 is for diag
        align1 = align1 + seq1[j-1]
        align2 = align2 + seq2[i-1]
        i = i -1
        j = j -1
    elif pointer[i][j] == 2: #2 is for up
        align1 = align1 + "-"
        align2 = align2 + seq2[i-1]
        i = i -1
    elif pointer[i][j] == 3: #3 is for left
        align1 = align1 + seq1[j-1]
        align2 = align2 + "-"
        j = j -1

#formatting the alignment
align3 = ""
for i in range(len(align1)):
    if align1[i] == align2[i]:
        align3 = align3 + "|"
    else:
        align3 = align3 + " "

align1 = align1[::-1]
align2 = align2[::-1]
align3 = align3[::-1]
print(align1)
print(align3)
print(align2)
print("Alignement score =", max_score)