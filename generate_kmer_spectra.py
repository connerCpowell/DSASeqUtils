__author__ = 'malonge'
import collections
from datetime import datetime
import argparse

from dsa_seq_utils.SeqReader import SeqReader
from dsa_seq_utils.utilities import kmerize

desc = """
Given a list of sequence files and a k value, return the kmer spectra information.
"""
parser = argparse.ArgumentParser(description="")
parser.add_argument('file_list', type=str, metavar="<file_list.txt>", help='A single column text file containing all the files names to be processed.')
parser.add_argument('k', type=int, metavar='k', help='The length of kmers for kmer spectra.')
parser.add_argument('--fastq', dest='using_fastq', action='store_true', help='Specify for use of fastq files. Uses fasta by default.')

args = parser.parse_args()
file_list = args.file_list
k = args.k
using_fastq = args.using_fastq

# Initialize the trie data structure used to store the kmer spectra information.
kmer_counts = {}

# Iterate through the sequence file and kmerize each sequence.
with open(file_list) as f:
    for line in f:
        x = SeqReader(line.rstrip())
        if using_fastq:
            # Use the fastq sequence generator
            for header, seq, plus, qual in x.parse_fastq():
                for kmer in kmerize(seq, k):
                    if kmer in kmer_counts:
                        kmer_counts[kmer] += 1
                    else:
                        kmer_counts[kmer] = 1

        else:
            # Use the fasta sequence generator
            for header, seq in x.parse_fasta():
                for kmer in kmerize(seq, k):
                    if kmer in kmer_counts:
                        kmer_counts[kmer] += 1
                    else:
                        kmer_counts[kmer] = 1

counter = collections.Counter(kmer_counts.values())
with open('unique_kmer_frequency.txt', 'w') as out_file:
    for i in counter.keys():
        out_file.write("%r\t%r\n" % (i, counter[i]))