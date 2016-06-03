#!/usr/bin/env python
import re

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
    -b           ------------- Write the genomic coordinates of all ambiguous
                                nucleotides to amb_coords.bed
"""


class AmbiguousSequence:
    """
    Creates objects representing sequences with gaps in them.
    Utilities defined here characterize these gaps.
    count_Ns -------- Calculates total number of 'N' characters present in the sequence.
    get_gaps -------- Uses regular expressions to return each contiguous subsequence of 'N' characters.
    get_gap_coords -- Uses regular expressions to return the string indices of each
                      contiguous subsequence of 'N' characters.
    """

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

    ambiguity_regex = r'[YRWSKMDVHB]'

    def __init__(self, sequence):
        self.sequence = sequence.upper()

    def count_ambiguity_codes(self):
        """ Return the total number of Ns in this sequence. """
        return sum(map(self.sequence.count, self.ambiguity_codes))

    def get_ambiguity_code_coords(self):
        """ Find all of the gap string indices for this sequence. """
        return re.finditer(self.ambiguity_regex, self.sequence)

if __name__ == '__main__':
    import sys
    import os
    import ntpath

    from utils.SeqReader import SeqReader
    from utils.utilities import get_flag
    from utils.utilities import help_desired
    from utils.utilities import log

    def write_bed_file(bed_dict, out_file_name):
        """
        From a dictionary storing bed file info, write output file in bed format.
        :param bed_dict: Dict where keys = fasta headers, and values = coordinates of each gap in that sequence.
        :param out_file_name: Name for output bed file.
        """
        with open(os.getcwd() + '/' + ntpath.basename(out_file_name), 'w') as out_file:
            for header in bed_dict.keys():
                for coordinates in bed_dict[header]:
                    out_file.write(
                        '%s\t%r\t%r\n' %(header[1:], coordinates[0], coordinates[1])
                    )

    # Get command line args
    if help_desired(sys.argv):
        sys.exit(usage)

    # Get the sequence file.
    input_file = get_flag(sys.argv, '-f', usage)

    # Check if bed file is requested.
    if '-b' in sys.argv:
        bed_file_requested = True
        log(' ---- Bed file requested.')
    else:
        bed_file_requested = False
        log(' ---- Bed file not requested.')

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

    # Iterate through each sequence and get ambiguity code info.
    # For now, I will just get a per3centage of nucleotides that are
    # ambiguous, and their genomic coordinates.

    # In the future, maybe report number per sequence, and frequency of each code.
    total = 0
    total_ambiguity = 0
    all_ambiguous_coords = {}
    x = SeqReader(input_file)
    if using_fastas:
        for header, sequence in x.parse_fasta():
            ambiguous_seq = AmbiguousSequence(sequence)
            total += len(ambiguous_seq.sequence)
            total_ambiguity += ambiguous_seq.count_ambiguity_codes()
            all_coordinates = [(m.start(0), m.end(0)) for m in ambiguous_seq.get_ambiguity_code_coords()]
            all_ambiguous_coords[header] = all_coordinates

    else:
        for read in x.parse_fastq():
            ambiguous_seq = AmbiguousSequence(read[1])
            total += len(ambiguous_seq.sequence)
            total_ambiguity += ambiguous_seq.count_ambiguity_codes()
            all_coordinates = [(m.start(0), m.end(0)) for m in ambiguous_seq.get_ambiguity_code_coords()]
            all_ambiguous_coords[read[0]] = all_coordinates

    # If a bed file is requested, write to current workding directory.
    if bed_file_requested:
        write_bed_file(all_ambiguous_coords, 'ambiguous_nucleotides.bed')
    log(' ---- The total number of nucleotides is %r' %total)
    log(' ---- The total number of ambiguous nucleotides is %r' %total_ambiguity)