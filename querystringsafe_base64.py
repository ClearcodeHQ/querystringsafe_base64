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
"""Main querystringsafe_base64 module."""

import sys
from base64 import urlsafe_b64encode, urlsafe_b64decode

__version__ = '0.2.0'
PY2 = sys.version_info < (3, 0)


def fill_padding(padded_string):
    """
    Fill up missing padding in a string.

    This function makes sure that the string has length which is multiplication of 4,
    and if not, fills the missing places with dots.

    :param str padded_string: string to be decoded that might miss padding dots.
    :return: properly padded string
    :rtype: str
    """
    length = len(padded_string)
    reminder = len(padded_string) % 4
    if reminder:
        return padded_string.ljust(length + 4 - reminder, '.')
    return padded_string


def encode(to_encode):
    """
    Encode an arbitrary string as a base64 that is safe to put as a URL query value.

    urllib.quote and urllib.quote_plus do not have any effect on the
    result of querystringsafe_base64.encode.

    :param (str, bytes) to_encode:
    :rtype: str
    :return: a string that is safe to put as a value in an URL query
        string - like base64, except characters ['+', '/', '='] are
        replaced with ['-', '_', '.'] consequently
    """
    encoded = urlsafe_b64encode(to_encode).replace(b'=', b'.')
    if PY2:
        return encoded
    return encoded.decode()


def decode(encoded):
    """
    Decode the result of querystringsafe_base64_encode or a regular base64.

    .. note ::
        As a regular base64 string does not contain dots, replacing dots with
        equal signs does basically noting to it. Also,
        base64.urlsafe_b64decode allows to decode both safe and unsafe base64.
        Therefore this function may also be used to decode the regular base64.

    :param (str, unicode) encoded: querystringsafe_base64 string or unicode
    :rtype: str, bytes
    :return: decoded string
    """
    padded_string = fill_padding(encoded)
    if PY2:
        return urlsafe_b64decode(str(padded_string).replace('.', '='))
    return urlsafe_b64decode(bytes(padded_string, 'ascii').replace(b'.', b'='))
