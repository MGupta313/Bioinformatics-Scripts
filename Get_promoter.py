#!/usr/bin/env python3

import re
import sys
import subprocess
from os import listdir
from os.path import isfile, join

input_query = sys.argv[1]
input_subject_dir = sys.argv[2]

input_subject_files = [f for f in listdir(input_subject_dir) if isfile(join(input_subject_dir, f))]
sfile_list=[]
for sfilename in input_subject_files:
	sfile=input_subject_dir+"/"+sfilename
	sfile_list.append(sfile)

subprocess.call(['mkdir', 'pro_align_dir'])
print("Making directory for aligned files of blastn output")
align_file_list = []

for i in range(len(sfile_list)):
	align_file_name=sfile_list[i].split(input_subject_dir+"/")[1].replace(".fasta", "-")+input_query
	align_file_list.append(align_file_name)

print("Blasting the sequences to get the aligned part")
for i in range(len(sfile_list)):
	subprocess.call(['blastn', '-query', input_query, '-subject', sfile_list[i],'-out', align_file_list[i] ,'-outfmt', '6'])
	subprocess.call(['mv', align_file_list[i], 'pro_align_dir'])

input_align_files = [f for f in listdir('pro_align_dir') if isfile(join('pro_align_dir', f))]

def get_promoter(file_in):
	promoter_seq=""
	with open("./pro_align_dir/"+file_in) as f:
		line=f.readlines()
		if len(line) > 0:
			line=line[0].split("\t")
			start_pt=int(line[8])-1
			end_pt=int(line[9])
			genome_filename=file_in.split("-")[0]+".fasta"
			
			with open(input_subject_dir+"/"+genome_filename) as f1:
				next(f1)
				lines=f1.readlines()
				lines=''.join(lines)
				f1_lines=lines.replace('\n', '')
				promoter_seq=f1_lines[start_pt-432:start_pt]
			
			with open("Promoter_multi.fasta", 'a+') as fo:
				fo.write(">"+genome_filename+'\n')
				fo.write(promoter_seq+"\n")
		else:
			pass
			

print("Creating multifasta file for promoter sequences")
for i in range(len(input_align_files)):
	get_promoter(input_align_files[i])