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
            '-HELP' in args_list
        ]
    ):
        return True
    else:
        return False