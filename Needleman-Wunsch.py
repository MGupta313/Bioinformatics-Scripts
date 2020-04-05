#!/usr/bin/env python3

# Write your code here


#Reading of input files
import sys
with open(sys.argv[1],'r') as sequence1:
	sequence1string=''
	for line in sequence1:
		if not line.startswith('>'):
			sequence1string+=line.rstrip()
		
with open(sys.argv[2],'r') as sequence2:
	sequence2string=''
	for line in sequence2:
		if not line.startswith('>'):
			sequence2string+=line.rstrip()


#Construction of the matrix with all zeros	
matrix=[]		
for row in range(len(sequence2string)+2):
	j=[]
	matrix.append(j)

for column in range(len(sequence1string)+2):
	for row in range(len(sequence2string)+2):
		i=0
		matrix[row].append(i)



#Initialilization of Matrix with sequence 1 and sequence 2 on horizontal and vertical axis
for column in range(2,(len(matrix[0]))):
		matrix[0][column]=sequence1string[column-2]	
#print('Length of sequence1string is',len(sequence1string))	
#print('No of columns are ',len(matrix[0]))
#print('Sequence1 is ',sequence1string)	
for row in range(2,len(matrix)):
	matrix[row][0]=sequence2string[row-2]	
#print('No of rows are ',len(matrix))
#print('Length of sequence2string is',len(sequence2string))
#print('Sequence2 is', sequence2string)
	

#Matrix filling 

matrix[0][0]=matrix[0][1]=matrix[1][0]=''
for row in range(1,len(matrix)):
	for column in range(1,len(matrix[0])):
		if row==1 and column==1:
			matrix[row][column]==0
		elif row==1:
			matrix[1][column]=matrix[1][column-1]-1
		elif column==1:
			matrix[row][1]=matrix[row-1][1]-1
		else:
			if matrix[row][0]==matrix[0][column]:
				matrix[row][column]=max((matrix[row][column-1]-1),(matrix[row-1][column]-1),(matrix[row-1][column-1]+1))
			else:
				matrix[row][column]=max((matrix[row][column-1]-1),(matrix[row-1][column]-1),(matrix[row-1][column-1]-1))

#print(matrix)

        
#Backtracking

numberOfRows=len(matrix)
numberOfColumns=len(matrix[0])
currentRow=len(matrix)-1
currentColumn=len(matrix[0])-1
#highlightedElement=matrix[len(matrix)-1][len(matrix[0])-1]
seq1,seq2=[],[]
alignmentScore=matrix[len(matrix)-1][len(matrix[0])-1]
def main(currentRow,currentColumn):
	print(currentRow,currentColumn)
	x=1
	if currentRow==currentColumn==1:
		x=0
	elif (x!=0) and (currentColumn==1):
		if matrix[currentRow][currentColumn]==(matrix[currentRow-1][currentColumn]-1):
			highlightedElement=matrix[currentRow-1][currentColumn] #if highlighted element is a part of 1st row or 1st column it will always be backtracked to the element to the left of it and utop of it respectively
			print(highlightedElement)
			seq1.append('-')
			seq2.append(matrix[currentRow][0])
			currentRow,currentColumn=currentRow-1,currentColumn #current row and current column values are changed to the row and column of the new highlighted element
			return main(currentRow,currentColumn)
	elif x!=0 and currentRow==1:
		if matrix[currentRow][currentColumn]==matrix[currentRow][currentColumn-1]-1:
			highlightedElement=matrix[currentRow][currentColumn-1]
			print(highlightedElement)
			seq1.append(matrix[0][currentColumn])
			seq2.append('-')
			currentRow,currentColumn=currentRow,currentColumn-1
			return main(currentRow,currentColumn)
	elif x!=0:
		if ((matrix[currentRow][currentColumn]==(matrix[currentRow-1][currentColumn-1]+1)) and (matrix[currentRow][0]==matrix[0][currentColumn])):
			highlightedElement=matrix[currentRow-1][currentColumn-1] 
			print(highlightedElement)
			seq1.append(matrix[0][currentColumn])       
			seq2.append(matrix[currentRow][0])
			currentRow,currentColumn=currentRow-1,currentColumn-1
			return main(currentRow,currentColumn)
		elif ((matrix[currentRow][currentColumn]==(matrix[currentRow-1][currentColumn-1]-1)) and (matrix[currentRow][0]!=matrix[0][currentColumn])):
			highlightedElement=matrix[currentRow-1][currentColumn-1] 
			print(highlightedElement)
			seq1.append(matrix[0][currentColumn])
			seq2.append(matrix[currentRow][0])
			currentRow,currentColumn=currentRow-1,currentColumn-1
			return main(currentRow,currentColumn)
		elif (matrix[currentRow][currentColumn]==(matrix[currentRow-1][currentColumn]-1)):
			highlightedElement=matrix[currentRow-1][currentColumn]
			print(highlightedElement)
			seq1.append('-')
			seq2.append(matrix[currentRow][0])
			currentRow,currentColumn=currentRow-1,currentColumn
			return main(currentRow,currentColumn)
		elif (matrix[currentRow][currentColumn]==(matrix[currentRow][currentColumn-1]-1)):
			highlightedElement=matrix[currentRow][currentColumn-1]
			print(highlightedElement)
			seq1.append(matrix[0][currentColumn])
			seq2.append('-')
			currentRow,currentColumn=currentRow,currentColumn-1
			return main(currentRow,currentColumn)
