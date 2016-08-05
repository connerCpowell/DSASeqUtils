#!/usr/bin/env python

from setuptools import setup
import glob

scripts = glob.glob("*.py")

setup(
    name='DSASeqUtils',
    version='1.1',
    description='A collection of command line utilities for simple processing of DNA sequence data.',
    author='Michael Alonge',
    author_email='michael.alonge@driscolls.com',
    packages=['utils'],
    package_dir={'utils': 'utils/'},
    scripts=scripts,
)