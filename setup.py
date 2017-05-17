#!/usr/bin/env python
import os
import sys
try:
    from setuptools import setup
    HAVE_SETUPTOOLS = True
except ImportError:
    from distutils.core import setup
    HAVE_SETUPTOOLS = False

localdir = os.path.dirname(__file__)
sys.path.insert(0, localdir)
import rickshaw
VERSION = rickshaw.__version__
del sys.path[0]

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


if __name__ == '__main__':
    setup(
        name='rickshaw',
        packages=['rickshaw'],
        long_description=open('README.rst').read(),
        **setup_kwargs
        )