while currentRow!=1 and currentColumn !=1:
	if currentColumn==1:
		if matrix[currentRow][currentColumn]==(matrix[currentRow-1][currentColumn]-1):
			highlightedElement=matrix[currentRow-1][currentColumn] #if highlighted element is a part of 1st row or 1st column it will always be backtracked to the element to the left of it and utop of it respectively
			#print(highlightedElement)
			seq1.append('-')
			seq2.append(matrix[currentRow][0])
			currentRow=currentRow-1 #current row and current column values are changed to the row and column of the new highlighted element
	elif currentRow==1:
		if matrix[currentRow][currentColumn]==matrix[currentRow][currentColumn-1]-1:
			highlightedElement=matrix[currentRow][currentColumn-1]
			#print(highlightedElement)
			seq1.append(matrix[0][currentColumn])
			seq2.append('-')
			currentColumn=currentColumn-1
	else:
		if ((matrix[currentRow][currentColumn]==(matrix[currentRow-1][currentColumn-1]+1)) and (matrix[currentRow][0]==matrix[0][currentColumn])):
			highlightedElement=matrix[currentRow-1][currentColumn-1] 
			#print(highlightedElement)
			seq1.append(matrix[0][currentColumn])       
			seq2.append(matrix[currentRow][0])
			currentRow,currentColumn=currentRow-1,currentColumn-1
		elif ((matrix[currentRow][currentColumn]==(matrix[currentRow-1][currentColumn-1]-1)) and (matrix[currentRow][0]!=matrix[0][currentColumn])):
			highlightedElement=matrix[currentRow-1][currentColumn-1] 
			#print(highlightedElement)
			seq1.append(matrix[0][currentColumn])
			seq2.append(matrix[currentRow][0])
			currentRow,currentColumn=currentRow-1,currentColumn-1
		elif (matrix[currentRow][currentColumn]==(matrix[currentRow-1][currentColumn]-1)):
			highlightedElement=matrix[currentRow-1][currentColumn]
			#print(highlightedElement)
			seq1.append('-')
			seq2.append(matrix[currentRow][0])
			currentRow,currentColumn=currentRow-1,currentColumn
		elif (matrix[currentRow][currentColumn]==(matrix[currentRow][currentColumn-1]-1)):
			highlightedElement=matrix[currentRow][currentColumn-1]
			#print(highlightedElement)
			seq1.append(matrix[0][currentColumn])
			seq2.append('-')
			currentRow,currentColumn=currentRow,currentColumn-1
			




			
			
			
			
			


#main(currentRow,currentColumn)	
#print(seq1)
#print(seq2)	
seq1string=''
seq2string=''
for i in range((len(seq1)-1),-1,-1):
	seq1string+=seq1[i]

for j in range((len(seq2)-1),-1,-1):
	seq2string+=seq2[j]

lines=''
for index in range(len(seq1string)):
	if seq1string[index]==seq2string[index]:
		lines+='|'
	else:
		seq1string[index]!=seq2string[index]
		lines+=' '

print(seq1string)
print(lines)
print(seq2string)
print('Alignment score:',alignmentScore)



			
			


					


	



 	



	
