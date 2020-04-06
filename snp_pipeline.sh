#!/bin/bash

#export NAME="mgupta313"

get_input () {
	# Function for doing your getopts
	#
	# Input: Getopts array

	usage="Usage: This program is for calling the variants such as indels and snps present in a sample sequence.

./snp_pipeline.bash [-options]...[arguements]

Commands:

-a read input reads1 file, format .fq
-b read input reads2 file, format fq
-r read the reference genome file, format .fa
-e realigning the mapping file
-o give name for the output file
-f read the mills file for realignment
-z output file as .vcf or .vcf.gz
-v verbose
-i index the file

This program first maps the paired reads file with respect to the given reference file. The output file can be improved upon realigning it using GenomeAnalysisTK. It depends on user's choice if he/she wants to improve the mapped file or not. Then after mapping, the file used to call the variants present in it. bcftools is used to carry out this step, where it identifies indels and snps using the intervals file."

	while getopts "a:b:r:o:f:ezvih" opt
		do
			case "$opt" in
			a) reads1=$OPTARG;; #stores in first input reads file
			b) reads2=$OPTARG;; #stores in second input reads file
			r) ref=$OPTARG;; #stores in the reference file
			e) realign=1;; #if status of option '-e' is 1 then realignement takes place; if status of option '-e' is 0 then no realignment takes place
			o) output=$OPTARG;; #stores the output VCF file
			f) millsFile=$OPTARG;; #stores the Mills indel file
			z) gunzip=1;; #if status of'-z' is 1 then gunzip the output vcf file; if 0 then no gunzip
			v) v=1;; #stores the status for verbose mode as 1 or 0 to print each command/instruction to tell the user what the script is doing right now
			i) index=1;; #if status of '-i' is 1 then index the file using samtools; if status is 0 then don't index the file
			h) echo "$usage";;
			:) echo "Option -$OPTARG requires an arguement";;
			\?) echo "Invalid option - $OPTARG";;
			esac
		done
}

check_files () {
	# Function for checking for presence of input files, reference genome,
	# and the output VCF file
	#
	# Input: File locations (string)
	# Output: True, if checks pass; False, if checks fail (bool)

	if [[ "$v" == "1" ]]; then
		echo "checking files"
	fi

	# to check if the first reads file is given by the user or not
	if [[ -f $reads1 ]]; then 
		echo "Reads1 file exists"
	else
		echo "Reads1 file doesn't exist. Please input reads1 file."
		exit 1
	fi

	# to check if the second reads file is given by the user or not
	if [[ -f $reads2 ]]; then 
		echo "Reads2 file exists"
	else
		echo "Reads2 file doesn't exist. Please input reads2 file."
		exit 1
	fi

	#to check if the reference file is given by the user or not
	if [[ -f $ref ]]; then 
	    echo "Reference file exists"
	else
	    echo "Reference file doesn't exist. Please input reference file."
	    exit 1
	fi

	#to check if an output vcf file already exists
	if [[ -f $output ]]; then 
		echo "Output File already exists. Do you want to overwrite it? (y/n): "
		read -r answer
		if [ "$answer" == "n" ]; then
			echo "Will not overwrite"  
			exit -1
	       	fi
	else
		echo "Output File doesn't exist"
	fi

	#to check if Millsfile is present or not
	#if [[ -f $millsFile ]]; then
	 #   echo "Mills File exists"
	#else
	 #   echo "Mills File doesn't exist"
	  #  exit 1
	#fi

}

prepare_temp () {
	# Preparing your temporary directory
	#
	# 

mkdir -p ./tmp
if [ "$v" == "1" ]; then
    echo "made tmp dir"
fi

cp "$ref" tmp/ref.fa #the original refernce file and its derivations should all be in the same folder
}


