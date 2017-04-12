__author__ = 'malonge'

import os
import unittest

#from dsa_seq_utils.utilities import reverse_complement
from lift_over import switch_SW
from lift_over import get_reverse_coords
from lift_over import place_pre_seqs
from lift_over import get_post_seqs
from lift_over import convert_coordinates


class LiftOverTest(unittest.TestCase):

    def setUp(self):
        with open('test_post_file.fasta', 'w') as f:
            f.write('>post_header\n')
            f.write('AATTWCCSGG')

        with open('test_pre_file.fasta', 'w') as f:
            f.write('>pre_header_1\n')
            f.write('ATTW\n')
            f.write('>pre_header_2\n')
            f.write('GGSA')

    def tearDown(self):
        os.remove('test_post_file.fasta')
        os.remove('test_pre_file.fasta')

    def test_get_post_seqs(self):
        d1 = get_post_seqs('test_post_file.fasta')
        self.assertEqual(d1, {'>post_header': 'AATTWCCSGG'})

    def test_switch_SW(self):
        d1 = get_post_seqs('test_post_file.fasta')
        new_seq = switch_SW(d1['>post_header'])
        self.assertEqual(new_seq, 'AATTSCCWGG')

    def test_place_pre_seqs(self):
        d1 = get_post_seqs('test_post_file.fasta')
        placements = place_pre_seqs({'>pre_header_1', '>pre_header_2'}, 'test_pre_file.fasta', d1, switch_sw=True)
        self.assertEqual(placements, {
            '>pre_header_1': ('>post_header', 1, False, 4),
            '>pre_header_2': ('>post_header', 3, True, 4)
        })

    def test_get_reverse_coords(self):
        # This assumes 1-indexed
        start, end = get_reverse_coords(1, 3, 4)
        self.assertEqual(start, 2)
        self.assertEqual(end, 4)