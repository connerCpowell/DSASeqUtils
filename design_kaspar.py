#!/usr/bin/env python


class KasparSequence:
    """
    This class allows for manipulation of an
    individual genomic region for kaspar
    primer designing.
    """

    def __init__(self, kaspar_sequence):
        """
        Create instance variable for genomic kaspar region represented as a 
        string of nucleotide characters.
        The region length will not change, though contents
        may to reflect polymorphisms, or masking.
        
        :param kaspar_sequence: String of nucleotide characters.
        """
        self.sequence = kaspar_sequence

    def replace_coordinates(self, replacement, coord1, coord2):
        """
        Replace region given in coords with replacement character.
        Coords are genomic coordinates, therefore the first
        character has coordinate 1, not 0.

        :param replacement: the character to insert into specified regions
        :param coord1: Start genomic coordinate.
        :param coord2: End genomic coordinate.
        """
        # Parse region into parts that will not be changed.
        pre = self.region[:coord1]
        post = self.region[coord2:]
        insert = ''
        # Insert replacement character(s) for each character in
        # Region to be replaced.
        for i in range(len(self.region) - (len(pre) + len(post))):
            insert += str(replacement)
        self.sequence = pre + insert + post


if __name__ == "__main__":
    usage = """
design_kaspar.py
Michael Alonge
6.4.15
Driscolls
___________
Description:

This command line utility slices a SNP containing region from its parent
chromosome/scaffold, and outputs 3 fasta files.
    1. Said sequence with reference SNP.
    2. Said sequence with alternate SNP.
    3. Said sequence with both options inserted i.e. [A/G]

It also produces blast results mapping the alternate sequences
against the reference, producing a visualization of the SNP.

A masking option is available that allows you to replace regions
given in genomic coordinates with 'n' values.
_____
Usage:

python design_kaspar.py [options] -g <genome build> -db <blast db> -c <LG or scaffold of SNP> -l <SNP Genomic Coordinate> -s <Reference Base,Alternate Base> -f <flanking region> -p <Project Name>

    flags:

    -g       ------------------- Genome build in FASTA format.
    -db      ------------------- Path to blast database.
    -c       ------------------- Fasta header of chromosome/
                                 scaffold with SNP.
    -l       ------------------- Genomic coordinate of SNP.
    -s       ------------------- comma separated list of SNP reference
                                 and alternate nt. i.e. A,G

    -f       ------------------- Integer of the number of flanking
                                 nucleotides to select surrounding SNP
    -p       ------------------- Project name. Prefix for output files.


    OPTIONS:

    -help, --help   ------------ Display help message.
    -m              ------------ Bed file for regions to be masked.
                                 Whole regions will be replaced with 'n'.
______
Output:

    project_name.REF.fasta
    project_name.ALt.fasta
    project_name.SNP.fasta
    project_name.alt.against.ref.blastresults
"""

    import sys

    from get_fasta_sequence import get_seq
    from utils.utilities import log
    from utils.utilities import run
    from utils.utilities import get_flag
    from utils.utilities import help_desired

    # get command line args
    if help_desired(sys.argv):
        sys.exit(usage)

    # Get the fasta.
    assembly = get_flag(sys.argv, '-g', usage)

    # Get the blast database.
    blastdb = get_flag(sys.argv, '-db', usage)

    # Get the fasta header for contig/scaffold of interest.
    scaffold = get_flag(sys.argv, '-c', usage)
    # Add a '>' character if not already there.
    if not scaffold.startswith('>'):
        scaffold = ''.join(('>', scaffold))

    # Get the genomic coordinate of the SNP.
    snp_coord = int(get_flag(sys.argv, '-l', usage))

    # Get the list of SNP, reference, and alternate.
    snp = get_flag(sys.argv, '-s', usage).upper().split(',')

    # Get teh flanking region length.
    flank = int(get_flag(sys.argv, '-f', usage))

    # Get the project name.
    project = get_flag(sys.argv, '-p', usage)

    # Get the masking bed file.
    try:
        masking_file = get_flag(sys.argv, '-m')
        masking = True
    except ValueError:
        log('---- No masking selected.')
        masking = False

    # Get scaffold with SNP.
    log('---- Getting SNP plus flanking region.')
    sequence = get_seq(assembly, scaffold)
    if sequence is None:
        raise ValueError(
            'The header %s provided was not found in the reference genome file.' % scaffold
        )

    # Check that reference base is consistent.
    if sequence[snp_coord-1] != snp[0]:
        raise ValueError(
            'Reference base %s did not equal input base %s.' % (sequence[snp_coord-1], snp[0])
        )

    # Get SNP region within scaffold.
    region = sequence[snp_coord - flank - 1:snp_coord + flank]
    alt_region = KasparSequence(region)
    SNP_region = KasparSequence(region)
    this_SNP = '[' + snp[0] + '/' + snp[1] + ']'

    # Mask
    if masking:
        log('---- Masking SNP region.')
        for line in open(masking_file):
            bed = line.split('\t')
            alt_region.replace_coordinates('n', int(bed[1]) - 1, int(bed[2]) - 1)
            SNP_region.replace_coordinates('n', int(bed[1]) - 1, int(bed[2]) - 1)
        alt_region.replace_coordinates(snp[1], flank, flank+1)
        SNP_region.replace_coordinates(this_SNP, flank, flank+1)
    else:
        alt_region.replace_coordinates(snp[1], flank, flank+1)
        SNP_region.replace_coordinates(this_SNP, flank, flank+1)

    # Write output fasta files.
    log('---- Writing output files.')
    with open(project + '.REF.fasta', 'w') as outfile1:
        outfile1.write(
            scaffold +
            ' ' +
            str(snp_coord - flank - 1) +
            ':' +
            str(snp_coord + flank) +
            ' reference SNP at ' +
            str(flank+1) +
            '\n'
        )
        outfile1.write(sequence)

    with open(project + '.ALT.fasta', 'w') as outfile2:
        outfile2.write(
            scaffold +
            ' ' +
            str(snp_coord - flank - 1) +
            ':' +
            str(snp_coord + flank) +
            ' alternate SNP at ' +
            str(flank+1) +
            '\n'
        )
        outfile2.write(alt_region.sequence)

    with open(project + '.SNP.fasta', 'w') as outfile3:
        outfile3.write(
            scaffold +
            ' ' +
            str(snp_coord - flank -1) +
            ':' +
            str(snp_coord + flank) +
            ' SNP at ' +
            str(flank+1) +
            '\n'
        )
        outfile3.write(SNP_region.sequence)

    # Run blast
    run(
        [
            'blastn',
            '-query',
            '{}.ALT.fasta'.format(project),
            '-db',
            '{}'.format(blastdb),
            '-out',
            '{}.alt.against.ref.blastresults'.format(project)
        ]
    )