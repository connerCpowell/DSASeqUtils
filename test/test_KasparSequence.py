__author__ = 'malonge'
import unittest

from Sequence.Sequence import KasparSequence


class KasparSequenceTest(unittest.TestCase):

    def setUp(self):
        self.ks_empty_string = KasparSequence('')
        self.ks_string = KasparSequence('AAAAAAAAAA')

    def test_init_1(self):
        with self.assertRaises(AttributeError):
            x = KasparSequence(1)

    def test_init_2(self):
        with self.assertRaises(AttributeError):
            x = KasparSequence(False)

    def test_init_3(self):
        with self.assertRaises(AttributeError):
            x = KasparSequence(1.0)

    # Test the replace_coordinates method.
    def test_replace_coordinates_empty_string(self):
        with self.assertRaises(ValueError):
            self.ks_empty_string.replace_coordinates('N', 10, 20)

    def test_replace_first_character(self):
        self.ks_string.replace_coordinates('N', 0, 1)
        self.assertEqual(self.ks_string.sequence, 'NAAAAAAAAA')

    def test_replace_last_character(self):
        self.ks_string.replace_coordinates('N', 9, 10)
        self.assertEqual(self.ks_string.sequence, 'AAAAAAAAAN')

    def test_replace_all_characters(self):
        self.ks_string.replace_coordinates('N', 0, 10)
        self.assertEqual(self.ks_string.sequence, 'NNNNNNNNNN')

    def test_replace_no_characters(self):
        self.ks_string.replace_coordinates('N', 0, 0)
        self.assertEqual(self.ks_string.sequence, 'AAAAAAAAAA')

if __name__ == '__main__':
    unittest.main()