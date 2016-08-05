#!/usr/bin/env python

from __future__ import division
import os
import sys
import ntpath
import re
import collections

from utils.SeqReader import SeqReader
from utils.stats import calculate_mean
from utils.stats import calculate_pop_sd
from utils.utilities import log
from utils.utilities import help_desired


class GapSequence:
    """
    Creates objects representing sequences with gaps in them.
    Utilities defined here characterize these gaps.
    count_Ns -------- Calculates total number of 'N' characters present in the sequence.
    get_gaps -------- Uses regular expressions to return each contiguous subsequence of 'N' characters.
    get_gap_coords -- Uses regular expressions to return the string indices of each
                      contiguous subsequence of 'N' characters.
    """

    def __init__(self, sequence):
        self.sequence = sequence.upper()

    def count_Ns(self):
        """ Return the total number of Ns in this sequence. """
        return self.sequence.count('N')

    def get_gaps(self):
        """ Find all of the gaps for this sequence."""
        return re.findall(r'N+', self.sequence)

    def get_gap_coords(self):
        """ Find all of the gap string indices for this sequence. """
        return re.finditer(r'N+', self.sequence)


if __name__ == "__main__":
    usage = """
___________
Description:
Command line utility for analyzing gaps in a fasta file. One file can be analyzed, or up to 3 can be compared.
Use this tool to compare a genome assembly pre and post gap filling with tools such as PBJelly.
_____
Usage:
python gap_stats.py [options] <sequence1.fasta> <sequence2.fasta> <sequence3.fasta>
    OPTIONS:
    -m        Save a matplotlib gap length histogram in current working directory.
              * Requires matplotlib to be installed *
    -p        Write a plain text file of all gap lengths in current working directory for
              use as input into other statistical analysis software.
    -b        Make a gap bed file for each input fasta.
    -h        Print help message.
    """

    def parse_args(args_list):
        """
        Given all command line arguments, make a dictionary containing all
        of the flags, and all of the fasta files.
        If the command line arguments either request help or raises an error,
        that will be done here. If this function returns, it can be assumed that
        the command line statement is ready for further analysis.
        :param args_list: List of command line arguments (sys.argv)
        :return: Dictionary specifying all flags and all fasta files.
        """
        # If no arguments specified, print usage statement with no error.
        if len(args_list) == 1:
            sys.exit(usage)

        # Make all flags upper case to avoid case sensitivity.
        flags = [i.upper() for i in args_list if i.startswith('-')]

        # See if help is desired. If so, print usage with no error.
        if help_desired(flags):
            sys.exit(usage)

        # Retrieve fasta files. At least one, up to 3 is needed.
        fastas = [
            i for i in args_list if
            i.endswith('.fasta') or
            i.endswith('.fa') or
            i.endswith('.fan') or
            i.endswith('.fas')
        ]

        # Make sure that at least one fasta file was found.
        if not fastas:
            print usage
            raise ValueError('No fasta files found.')

        # Make sure that no more than 3 fasta files have been selected.
        if len(fastas) > 3:
            print usage
            raise ValueError(
                'A maximum of 3 fasta files can be compared at once. You entered %r fasta files.' % len(fastas)
            )

        return {
            'flags': flags,
            'fastas': fastas
        }

    def write_gap_stats(info):
        """
        Use info obtained in get_gap_info to write a summary stats csv file.
        :param info: Dictionary where
                       key = fasta file
                       value = ordered dictionary containing all gap info from get_gap_info
        """
        with open('gap_stats.csv', 'w') as out_file:
            # Get each category from each fasta file. One row for each.
            all_percent_N = [str(100*(info[i]['total_N']/info[i]['total_nucleotides'])) for i in info.keys()]
            all_total_gaps = [str(info[i]['total_gaps']) for i in info.keys()]
            all_total_gaps_over_100 = [str(info[i]['total_gaps_over_100']) for i in info.keys()]
            all_longest_gap = [str(max(info[i]['all_gap_lengths'])) for i in info.keys()]
            all_means = [str(calculate_mean(info[i]['all_gap_lengths'])) for i in info.keys()]
            all_standard_deviations = [str(calculate_pop_sd(info[i]['all_gap_lengths'])) for i in info.keys()]

            # Write rows out to csv file.
            # First, write out the header (file names).
            out_file.write(',' + ','.join(ntpath.basename(f) for f in info.keys()) + '\n')

            # Next, write out the stats.
            out_file.write('% N,' + ','.join(all_percent_N) + '\n')
            out_file.write('Total Gaps,' + ','.join(all_total_gaps) + '\n')
            out_file.write('Total Gaps Longer Than 100bp,' + ','.join(all_total_gaps_over_100) + '\n')
            out_file.write('Longest Gap,' + ','.join(all_longest_gap) + '\n')
            out_file.write('Mean Gap Length,' + ','.join(all_means) + '\n')
            out_file.write('Gap Length Standard Deviation,' + ','.join(all_standard_deviations))

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

    def write_hist_img_file(lengths, labels):
        """
        Save a matplotlib length histogram image to current working directory.
        :param lengths: List of Lists of all gap lengths for each fasta.
        :param labels: Labels to be used in the histogram image file.
        """
        import matplotlib.pyplot as plt

        # Find the max and min values for plotting.
        max_length = max(max(i) for i in lengths)
        min_length = min(min(i) for i in lengths)
        bin_size = int(0.025*max_length)

        # Make histogram
        colors = ['r', 'g', 'b']
        plt.hist(
            lengths,
            bins=range(min_length, max_length+bin_size, bin_size),
            color=colors[:len(lengths)],
            label=[ntpath.basename(l) for l in labels]
        )
        plt.legend()
        plt.title('Gap Length Histogram')
        plt.xlabel('Gap Length (b)')
        plt.ylabel('Frequency')
        plt.savefig(os.getcwd() + '/gap_stats_hist.pdf')

    def write_hist_text_file(lengths, labels):
        """
        Write a plain text file to current working directory.
        1 ordered column of all histogram lengths.
        This is for input into statistical analysis software such as R.
        :param lengths: List of Lists of all gap lengths for each fasta.
        :param labels: Labels to be used in the histogram image file.
        """
        for lengths_list, label in zip(lengths, labels):
            hist_file_name = label[:label.rfind('.')] + '.all_lengths.txt'
            with open(os.getcwd() + '/' + ntpath.basename(hist_file_name), 'w') as out_file:
                out_file.write(ntpath.basename(label) + '\n')
                for length in sorted(lengths_list):
                    out_file.write(str(length) + '\n')

    def get_gap_info(in_file):
        """
        Given a fasta file, find out some information regarding its global gap content.
        :param in_file: Fasta or multi-fasta with sequences for gap analysis.
        :return: dictionary with total_N, total_nucleotides, total_gaps and all_gap_lengths
        """
        # Initialize values to be computed.
        total_N = 0
        total_nucleotides = 0
        total_gaps = 0
        total_gaps_over_100 = 0
        all_gap_lengths = []

        # Use a dictionary to store bed coordinates.
        # key = fasta header
        # Value = list of tuples corresponding to genomic coordinates.
        bed_gaps = collections.OrderedDict()

        # Iterate through each sequence in the fasta,
        # and get gap info from each.
        sequences = SeqReader(in_file)
        for header, sequence in sequences.parse_fasta():
            gap_sequence = GapSequence(sequence)

            # Get total number of 'N' characters for this sequence.
            total_N += gap_sequence.count_Ns()
            # Get total number of nucleotides for this sequence.
            total_nucleotides += len(sequence)
            for gap in gap_sequence.get_gaps():
                # Increment total number of gaps
                total_gaps += 1
                if len(gap) > 100:
                    total_gaps_over_100 += 1
                # Save this gap length to master list.
                all_gap_lengths.append(len(gap))

            # Now fill in bed file data structure.
            all_coordinates = [(m.start(0)+1, m.end(0)) for m in gap_sequence.get_gap_coords()]
            if all_coordinates:
                bed_gaps[header] = all_coordinates

        return {
            'total_N': total_N,
            'total_nucleotides': total_nucleotides,
            'total_gaps': total_gaps,
            'total_gaps_over_100': total_gaps_over_100,
            'all_gap_lengths': all_gap_lengths,
            'bed_gaps': bed_gaps
        }

    # Parse the command line arguments.
    arg_dict = parse_args(sys.argv)

    # Get gap info for each fasta.
    all_files_info = collections.OrderedDict()
    for fasta in arg_dict['fastas']:
        log(' ---- Analyzing gaps for %s' % fasta)
        all_files_info[fasta] = get_gap_info(fasta)

    # Write csv file with basic gap stats.
    write_gap_stats(all_files_info)

    # Check if bed file is desired.
    # Save to current working directory if so.
    if '-B' in arg_dict['flags']:
        log(' ---- Writing bed file(s).')
        for f in all_files_info.keys():
            file_name = f[:f.rfind('.')] + '.gaps.bed'
            write_bed_file(all_files_info[f]['bed_gaps'], file_name)

    # Check if histogram is desired.
    # Save to current working directory if so.
    if '-M' in arg_dict['flags']:
        log(' ---- Writing histogram image file.')
        all_lengths = [all_files_info[i]['all_gap_lengths'] for i in all_files_info.keys()]
        write_hist_img_file(all_lengths, all_files_info.keys())

    # Make a plain text file for plugging into ones
    # favorite statistical analysis software.
    if '-P' in arg_dict['flags']:
        log(' ---- Writing histogram plain text file.')
        all_lengths = [all_files_info[i]['all_gap_lengths'] for i in all_files_info.keys()]
        write_hist_text_file(all_lengths, all_files_info.keys())
