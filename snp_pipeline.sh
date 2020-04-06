#!/bin/bash

# Place your gatech userame in the below export
export NAME="mgupta313"

usage="Usage: ./snp_pipeline.bash -a <first reads file> -b <second reads file> 
-r <reference genome file> -o <output file> -f <hg38 1000G bundle file> 
-e <for realignment step: improvement> -z <zip output file .vcf.gz> -v <verbose: prints process> 
-i <indexing .bam file> -h <help>
-->>Check if you have .fai and .dict files for reference genome file<<--"

get_input () {
	while getopts "a:b:r:eo:f:zvih" opt
        do
          case $opt in
          a) reads1=$OPTARG;; #first reads file
          b) reads2=$OPTARG;; #second reads file
          r) ref=$OPTARG;; #reference genome file
          o) output=$OPTARG;; #output file
          f) millsFile=$OPTARG;; #location of hg38 1000G bundle file
          e) realign=1;; #realigns file during improvement
          z) gunzip=1;; #zips output file
          v) v=1;; #prints the ongoing step
          i) index=1;; #indexes the output bam file
          h) echo "$usage"; exit 0;; #exit 0 = normal exit, stops the program as user does not want to proceed with the program, just help wanted on how to use the command
          *) echo "INVALID!"; exit 0;;
          esac
        done
}

check_files () {
	# Function for checking for presence of input files, reference genome,
	# and the output VCF file
	#
	# Input: File locations (string)
	# Output: True, if checks pass; False, if checks fail (bool)

	#reads1, reads2, ref, millsFile, output

	if [ "$v" -eq 1 ]; then
		echo "File check"
	fi

        if [ ! -f "$reads1" ]; then
		echo "Can't find reads1 file"
		echo "$usage"
		exit 1 #improper exit, files not found, program can't run
	fi
	
	if [ ! -f "$reads2" ]; then
		echo "Can't find reads2 file"
		echo "$usage"
		exit 1
	fi
	
	if [ ! -f "$ref" ]; then
		echo "Can't find ref file"
		echo "$usage"
		exit 1
	fi

	if [ ! -f "$millsFile" ]; then
		echo "Can't find millsFile file"
 		echo "$usage"
		exit 1
	fi

	if [ -f "$output" ]; then
		echo "Output file exist, overwrite? [y/n]:"
         	read -r answer
		if [ "$answer" != "y" ]; then
			echo "Will not overwrite file"
 			echo "$usage"
			exit -1 #normal exit, user does not want to continue with program
		fi
	fi
}

prepare_temp () {
	# Preparing your temporary directory
	#
	# 
	if [ "$v" -eq 1 ]; then
		echo "Created temporary directory"
	fi

	mkdir tmp1
     	
}


mapping () {
	# Function for the mapping step of the SNP-calling pipeline
	#
	# Input: File locations (string), Verbose flag (bool)
	# Output: File locations (string)

	if [ "$v" -eq 1 ]; then
		echo "Mapping"
	fi
	
	bwa index "$ref"
	bwa mem -R '@RG\tID:foo\tSM:bar\tLB:library1' "$ref" "$reads1" "$reads2" > lane.sam
	samtools fixmate -O bam lane.sam lane_fixmate.bam
	samtools sort -O bam -o lane_sorted.bam -T /tmp/lane_temp lane_fixmate.bam
	bamFile=lane_sorted.bam
	
}

improvement () {
	# Function for improving the number of miscalls
	#
	# Input: File locations (string)
	# Output: File locations (string)

	if [ "$v" -eq 1 ]; then
		echo "Improvement"
	fi
	
	samtools index lane_sorted.bam  lane_sorted.bam.bai
	java -Xmx2g -jar GenomeAnalysisTK.jar -T RealignerTargetCreator -R "$ref" -I lane_sorted.bam -o lane.intervals --known "$millsFile"
	java -Xmx4g -jar GenomeAnalysisTK.jar -T IndelRealigner -R "$ref" -I lane_sorted.bam -targetIntervals lane.intervals -known "$millsFile" -o lane_realigned.bam
	bamFile=lane_realigned.bam
}

call_variants () {
	# Function to call variants
	#
	# Input: File locations (string)
	# Ouput: None

	if [ "$index" -eq 1 ]; then
		samtools index "$bamFile"
	fi

	if [ "$v" -eq 1 ]; then
		echo "Calling Variants"
	fi
	
	if [ "$gunzip" == 1 ]; then
		bcftools mpileup -Ou -f "$ref" "$bamFile" | bcftools call -vmO z -o "$output".gz
	else
		bcftools mpileup -Ou -f "$ref" "$bamFile" | bcftools call -vmO z -o "$output".gz
		gunzip "$output".gz
	fi
	
	mv "$ref".* lane* tmp1/
	mv "$output"* output/
 	
}

main() {
	# Function that defines the order in which functions will be called
	# You will see this construct and convention in a lot of structured code.
	
	# Add flow control as you see appropriate
	get_input "$@"
	check_files "$reads1" "$reads2" "$ref" "$millsFile" "$output"
	prepare_temp
	mapping "$ref" "$reads1" "$reads2"	
	if [ "$realign" -eq 1 ]; then
		improvement "$ref" "$millsFile"
	fi
	call_variants "$ref" "$output"
}

# Calling the main function
main "$@"


# DO NOT EDIT THE BELOW FUNCTION
bats_test (){
    command -v bats
}
# DO NOT EDIT THE ABOVE FUNCTION

