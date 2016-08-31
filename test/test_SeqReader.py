__author__ = 'malonge'
import os
import unittest

from dsa_seq_utils.SeqReader import SeqReader


class SeqReaderTest(unittest.TestCase):

    def setUp(self):
        # Make a fasta file that adheres to fasta convention.
        # Alternate header and sequence each line.
        with open('good_alt_line.fasta', 'w') as f:
            # Write two lines of a fasta file
            f.write('>test1\n')
            f.write('AAAAAAAAAA\n')
            f.write('>test2\n')
            f.write('GGGGGGGGGG')

        # Make a fasta file that adheres to fasta convention.
        # Do not alternate header and sequence each line.
        with open('good_non_alt_line.fasta', 'w') as f:
            # Write two lines of a fasta file
            f.write('>test1\n')
            f.write('AAAAA\n')
            f.write('AAAAA\n')
            f.write('>test2\n')
            f.write('GGGGG\n')
            f.write('GGGGG\n')

        # Make a fasta file that does not adhere to fasta convention
        # first line is a comment.
        with open('bad_comment.fasta', 'w') as f:
            # Write two lines of a fasta file
            f.write('#This is a comment\n')
            f.write('>test\n')
            f.write('AAAAAAAAAA\n')
            f.write('>test\n')
            f.write('GGGGGGGGGG')

        # Make a fasta file that does not adhere to fasta convention
        # No headers.
        with open('bad_no_header.fasta', 'w') as f:
            # Write two lines of a fasta file
            f.write('AAAAAAAAAA\n')
            f.write('GGGGGGGGGG')

        # Make a fastq file that adheres to fastq convention
        with open('good.fastq', 'w') as f:
            f.write('@header\n')
            f.write('AAAAAAAAAA\n')
            f.write('+\n')
            f.write('QQQQQQQQQQ\n')

        # Make a fastq file where the number of lines is not a multiple of 4.
        with open('bad_line_number.fastq', 'w') as f:
            f.write('@header\n')
            f.write('AAAAAAAAAA\n')
            f.write('+\n')
            f.write('QQQQQQQQQQ')
            f.write('@header')

    def tearDown(self):
        os.remove('good_alt_line.fasta')
        os.remove('good_non_alt_line.fasta')
        os.remove('bad_comment.fasta')
        os.remove('bad_no_header.fasta')
        os.remove('good.fastq')
        os.remove('bad_line_number.fastq')

    def test_init_1(self):
        with self.assertRaises(AttributeError):
            x = SeqReader(True)

    def test_non_existent_file(self):
        with self.assertRaises(IOError):
            x = SeqReader('fake_file_that_does_not_exists.fasta')
            for header, sequence in x.parse_fasta():
                pass

    def test_good_alt_lines_fasta(self):
        x = SeqReader('good_alt_line.fasta')
        fasta_iter = x.parse_fasta()

        header, sequence = fasta_iter.next()
        self.assertEqual(header, '>test1')
        self.assertEqual(sequence, 'AAAAAAAAAA')

        header, sequence = fasta_iter.next()
        self.assertEqual(header, '>test2')
        self.assertEqual(sequence, 'GGGGGGGGGG')

    def test_good_non_alt_lines_fasta(self):
        x = SeqReader('good_non_alt_line.fasta')
        fasta_iter = x.parse_fasta()

        header, sequence = fasta_iter.next()
        self.assertEqual(header, '>test1')
        self.assertEqual(sequence, 'AAAAAAAAAA')

        header, sequence = fasta_iter.next()
        self.assertEqual(header, '>test2')
        self.assertEqual(sequence, 'GGGGGGGGGG')

    def test_bad_comment(self):
        x = SeqReader('bad_comment.fasta')
        fasta_iter = x.parse_fasta()

        header, sequence = fasta_iter.next()
        self.assertEqual(header, '>test')
        self.assertEqual(sequence, 'AAAAAAAAAA')

        header, sequence = fasta_iter.next()
        self.assertEqual(header, '>test')
        self.assertEqual(sequence, 'GGGGGGGGGG')

    def test_no_header(self):
        with self.assertRaises(RuntimeError):
            x = SeqReader('bad_no_header.fasta')
            for header, seq in x.parse_fasta():
                pass

    def test_parse_fasta_with_fastq(self):
        with self.assertRaises(RuntimeError):
            x = SeqReader('good.fastq')
            for header, seq in x.parse_fasta():
                pass

    def test_good_parse_fastq(self):
        x = SeqReader('good.fastq')
        for header, seq, plus, qual in x.parse_fastq():
            self.assertEqual(header, '@header')
            self.assertEqual(seq, 'AAAAAAAAAA')
            self.assertEqual(plus, '+')
            self.assertEqual(qual, 'QQQQQQQQQQ')

    """
    # Should I add some features to catch this?
    # Rigth now no errors are thrown
    def test_incorrect_line_number_fastq(self):
        x = SeqReader('bad_line_number.fastq')
        for header, seq, plus, qual in x.parse_fastq():
            print header

    def test_parse_fastq_with_fasta(self):
        x = SeqReader('good_alt_line.fasta')
        for read in x.parse_fastq():
            print read

    """

if __name__ == '__main__':
    unittest.main()