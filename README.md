# DSASeqUtils

<b>DSASeqUtils</b> is a collection of python command line utilities for simple processing of DNA sequence data. 

# Installing DSASeqUtils
## Platforms
<ul>
  <li>Linux</li>
  <li>Mac OSX</li>
</ul>
## Dependencies
DSASeqUtils has no dependencies except for python2.7. There is an optional usage of the gap_stats.py utility that requires matplotlib.

## Installing From Source
Currently, the only way to install DSASeqUtils is from source. To install, execute the following commands:

```
$git clone https://github.com/malonge/DSASeqUtils
$cd DSASeqUtils
$python setup.py install
```

# Usage
All command line utilities can will show help message if run with no arguments, or if the -h flag is specified. 

## Genomic Gap Analysis

### gap_stats.py
```
Command line utility for analyzing gaps in a fasta file. One file can be analyzed, or up to 3 can be compared.
    Use this tool to compare a genome assembly pre and post gap filling with tools such as PBJelly.
    Usage:
      python gap_stats.py [options] <sequence1.fasta> <sequence2.fasta> <sequence3.fasta>
    Options
      -m        Save a matplotlib gap length histogram in current working directory.
                * Requires matplotlib to be installed *
      -p        Write a plain text file of all gap lengths in current working directory for
                use as input into other statistical analysis software.
      -b        Make a gap bed file for each input fasta.
      -h        Print help message.
```
