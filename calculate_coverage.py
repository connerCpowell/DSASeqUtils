#!/usr/bin/env python
from __future__ import division

import sys

from dsa_seq_utils.SeqReader import SeqReader
from dsa_seq_utils.stats import calculate_mean
from dsa_seq_utils.stats import calculate_pop_sd
from dsa_seq_utils.utilities import get_flag
from dsa_seq_utils.utilities import help_desired
from dsa_seq_utils.utilities import log

usage = """
Michael Alonge
calculate_coverage.py
5.3.16
Driscolls
___________
Description:

This command line utility calculates genome coverage given a set of fasta
or fastq files. This is not a utility that makes use of mapping information to
report precise coverage information. Rather, this tool reports a theoretical
global genome coverage given an expected genome size.

_____
Usage:

python calculate_coverage [options] -s <genome size> <fastq/fasta file(s)>

    flags:

    -s       ------------------- Genome size in bp. e.g. 1 Mb genome = 1000000


    OPTIONS:

    -h, --help      ------------ Display help message.
    --hist          ------------ Write a read length histogram file to current working directory.
    -a              ------------ Input files are in fasta format.
    -q              ------------ Input files are in fastq format.

"""

# Get command line args
if help_desired(sys.argv):
    sys.exit(usage)

genome_size = get_flag(sys.argv, '-s', usage)
try:
    genome_size = int(genome_size)
except ValueError():
    raise ValueError('Genome size must be an integer.')

if '-a' in sys.argv and '- q' not in sys.argv:
    using_fastas = True
elif '-q' in sys.argv and '-a' not in sys.argv:
    using_fastas = False
elif '-q' in sys.argv and '-a' in sys.argv:
    raise ValueError(
        "'-a' and '-q' flag cannot be specified together. Files must be either all fasta or all fastq format."
    )
else:
    raise ValueError(
        "A '-a' or '-q' flag must be specified. This specifies fasta or fastq file format."
    )

# Check if a histogram file is desired.
if '--hist' in sys.argv:
    histogram_requested = True
    log("Histogram file requested.")
else:
    histogram_requested = False
    log("Histogram file not requested.")

# Get the list of all fasta or fastq files.
if using_fastas:
    all_files = [
        i for i in sys.argv if
        i.endswith('.fasta') or
        i.endswith('.fa') or
        i.endswith('.fan') or
        i.endswith('.fas')
    ]
    if not all_files:
        raise ValueError(
            "The '-a' option was specified, but no fasta files were found."
        )

else:
    all_files = [
        i for i in sys.argv if
        i.endswith('.fastq') or
        i.endswith('.fq')
    ]
    if not all_files:
        raise ValueError(
            "The '-q' option was specified, but no fastq files were found."
        )

all_seq_lengths = []
for f in all_files:
    log("Processing %s" % f)
    x = SeqReader(f)
    if using_fastas:
        for header, seq in x.parse_fasta():
            all_seq_lengths.append(len(seq))

    else:
        for read in x.parse_fastq():
            all_seq_lengths.append(len(read[1]))

# Write read length histogram file.
if histogram_requested:
    log("Writing read length histogram 'read_lengths.txt'.")
    with open('read_lengths.txt', 'w') as histogram_file:
        for length in sorted(all_seq_lengths):
            histogram_file.write(str(length) + "\n")

log("The coverage for a genome of size %r is %fX." % (genome_size, sum(all_seq_lengths)/genome_size))
log("The average read length is %fbp." % calculate_mean(all_seq_lengths))
log("The read length standard deviation is %fbp." % calculate_pop_sd(all_seq_lengths))



