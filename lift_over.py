__author__ = 'malonge'

import string
import argparse
from collections import OrderedDict

from dsa_seq_utils.SeqReader import SeqReader
from dsa_seq_utils.utilities import reverse_complement
from dsa_seq_utils.utilities import log


def get_reverse_coords(start_coord, end_coord, seq_length):
        """
        Returns new genomic coordinates of a region that has undergone reverse complementation.

        new start coordinate = seqLength - endCoord
        new end coordinate = seqLength - startCoord
        :param startCoord:
        :param endCoord:
        :param seqLength:
        :return:
        """
        return seq_length - (end_coord - 1), seq_length - (start_coord - 1)


def switch_SW(in_seq):
    return in_seq.translate(string.maketrans('SW', 'WS'))


def get_post_seqs(post_file):
    """
    Save the post assembly as an ordered dictionary - header: sequence. Ordered means that
    if the larger sequences are first, the search should go faster.
    :param post_file:
    :return:
    """
    seqs = OrderedDict()
    x = SeqReader(post_file)
    for header, sequence in x.parse_fasta():
        seqs[header] = sequence.upper()

    return seqs


def get_query_seqs(in_coords_file, delim='\t'):
    """

    :param in_coords_file:
    :param delim:
    :return:
    """
    headers = []
    with open(in_coords_file, 'r') as f:
        for line in f:
            if not line.startswith('#'):
                L1 = line.split(delim)
                headers.append(L1[0])

    return set(headers)


def place_pre_seqs(query_headers, pre_file, post_seqs, switch_sw=False):
    """

    :param query_seqs: set or list of query headers to be placed.
    :param post_seqs: dictionary made from get_post_seqs (header:sequence) for post file
    :return:
    """
    placements = dict()
    total = 0
    x = SeqReader(pre_file)
    for query_header in query_headers:
        placed = False
        reverse_complimented = False
        try:
            query_seq = x.get_seq(query_header)[1]
        except TypeError:
            raise ValueError('The query sequence in the coordinates file was not found %s.' % query_header)

        for post_header in post_seqs.keys():
            search_result = post_seqs[post_header].find(query_seq)
            if search_result != -1:
                placed = True
                break

        if not placed:
            # Reverse compliment and try again
            reverse_complimented = True
            query_seq_R = reverse_complement(query_seq)

            # Switch S and W nucleotides if necessary
            if switch_sw:
                query_seq_R = switch_SW(query_seq_R)

            for post_header in post_seqs.keys():
                search_result = post_seqs[post_header].find(query_seq_R)
                if search_result != -1:
                    placed = True
                    break

        if not placed:
            raise ValueError('Sequence %s was not found in the post assembly.' % query_header)

        total += 1
        if total%100 == 0:
            log('processed %r sequecnes' % total)
        pre_length = len(query_seq)
        placements[query_header] = (post_header, search_result, reverse_complimented, pre_length)

    return placements


def convert_coordinates(coords_file, placements, delim='\t'):
    """
    Update the genomic coordinates of the given file.
    :param coords_file:
    :return:
    """
    # Make new output file.
    base_name = coords_file[:coords_file.rfind('.')]
    out_file = open(base_name + '.transfered.genes.gff3', 'w')

    # Iterate through input gene file.
    for line in open(coords_file):
        if line.startswith('#'):
            out_file.write(line)
        else:
            # If not a comment line, update chromosome and coordinate info.
            split_line = line.split(delim)
            header = str(split_line[0])
            # Raise error under the else condition here
            if header in placements.keys():
                start_coord = int(split_line[3])
                end_coord = int(split_line[4])
                if placements[header][2]:
                    # print reverse complement coords.
                    new_coords = get_reverse_coords(start_coord, end_coord, placements[header][3])
                    out_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (placements[header][0][1:], split_line[1],
                                                                           split_line[2], new_coords[0] + placements[header][1] - 1,
                                                                           new_coords[1] + placements[header][1] - 1, split_line[5],
                                                                           split_line[6], split_line[7], split_line[8]))
                else:
                    out_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (placements[header][0][1:], split_line[1],
                                                                           split_line[2], str(start_coord + placements[header][1]),
                                                                           str(placements[header][1] + end_coord), split_line[5], split_line[6],
                                                                           split_line[7], split_line[8]))
    out_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Lift over genomic coordinates from one assembly to another.')
    parser.add_argument('post_assembly', metavar='<post_assembly.fasta>', type=str,
                        help='Assembly to which genomic coordinates will be lifted over.')

    parser.add_argument('pre_assembly', metavar='<pre_assembly.fasta>', type=str,
                        help='Assembly from which genomic coordinates will be lifted over.')

    parser.add_argument('coordinates', metavar='<coordinates.gff3>', type=str,
                        help='File with genomic coordnates to be lifted over.')

    parser.add_argument('-sw', action="store_true", default=False, help='Switch S and W ambiguity codes when reverse complementing.')

    args = parser.parse_args()

    post_assembly = args.post_assembly
    pre_assembly = args.pre_assembly
    coordinates_file = args.coordinates
    sw = args.sw

    log('Parsing post assembly sequences.')
    post_dict = get_post_seqs(post_assembly)

    log('Getting all pre assembly sequences.')
    query_header_set = get_query_seqs(coordinates_file)

    log('%r query sequences are present in the coordinates file.' %len(query_header_set))
    log('Finding the query headers in the post assembly.')
    final_placements = place_pre_seqs(query_header_set, pre_assembly, post_dict, switch_sw=sw)

    log('Writing coordinates file with coordinates lifted over.')
    convert_coordinates(coordinates_file, final_placements)