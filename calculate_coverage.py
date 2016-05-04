from __future__ import division

if __name__ == "__main__":
    usage = """
python calculate_coverage [options] -s <genome size>
    flags:

    -s      ------------------- Genome size


    OPTIONS:

    -help, --help   ------------ Display help message.
    -a              ------------ Input files are in fasta format.
    -q              ------------ Input files are in fastq format.

"""

    import sys

    from utils.SeqReader import SeqReader
    from utils.stats import calculate_mean
    from utils.stats import calculate_pop_sd
    from utils.utilities import get_flag
    from utils.utilities import help_desired

    # Get command line args
    if help_desired(sys.argv):
        sys.exit(usage)

    genome_size = get_flag(sys.argv, '-s', usage)
    try:
        genome_size = int(genome_size)
    except ValueError():
        raise ValueError('Genome size must be an integer.')

    if '-a' in sys.argv and '- q' not in sys.argv:
        using_fastas = True
    elif '-q' in sys.argv and '-a' not in sys.argv:
        using_fastas = False
    elif '-q' in sys.argv and '-a' in sys.argv:
        raise ValueError(
            "'-a' and '-q' flag cannot be specified together. Files must be either all fasta or all fastq format."
        )
    else:
        raise ValueError(
            "A '-a' or '-q' flag must be specified. This specifies fasta or fastq file format."
        )

    # Get the list of all fasta or fastq files.
    if using_fastas:
        all_files = [
            i for i in sys.argv if
            i.endswith('.fasta') or
            i.endswith('.fa') or
            i.endswith('.fan') or
            i.endswith('.fas')
        ]
        if not all_files:
            raise ValueError(
                "The '-a' option was specified, but no fasta files were found."
            )

    else:
        all_files = [
            i for i in sys.argv if
            i.endswith('.fastq') or
            i.endswith('.fq')
        ]
        if not all_files:
            raise ValueError(
                "The '-q' option was specified, but no fastq files were found."
            )

    all_seq_lengths = []
    for f in all_files:
        x = SeqReader(f)
        if using_fastas:
            for header, seq in x.parse_fasta():
                all_seq_lengths.append(len(seq))

        else:
            for read in x.parse_fastq():
                all_seq_lengths.append(len(read[1]))

    print "The coverage for a genome of size %r is %f." % (genome_size, sum(all_seq_lengths)/genome_size)
    print "The average read length is %f." % calculate_mean(all_seq_lengths)
    print "The read length standard deviation is %f." % calculate_pop_sd(all_seq_lengths)



