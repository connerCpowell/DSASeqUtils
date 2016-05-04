#!/usr/bin/env python
__author__ = 'malonge'

"""
Michael Alonge
SeqReader.py
Bare bones sequence file generators for fasta and fastq files.
e.g.
from SeqReader import SeqReader
x = SeqReader('sequences.fasta')
for header, sequence in x.parse_fasta():
    # Do stuff with header and sequence.

y = SeqReader('reads.fastq')
for read in y.parse_fastq():
    # Each read is a 4 element list.
    # One element for each line of a read.
"""

import sys


class SeqReader:
    """ Defines two generator methods, one for fasta files,
        and one for fastq files. These methods are bare bones,
        and simply provide the raw contents of the file provided.
        parse_fasta() --- fasta parser. Yields header, sequence for each sequence.
        parse_fastq() --- fastq parser. Yields a list of 4 elements per read
                          [header, sequence, '+', quality scores]
    """

    def __init__(self, inFile):
        """ Initialize sequence file to be parsed."""
        self.in_file = inFile

    def parse_fasta (self):
        """ Generator yielding header and sequence, for each sequence
            in the fasta file sent to the class.
        """
        with open(self.in_file) as fasta_file:
            header = ''
            sequence = ''
            # Find first header.
            line = fasta_file.readline()
            while not line.startswith('>'):
                line = fasta_file.readline()
            header = line.rstrip()

            # Get sequence associated with that header.
            for line in fasta_file:
                if line.startswith('>'):
                    # Once the sequence is over, (next header begins),
                    # yield initial header and sequence.
                    yield header,sequence
                    header = line.rstrip()
                    sequence = ''
                else:
                    sequence += ''.join(line.rstrip().split()).upper()
        yield header, sequence

    def parse_fastq(self):
        """ Fastq generator, yielding a list of 4 lines at a time.
            These 4 lines represent 1 read.
        """
        with open(self.in_file) as fastq_file:
            read_list = []
            index = 0
            # Iterate over each line of fastq file.
            for line in fastq_file:
                read_list.append(line.rstrip())
                index += 1
                if index == 4:
                    yield read_list
                    read_list = []
                    index = 0