__author__ = 'malonge'
import unittest

from gap_stats import GapSequence


class GapStatsTest(unittest.TestCase):

    def setUp(self):
        self.gs_empty_string = GapSequence('')
        self.gs_one_flanked_gap = GapSequence('AANNAA')
        self.gs_two_flanked_gaps = GapSequence('AANNAANNAA')
        self.gs_all_N = GapSequence('NNNN')
        self.gs_flanking_N = GapSequence('NAAN')
        self.gs_lower_case = GapSequence('nn')


    # Test the constructor of the class.
    def test_init_1(self):
        with self.assertRaises(AttributeError):
            x = GapSequence(1)

    def test_init_2(self):
        with self.assertRaises(AttributeError):
            x = GapSequence(False)

    def test_init_3(self):
        with self.assertRaises(AttributeError):
            x = GapSequence(1.0)


    # Test the count_N method.
    def test_count_N_empty_string(self):
        self.assertEqual(self.gs_empty_string.count_Ns(), 0)

    def test_count_N_2_Ns(self):
        self.assertEqual(self.gs_one_flanked_gap.count_Ns(), 2)

    def test_count_N_lower_case(self):
        self.assertEqual(self.gs_lower_case.count_Ns(), 2)

    # Test the get_gaps method
    def test_get_gaps_empty_string(self):
        self.assertEqual(self.gs_empty_string.get_gaps(), [])

    def test_get_gaps_1_gap(self):
        self.assertEqual(self.gs_one_flanked_gap.get_gaps(), ['NN'])

    def test_get_gaps_2_gaps(self):
        self.assertEqual(self.gs_two_flanked_gaps.get_gaps(), ['NN', 'NN'])

    def test_get_gaps_only_N(self):
        self.assertEqual(self.gs_all_N.get_gaps(), ['NNNN'])

    def test_get_gaps_flanking_gap(self):
        self.assertEqual(self.gs_flanking_N.get_gaps(), ['N', 'N'])

"""
    # Test the get_gap_coords method
    def test_get_gap_coords(self):
        x = GapSequence('AANNAA')
        self.assertEqual(x.get_gap_coords(), )
"""

if __name__ == '__main__':
    unittest.main()