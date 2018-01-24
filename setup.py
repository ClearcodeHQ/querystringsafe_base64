#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2016 by Clearcode <http://clearcode.cc>
# and associates (see AUTHORS.rst).

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
from setuptools import setup

here = os.path.dirname(__file__)

def read(fname):
    """
    Read given file's content.

    :param str fname: file name
    :returns: file contents
    :rtype: str
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
    version='1.0.0',
    author='Clearcode - The A Room',
    author_email='thearoom@clearcode.cc',
    description='Encoding and decoding arbitrary strings into strings '
    'that are safe to put into a URL query param.',
    long_description=(
            read('README.rst') + '\n\n' + read('CHANGES.rst')
    ),
    py_modules=['querystringsafe_base64', ],

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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',  # noqa
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
    ],
)
