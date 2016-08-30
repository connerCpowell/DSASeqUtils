__author__ = 'malonge'
import re


class BaseSequence(object):

    def __init__(self, in_sequence):
        if not isinstance(in_sequence, str):
            raise AttributeError('Only a string can be used to instantiate this class.')
        self.sequence = in_sequence.upper()


class KasparSequence(BaseSequence):

    def replace_coordinates(self, replacement, coord1, coord2):
        """
        Replace region given in coords with replacement character.
        Coords are genomic coordinates, therefore the first
        character has coordinate 1, not 0.

        :param replacement: the character to insert into specified regions
        :param coord1: Start genomic coordinate.
        :param coord2: End genomic coordinate.
        """
        # Check that there is not an empty string
        if not self.sequence:
            raise ValueError('Cannot replace coordinates of an empty string.')
        # Parse region into parts that will not be changed.
        pre = self.sequence[:coord1]
        post = self.sequence[coord2:]
        insert = ''
        # Insert replacement character(s) for each character in
        # Region to be replaced.
        for i in range(len(self.sequence) - (len(pre) + len(post))):
            insert += str(replacement)
        self.sequence = pre + insert + post


class AmbiguousSequence(BaseSequence):
    """
    Creates objects representing sequences with gaps in them.
    Utilities defined here characterize these gaps.
    count_Ns -------- Calculates total number of 'N' characters present in the sequence.
    get_gaps -------- Uses regular expressions to return each contiguous sub sequence of 'N' characters.
    get_gap_coords -- Uses regular expressions to return the string indices of each
                      contiguous sub sequence of 'N' characters.
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

    def count_ambiguity_codes(self):
        """ Return the total number of Ns in this sequence. """
        return sum(map(self.sequence.count, self.ambiguity_codes))

    def get_ambiguity_code_coords(self):
        """ Find all of the gap string indices for this sequence. """
        return re.finditer(self.ambiguity_regex, self.sequence)


class GapSequence(BaseSequence):
    """
    Creates objects representing sequences with gaps in them.
    Utilities defined here characterize these gaps.
    count_Ns -------- Calculates total number of 'N' characters present in the sequence.
    get_gaps -------- Uses regular expressions to return each contiguous subsequence of 'N' characters.
    get_gap_coords -- Uses regular expressions to return the string indices of each
                      contiguous subsequence of 'N' characters.
    """

    def count_Ns(self):
        """ Return the total number of Ns in this sequence. """
        return self.sequence.count('N')

    def get_gaps(self):
        """ Find all of the gaps for this sequence."""
        return re.findall(r'N+', self.sequence)

    def get_gap_coords(self):
        """ Find all of the gap string indices for this sequence. """
        return re.finditer(r'N+', self.sequence)
