__author__ = 'malonge'

import unittest

from Sequence.Sequence import AmbiguousSequence


class AmbiguousSequenceTest(unittest.TestCase):

    def setUp(self):
        self.as_empty_string = AmbiguousSequence('')
        self.as_all_ambiguous = AmbiguousSequence('YRWSKMDVHB')
        self.as_not_ambiguous = AmbiguousSequence('NNNNNNNNNN')
        self.as_flank_ambiguous = AmbiguousSequence('YNNNNNNNNY')

    # Test the constructor of the class.
    def test_init_1(self):
        with self.assertRaises(AttributeError):
            x = AmbiguousSequence(1)

    def test_init_2(self):
        with self.assertRaises(AttributeError):
            x = AmbiguousSequence(False)

    def test_init_3(self):
        with self.assertRaises(AttributeError):
            x = AmbiguousSequence(1.0)

    def test_count_ambiguity_codes_all_ambiguous(self):
        self.assertEqual(self.as_all_ambiguous.count_ambiguity_codes(), 10)

    def test_count_ambiguity_codes_none_ambiguous(self):
        self.assertEqual(self.as_not_ambiguous.count_ambiguity_codes(), 0)

    def test_count_ambiguity_codes_flank_ambiguous(self):
        self.assertEqual(self.as_flank_ambiguous.count_ambiguity_codes(), 2)

    def test_count_ambiguity_codes_empty_string(self):
        self.assertEqual(self.as_empty_string.count_ambiguity_codes(), 0)

    def test_get_code_coords_all_ambiguous(self):
        coord_iter = self.as_all_ambiguous.get_ambiguity_code_coords()
        print coord_iter.next().start()
        print coord_iter.next().end()

        print coord_iter.next().start()
        print coord_iter.next().end()

        print self.as_all_ambiguous.sequence[0:2]

if __name__ == '__main__':
    unittest.main()
