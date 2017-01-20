#!/usr/bin/env python
import time
import subprocess


def run(cmnd):
    """ Run command and report status. """
    log(' ---- Running : %s' % cmnd)
    if subprocess.call(cmnd) != 0:
        raise RuntimeError('Failed : %s ' % cmnd)


def log(message):
    """ Log messages to standard output. """
    print time.ctime() + ' ' + message


def get_flag(args_list, flag, usage=''):
    """

    :param args_list:
    :param flag:
    :param usage:
    """
    try:
        arg = args_list[args_list.index(flag) + 1]
    except ValueError:
        if usage:
            print usage
        raise ValueError("No '%s' flag specified." % flag)
    except IndexError:
        if usage:
            print usage
        raise ValueError("The %s flag was specified, but was not followed by an argument." % flag)
    return arg


def help_desired(args_list):
    """
    Detects if a help message has been requested in the command line arguments.
    :param args_list: List of command line arguments.
    """
    if any(
        [
            '-h' in args_list,
            '-H' in args_list,
            '-help' in args_list,
            '-HELP' in args_list,
            '--help' in args_list,
            '--HELP' in args_list
        ]
    ):
        return True
    return False


def kmerize(seq, k):
    """
    :param seq:
    :param k:
    """
    for i in range(len(seq) - k +1):
        yield seq[i:i+k]


def find_coverage_cutoff(read_lengths, genome_size, desired_coverage):
    """
    Given a desired coverage and a list of read lengths, return
    the read length at which all reads greater than that value collectively
    reach the desired coverage.

    :param read_lengths:
    :param genome_size:
    :param desired_coverage:
    """
    sorted_read_lengths = sorted(read_lengths, reverse=True)
    total = 0

    for read_length in sorted_read_lengths:
        total += read_length

        # Check if the desired coverage has been reached yet
        if total/genome_size >= desired_coverage:
            return read_length - 1

    # If the desired coverage is never reached, let the user know.
    error = """
    The entire dataset does not reach the desired coverage. The coverage
               of the dataset is %f""" % (total/genome_size)
    raise RuntimeError(error)