mapping () {
	# Function for the mapping step of the SNP-calling pipeline
	#
	# Input: File locations (string), Verbose flag (bool)
	# Output: File locations (string)

	if [ "$v" == 1 ]; then
	echo "Starting the mapping process"
	fi

	bwa index "$ref" 

	bwa mem -R '@RG\tID:foo\tSM:bar\tLB:library1' "$ref" "$reads1" "$reads2" > ./tmp/"$output.sam"

	#making some changes in the ./tmp/$output.sam file
	samtools fixmate -O bam ./tmp/"$output.sam" ./tmp/"$output.fixmate.bam" #if $output_fixmate.bam is used instaed of $output.fixmate.bam then $output_fixmate becomes a whole new variable

	samtools sort -O bam -o ./tmp/"$output.sorted.bam" -T ./tmp/"$output.temp" ./tmp/"$output.fixmate.bam"
	
	bamfile=./tmp/"$output.sorted.bam" #now instead of using different bam files, $bamFile var could be used
	
}
#improvement () {
	# Function for improving the number of miscalls
	#
	# Input: File locations (string)
	# Output: File locations (string)


 # if [ "$realign" == "1" ]; then
	
#	if [ "$v" == 1 ]; then
#	echo "Completed the mapping process. Starting improvement process."
#	fi

#	if [ "$v" == 1 ]; then
#	echo "Indexing the reference file."
#	fi
#	samtools faidx ./tmp/ref.fa

#	if [ "$v" == 1 ]; then
#	echo "Creating a dictionary file for the reference file."
#	fi
      
#	java -jar ./lib/picard.jar CreateSequenceDictionary R=./tmp/ref.fa O=./tmp/ref.dict

	#indexing the $bamfile becuase it is requirement for the improvement command.
#	samtools index "$bamfile"
	
#	if [ "$v" == 1 ]; then
#	echo "Creating the intervals file."
#	fi
#	java -Xmx2g -jar ./lib/GenomeAnalysisTK.jar -T RealignerTargetCreator -R ./tmp/ref.fa -I ./tmp/"$output.sorted.bam" -o ./tmp/"$output.intervals" --known "$millsFile"
	#intervals file gives the information where all could the indels and snps be in the reads files when compared with the reference file

#	if [ "$v" == 1 ]; then
#	echo "Realigning the data."
#	fi
#	java -Xmx4g -jar ./lib/GenomeAnalysisTK.jar -T IndelRealigner -R ./tmp/ref.fa -I ./tmp/"$output.sorted.bam" -targetIntervals ./tmp/"$output.intervals" -known "$millsFile" -o ./tmp/"$output.realigned.bam"
#	bamfile=./tmp/"$output.realigned.bam"

#	if [ "$v" == 1 ]; then
#	echo "Indexing the file."
#	fi
	
#	if [ "$index" == "1" ]; then
#	    samtools index "$bamfile"
#	fi
 # fi
#}

call_variants () {
	# Function to call variants
	#
	# Input: File locations (string)
	# Ouput: None

	if [ "$v" == 1 ]; then
	echo "Improvement is done. Calling the variants now."
	fi

	if [ "$gunzip" == "1" ]; then
	    bcftools mpileup -Ou -f ./tmp/ref.fa "$bamfile" | bcftools call -vmO z -o ./output/"$output.vcf.gz"	    
	else
	bcftools mpileup -Ou -f ./tmp/ref.fa "$bamfile" | bcftools call -vmO -o ./output/"$output.vcf"
	fi

	if [ "$v" == 1 ]; then
	echo "Variant calling is done."
	fi

	tabix -p vcf $"output.vcf.gz"
	#if [ "$v" == 1 ]; then
	#echo "Converting .vcf file to .bed file"
	#fi
	#gunzip "$output.vcf.gz"
	#sed -e 's/chr//' ./output/"$output.vcf" | awk '{OFS="\t"; if (!/^#/){print $1,$2,$2+length($5)-length($4),length($5)-length($4)}}' > ./output/"$output.bed"
	
}

main() {
	# Function that defines the order in which functions will be called
	# You will see this construct and convention in a lot of structured code.
	
	# Add flow control as you see appropriate
	get_input "$@"
	check_files # Add arguments here
	prepare_temp
	mapping # Add arguments here
	#improvement # Add arguments here
	call_variants # Add arguments here
}

# Calling the main function
main "$@"


# DO NOT EDIT THE BELOW FUNCTION
bats_test (){
    command -v bats
}
# DO NOT EDIT THE ABOVE FUNCTION
