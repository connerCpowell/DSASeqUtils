#!/usr/bin/env python

usage = """
Michael Alonge
analyze_ambiguity.py
6.2.16
Driscolls
___________
Description:

This command line utility takes a sequences file, and reports various metrics
regarding the ambiguity codes therein.

_____
Usage:

python analyze_ambiguity.py [options] -f <sequence file>

    flags:

    -f      ------------------- Sequence file for which ambiguity code analysis is desired.


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

ambiguity_codes = {
    "Y",
    "R",
    "W",
    "S",
    "K",
    "M",
    "D",
    "V",
    "H",
    "B",
}

# Iterate through each sequence and get ambiguity code info.
# For now, I will just get a per3centage of nucleotides that are
# ambiguous, and their genomic coordinates.

# In the future, maybe report number per sequence, and frequency of each code.
total = 0
total_ambiguity = 0
x = SeqReader(input_file)
if using_fastas:
    for header, sequence in x.parse_fasta():
        total += len(sequence)
        # The following should be optimized. Maybe use a mapping or regex?
        for code in ambiguity_codes:
            total_ambiguity += sum(map(sequence.count, ambiguity_codes))

else:
    for read in x.parse_fastq():
        total += len(read[1])
        for code in ambiguity_codes:
            total_ambiguity += sum(map(read[1].count, ambiguity_codes))

print 'The total number of nucleotides is %r' %total
print 'The total number of ambiguous nucleotides is %r' %total_ambiguity

