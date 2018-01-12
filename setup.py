#!/usr/bin/env python
import os
import sys
try:
    from setuptools import setup
    HAVE_SETUPTOOLS = True
except ImportError:
    from distutils.core import setup
    HAVE_SETUPTOOLS = False


VERSION = '1.5.3'

setup_kwargs = {
    "version": VERSION,
    "description": 'Rickshaw is an automated driver for Cyclus',
    "license": 'BSD 3-clause',
    "author": 'The ERGS developers',
    "author_email": 'ergsonomic@googlegroups.com',
    "url": 'https://github.com/ergs/rickshaw',
    "download_url": "https://github.com/ergs/rickshaw/zipball/" + VERSION,
    "classifiers": [
        "License :: OSI Approved",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Utilities",
        ],
    "zip_safe": False,
    "data_files": [("", ['LICENSE', 'README.rst']),],
    "scripts": ["scripts/rickshaw", "scripts/rickserv"]
    }

if HAVE_SETUPTOOLS:
    setup_kwargs['install_requires'] = ['python-json-logger', 'pprintpp', 'jinja2']

if __name__ == '__main__':
    setup(
        name='rickshaw',
        packages=['rickshaw'],
        long_description=open('README.rst').read(),
        **setup_kwargs
        )
