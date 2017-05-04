#!/usr/bin/env python


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
written to standard output in fasta format. A file of many headers can be used to select many
sequences.
_____
Usage:

python get_fasta_sequence.py [options] -f <fasta> -s <header> -l <headers.txt>

    flags:

    -f      ------------------- Fasta file from which a sequence is desired.
    -s      ------------------- The header of the sequence desired.
    -l           -------------- A file of header names. One column with each row as a header name. This will
                                override -s.


    OPTIONS:

    -h, --help   -------------- Display the help message.
    -r           -------------- Specify a range for a subset nucleotides to return from the given sequence.
                                e.g. -r 100:25843 returns the subset of nucleotides specified in between these
                                genomic coordinates (0-based). If multiple headers are specified with -l, this
                                range will apply to all sequences.
"""

    import sys

    from dsa_seq_utils.SeqReader import SeqReader
    from dsa_seq_utils.utilities import get_flag
    from dsa_seq_utils.utilities import help_desired

    # Parse the command line arguments.
    if help_desired(sys.argv):
        sys.exit(usage)

    # Get the fasta.
    fasta = get_flag(sys.argv, '-f', usage)

    # Get the fasta header for contig/scaffold of interest.
    one_header = False
    try:
        query_header = get_flag(sys.argv, '-s', usage)
        one_header = True
        # Add a '>' character if not already there.
        if not query_header.startswith('>'):
            query_header = ''.join(('>', query_header))
    except ValueError:
        pass

    # If a range has been specified, retrieve it.
    subseq = False
    if '-r' in sys.argv:
        coordinates = get_flag(sys.argv, '-r', usage)

        try:
            coords = [int(i) for i in coordinates.split(":")]
        except:
            error = """
            The subsequence coordinates has not been properly specified. Specify coordinates using a colon.
            e.g. -r start:end, where start and end are integers. """
            raise ValueError(error)

        subseq = True

    # Check if a list of headers has been passed.
    multi_headers = False
    try:
        header_list = get_flag(sys.argv, '-l', usage)
        multi_headers = True
    except ValueError:
        if not one_header:
            print usage
            raise ValueError('Either -s or -l flags must be specified.')


    x = SeqReader(fasta)
    if not multi_headers:
        query = x.get_seq(query_header)
        if query is not None:
            if not subseq:
                print query[0]
                print query[1]
            else:
                # This check is more for header output, as this will not affect string slicing.
                if coords[1] > len(query[1]):
                    coords[1] = len(query[1])
                print query[0] + " - " + str(coords[0]) + ":" + str(coords[1])
                print query[1][coords[0]:coords[1]]
        else:
            print 'A sequence for header %s was not found' % query_header

    else:
        with open(header_list, 'r') as in_file:
            all_headers = in_file.read().split('\n')
        for query in x.get_multiple_seqs(all_headers):
            if not subseq:
                print query[0]
                print query[1]
            else:
                # This check is more for header output, as this will not affect string slicing.
                if coords[1] > len(query[1]):
                    coords[1] = len(query[1])
                print query[0] + " - " + str(coords[0]) + ":" + str(coords[1])
                print query[1][coords[0]:coords[1]]