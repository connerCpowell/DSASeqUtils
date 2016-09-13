# DSASeqUtils

<b>DSASeqUtils</b> is a collection of python command line utilities for simple processing of DNA sequence data. 

# Installing DSASeqUtils
## Platforms
<ul>
  <li>Linux</li>
  <li>Mac OSX</li>
</ul>
## Dependencies
All utilities require python2.7.

design_kaspar.py requires blastn. Please ensure blastn is in your path before executing design_kaspar.py 

gap_stats.py has an optional flag that requires matplotlib.

## Installing From Source
Currently, the only way to install DSASeqUtils is from source. To install, execute the following commands:

```
$git clone https://github.com/malonge/DSASeqUtils
$cd DSASeqUtils
$python setup.py install
```

# Command Line Utilities Usage
All command line utilities will show help message if run with no arguments, or if the -h flag is specified. 

## Genomic Gap Analysis

### gap_stats.py
```
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
```

## Genomic Ambiguity Analysis

### analyze_ambiguity.py
```
___________
Description:
This command line utility takes a sequences file, and reports various metrics
regarding the ambiguity codes therein.
_____
Usage:
python analyze_ambiguity.py [options] -f <sequence file>
    flags:
    -f      ------------------- Sequence file for which ambiguity code analysis is desired.
    OPTIONS:
    -h, --help   -------------- Display help message.
    -a           -------------- Input file is in fasta format.
    -q           -------------- Input file is in fastq format.
    -b           -------------- Write the genomic coordinates of all ambiguous
                                nucleotides to amb_coords.bed
```

## Genomic Coverage Analysis

### calculate_coverage.py

```
___________
Description:
This command line utility calculates genome coverage given a set of fasta
or fastq files. This is not a utility that makes use of mapping information to
report precise coverage information. Rather, this tool reports a theoretical
global genome coverage given an expected genome size.
_____
Usage:
python calculate_coverage [options] -s <genome size> <fastq/fasta file(s)>
    flags:
    -s       ------------------- Genome size in bp. e.g. 1 Mb genome = 1000000
    OPTIONS:
    -h, --help      ------------ Display help message.
    --hist          ------------ Write a read length histogram file to current working directory.
    -a              ------------ Input files are in fasta format.
    -q              ------------ Input files are in fastq format.
"""
```

## Kaspar Primer Design

### design_kaspar.py

```
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
```

## Fasta/Fastq Manipulation

### filter_lengths.py

```
___________
Description:

This command line utility takes a sequence file, and output sequences
of a length that falls between upper and lower limits.

_____
Usage:

python filter_lengths.py [options] -f <sequence file> -c <length cutoff>

    flags:

    -f      ------------------- Sequence file from which a sequence is desired.
    -l      ------------------- Lower cutoff value for read length.
    -u      ------------------- Upper cutoff value for read length.


    OPTIONS:

    -h, --help   -------------- Display help message.
    -a           -------------- Input file is in fasta format.
    -q           -------------- Input file is in fastq format.
```

### get_fasta_sequence.py

```
___________
Description:
This command line utility selects one fasta sequence from a multi fasta file
given a sequence header. The sequence from the desired header is
written to standard output in fasta format.
_____
Usage:
python get_fasta_sequence.py [options] -f <fasta> -s <header>
    flags:
    -f      ------------------- Fasta file from which a sequence is desired.
    -s      ------------------- The header of the sequence desired.
    OPTIONS:
    -h, --help   -------------- Display help message.
```

### search_subseq.py

```
___________
Description:

This command line utility takes a sequence file and outputs sequences
of that file containing a specified subsequence.

_____
Usage:

python search_subseq.py [options] -f <sequence file> -s <length cutoff>

    flags:

    -f      ------------------- File from which a sequence is desired.
    -s      ------------------- The subsequence to search for.


    OPTIONS:

    -h, --help   -------------- Display help message.
    -a           -------------- Input file is in fasta format.
    -q           -------------- Input file is in fastq format.
```
# API
## Fasta Sequence Generator
These sequences generators are light weight and designed for speed. Though they iterate through large files with speed, they are quite easy to break.

There are two sequences generators, one for fasta and one for fastq format. Both of these are methods of the SeqReader class.
```
from dsa_seq_utils.SeqReader import SeqReader

x = SeqReader('sequences.fasta')
for header, sequence in x.parse_fasta():
    # Do something with the header and sequence
    
y = SeqReader('sequences.fastq')
for header, sequence, plus, qual in y.parse_fastq():
    # Do something with header, sequence, plus, and qual
```
