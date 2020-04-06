#!/usr/bin/env python3

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-a",help="Enter the first genome file")
parser.add_argument("-b",help="Enter the second genome file")
parser.add_argument("-d",help="Enter the directory containing input genome files")
parser.add_argument("-s",help="Enter the number of random kmers to evaluate")
parser.add_argument("--seed",help="Enter seed value for random generation")
parser.add_argument("-o",help="name of output file")
parser.add_argument("-t",help="Enter the number of threads to run analysis")
parser.add_argument("-f",help="overwrite files if they exist")
args = parser.parse_args()