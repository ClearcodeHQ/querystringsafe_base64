#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2016 by Clearcode <http://clearcode.cc>
# and associates (see AUTHORS.md).

# This file is part of querystringsafe_base64.

# querystringsafe_base64 is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.

# querystringsafe_base64 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with querystringsafe_base64. If not, see <http://www.gnu.org/licenses/
"""querystringsafe_base64's installation module."""

import os
import re
from setuptools import setup, find_packages


here = os.path.dirname(__file__)
with open(
    os.path.join(here, 'src', 'querystringsafe_base64.py')
) as v_file:
    package_version = re.compile(
        r".*__version__ = '(.*?)'", re.S).match(v_file.read()).group(1)


try:
    from pypandoc import convert

    def read(fname):
        """
        Read filename.

        :param str fname: name of a file to read
        """
        return convert(os.path.join(here, fname), 'rst')
except ImportError:
    print(
        "warning: pypandoc module not found, could not convert Markdown to RST"
    )

    def read(fname):
        """
        Read filename.

        :param str fname: name of a file to read
        """
        return open(os.path.join(here, fname)).read()


test_requires = [
    'pytest',
    'pytest-cov',
    'pylama',
]

extras_require = {
    'tests': test_requires
}

setup(
    name='querystringsafe_base64',
    version=package_version,
    author='Clearcode - The A Room',
    author_email='@'.join(['thearoom', 'clearcode.cc']),
    description='Encoding and decoding arbitrary strings into strings '
    'that are safe to put into a URL query param.',
    long_description=read('README.md'),

    packages=find_packages('src'),
    package_dir={'': 'src'},

    url='https://github.com/ClearcodeHQ/querystringsafe_base64',
    include_package_data=True,
    install_requires=[],
    extras_require=extras_require,
    tests_require=test_requires,
    zip_safe=False,

    license="LGPL",
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',  # noqa
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
    ],
)
