#!/usr/bin/env python

import nytcampfin
from distutils.core import setup

README = open('README.md').read()

setup(
    name = "nytcampfin",
    version = nytcampfin.__version__,
    description = "A Python client for the New York Times Campaign Finance API",
    long_description = README,
    author = "Derek Willis",
    author_email = "dwillis@gmail.com",
    py_modules = ['nytcampfin'],
    platforms=["any"],
    classifiers=[
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: BSD License",
                 "Natural Language :: English",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python",
                 "Topic :: Software Development :: Libraries :: Python Modules",
                 ],
)

