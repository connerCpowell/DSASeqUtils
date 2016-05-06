#!/usr/bin/env

usage = """
Michael Alonge
get_fasta_sequence.py
5.3.16
Driscolls
___________
Description:

This command line utility takes a sequences file, and output sequences
of that file that are longer than a specified length.

_____
Usage:

python filter_lengths.py [options] -f <sequence file> -c <length cutoff>

    flags:

    -f      ------------------- Fasta file from which a sequence is desired.
    -c      ------------------- The header of the sequence desired.


    OPTIONS:

    -h, --help   -------------- Display help message.
    -a           -------------- Input file is in fasta format.
    -q           -------------- Input file is in fastq format.
"""
import sys

from utils.SeqReader import SeqReader
from utils.utilities import get_flag
from utils.utilities import help_desired

# Get command line args
if help_desired(sys.argv):
    sys.exit(usage)

# Get the sequence file.
input_file = get_flag(sys.argv, '-f', usage)

# Get the cutoff length.
cutoff = get_flag(sys.argv, '-c', usage)
try:
    cutoff = int(cutoff)
except ValueError():
    raise ValueError('Length cutoff must be an integer.')

# Check if the input file is in fasta or fastq format.
if '-a' in sys.argv and '- q' not in sys.argv:
    using_fastas = True
elif '-q' in sys.argv and '-a' not in sys.argv:
    using_fastas = False
elif '-q' in sys.argv and '-a' in sys.argv:
    raise ValueError(
        "'-a' and '-q' flag cannot be specified together. File must be either fasta or fastq format."
    )
else:
    raise ValueError(
        "A '-a' or '-q' flag must be specified. This specifies fasta or fastq file format."
    )

# Iterate through the sequence file and write sequence to standard output
# if the sequence is longer than the specified cutoff length.
x = SeqReader(input_file)
if using_fastas:
    for header, sequence in x.parse_fasta():
        if len(sequence) > cutoff:
            print header
            print sequence
else:
    for read in x.parse_fastq():
        if len(read[1]) > cutoff:
            for i in read:
                print i

