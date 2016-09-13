#!/usr/bin/env python
from dsa_seq_utils.SeqReader import SeqReader

if __name__ == "__main__":
    usage = """
Michael Alonge
get_fasta_sequence.py
5.3.16
Driscolls
___________
Description:

This command line utility selects one fasta sequence from a multi fasta file
given a sequence header. The sequence from the desired header is
written to standard output in fasta format.
_____
Usage:

python get_fasta_sequence.py [options] -f <fasta> -s <header>

    flags:

    -f      ------------------- Fasta file from which a sequence is desired.
    -s      ------------------- The header of the sequence desired.


    OPTIONS:

    -h, --help   -------------- Display help message.
"""

    import sys

    from dsa_seq_utils.utilities import get_flag
    from dsa_seq_utils.utilities import help_desired

    # Parse the command line arguments.
    if help_desired(sys.argv):
        sys.exit(usage)

    # Get the fasta.
    fasta = get_flag(sys.argv, '-f', usage)

    # Get the fasta header for contig/scaffold of interest.
    query_header = get_flag(sys.argv, '-s', usage)
    # Add a '>' character if not already there.
    if not query_header.startswith('>'):
        query_header = ''.join(('>', query_header))

    x = SeqReader(fasta)
    query = x.get_seq(query_header)
    if query is not None:
        print query[0]
        print query[1]
    else:
        print 'A sequence for header %s was not found' % query_header