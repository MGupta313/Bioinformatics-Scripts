#!/usr/bin/env python3

import sys
from os import listdir
from os.path import isfile, join
import subprocess
import re

input_reg_dir=sys.argv[1]
input_genome_dir=sys.argv[2]


input_reg_files = [f for f in listdir(input_reg_dir) if isfile(join(input_reg_dir, f))]
rfile_list=[]
for rfilename in input_reg_files:
	rfile=input_reg_dir+"/"+rfilename
	rfile_list.append(rfile)
#print(rfile_list)

input_genome_files = [f for f in listdir(input_genome_dir) if isfile(join(input_genome_dir, f))]
gfile_list=[]
for gfilename in input_genome_files:
	gfile=input_genome_dir+"/"+gfilename
	gfile_list.append(gfile)
#print(gfile_list)


subprocess.call(['mkdir', 'strand_dir'])
subprocess.call(['mkdir', 'align_dir'])

print("Making directories for strand files and aligned files of blastn output")

strand_file_list = []
align_file_list = []
for i in range(len(gfile_list)):
	for j in range(len(rfile_list)):
		strand_file_name=gfile_list[i].split(input_genome_dir+"/")[1].replace(".fasta", "-")+rfile_list[j].split(input_reg_dir+"/")[1].replace(".fasta", ".txt")
		strand_file_list.append(strand_file_name)
		align_file_name=gfile_list[i].split(input_genome_dir+"/")[1].replace(".fasta", "-")+rfile_list[j].split(input_reg_dir+"/")[1]
		align_file_list.append(align_file_name)

#print(strand_file_list)

#print(align_file_list)


print("Blasting the sequences to get the aligned part")

for i in range(len(gfile_list)):
	for j, k in zip(range(len(rfile_list)), range(6*(i), 6*(i+1)+1)):
		print('blastn', '-query', rfile_list[j], '-subject', gfile_list[i],'-out', strand_file_list[k] ,'-outfmt', '6 sstrand')

		subprocess.call(['blastn', '-query', rfile_list[j], '-subject', gfile_list[i],'-out', strand_file_list[k] ,'-outfmt', '6 sstrand'])
		subprocess.call(['mv', strand_file_list[k], 'strand_dir'])
		subprocess.call(['blastn', '-query', rfile_list[j], '-subject', gfile_list[i],'-out', align_file_list[k] ,'-outfmt', '6 sseq'])
		subprocess.call(['mv', align_file_list[k], 'align_dir'])


input_strand_files=[f for f in listdir('strand_dir') if isfile(join('strand_dir', f))]

input_align_files = [f for f in listdir('align_dir') if isfile(join('align_dir', f))]

#subprocess.call(["mkdir", "multifasta_dir"])

def write_in_file(file_input):
	with open("./align_dir/"+file_input) as f2:
		lines=f2.readlines()
		seq=lines[0].replace('\n', '')		
		out_filename = file_input.replace(".fasta","-align.fasta")
		if re.search(pattern="CytR", string=out_filename):
			output_filename = file_input.split("-")[1].replace(".fasta", "-multiseq.fasta")
		elif re.search(pattern="HapR", string=out_filename):
			output_filename = file_input.split("-")[1].replace(".fasta", "-multiseq.fasta")
		elif re.search(pattern="QstR", string=out_filename):
			output_filename = file_input.split("-")[1].replace(".fasta", "-multiseq.fasta")
		elif re.search(pattern="TfoX", string=out_filename):
			output_filename = file_input.split("-")[1].replace(".fasta", "-multiseq.fasta")
		elif re.search(pattern="TfoY", string=out_filename):
			output_filename = file_input.split("-")[1].replace(".fasta", "-multiseq.fasta")
		elif re.search(pattern="LuxO", string=out_filename):
			output_filename = file_input.split("-")[1].replace(".fasta", "-multiseq.fasta")
	with open(output_filename, 'a+') as fo:
		fo.write(">"+out_filename+'\n')
		fo.write(seq+"\n")
		subprocess.call(["mv", output_filename, "multifasta_dir"])
		
print("Creating multifasta files for all 5 regulators: CytR, HapR, QstR, TfoX, TfoY, LuxO")

line_list=[]
for i in range(len(input_strand_files)):
	with open("./strand_dir/"+input_strand_files[i]) as sf:
		line= sf.readline()
		line_list.append(line)
		if len(line_list[i]) > 0:
			line_list[i]=line_list[i].rstrip()
			file_for_msa = input_strand_files[i].replace(".txt", ".fasta")
			write_in_file(file_for_msa)
		elif len(line_list[i]) == 0:
			pass