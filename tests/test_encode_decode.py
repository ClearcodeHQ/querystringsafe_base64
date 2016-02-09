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
"""querystringsafe_base64's tests."""

import sys
from base64 import b64encode, b64decode, urlsafe_b64decode
import string
try:
    from urllib import quote_plus, unquote_plus
except ImportError:
    from urllib.parse import quote_plus, unquote_plus

import pytest
import querystringsafe_base64

PY2 = sys.version_info < (3, 0)

# We want to test querystringsafe_base64.encode with a string that normally
# encodes to a URL-unsafe base64 so we obtain it by decoding a manually created
# base64 string with all the unsafe chars.
if PY2:
    url_unsafe_string_short = b64decode('aDaF+/===')  # Unsafe chars: +, /, =
else:
    url_unsafe_string_short = b64decode('aDbChcO7'.encode('UTF-8')).decode('UTF-8')  # Unsafe chars: +, /, =

# Creating a synthetic base64 that contains all base64 characters:
base64_alphabet = string.ascii_letters + string.digits + '+/'
assert len(base64_alphabet) == 64
# base64 alphabet is already a valid base64 string but it does not contain
# all allowed characters - '=' (padding) is missing. So add it.
base64_string_with_all_allowed_chars = base64_alphabet + 'aa=='
if PY2:
    string_encoding_to_base64_with_all_allowed_characters = b64decode(
        base64_string_with_all_allowed_chars
    )
else:
    string_encoding_to_base64_with_all_allowed_characters = b64decode(
        b64encode(base64_string_with_all_allowed_chars.encode('UTF-8')).decode('UTF-8')
    ).decode()

# Strings to test with. They decode to base64 that would be unsafe in url and
# would have to be escaped. The short string, unlike the long one, will be
# fully shown in tracebacks when --showlocals is used.
test_strings = [
    url_unsafe_string_short,
    string_encoding_to_base64_with_all_allowed_characters
]

# Test strings are unsafe to print - they potentially contain all the nasty
# characters, including '\r' and '\0'. Py.test does not excape them in its
# output, so we address them by indices.
test_strings_indices = range(len(test_strings))


@pytest.mark.parametrize('string_num', test_strings_indices)
def test_encode_decode(string_num):
    """Check if querystringsafe_base64.encode can be reverted by querystringsafe_base64.decode."""
    original = test_strings[string_num]

    encoded = querystringsafe_base64.encode(original)
    decoded = querystringsafe_base64.decode(encoded)
    assert decoded == original


@pytest.mark.parametrize('string_num', test_strings_indices)
def test_encode_result_is_agnostic_to_url_quoting(string_num):
    """Test if querystringsafe_base64.encode returns a string that does not have characters that must be quoted."""
    original = test_strings[string_num]

    # quoting and unquoting has no impact on base64dotted:
    safe_encoded = querystringsafe_base64.encode(original)
    assert safe_encoded == quote_plus(safe_encoded)
    assert safe_encoded == unquote_plus(safe_encoded)

    # base64 has to be quoted:
    url_encoded = b64encode(original)
    assert url_encoded != quote_plus(url_encoded)


def test_decode_accepts_regular_base64():
    """Check if querystringsafe_base64.decode can also decode standard base64."""
    # Check if we test with a regular base64 that has all the unsafe chars:
    for char in ['+', '/', '=']:
        assert char in base64_string_with_all_allowed_chars
    assert (
        querystringsafe_base64.decode(
            base64_string_with_all_allowed_chars
        ) == string_encoding_to_base64_with_all_allowed_characters)


def test_querystringsafe_base64_decode_handles_unicode():
    """
    Base64.urlsafe_b64decode called by querystringsafe_base64.decode complains about unicode being passed.

    Check if querystringsafe_base64.decodefixes it.
    """
    base64_unicode = u'DD=='
    base64_str = str(base64_unicode)
    base64dotted_unicode = u'DD..'
    base64dotted_str = str(base64_unicode)

    # urlsafe_b64decode can handle str but breaks on unicode.
    decoded_str = urlsafe_b64decode(base64_str)
    with pytest.raises(TypeError):
        urlsafe_b64decode(base64_unicode)

    # querystringsafe_base64.decode handles str and unicode in both formats.
    assert querystringsafe_base64.decode(base64_unicode) == decoded_str
    assert querystringsafe_base64.decode(base64_str) == decoded_str
    assert querystringsafe_base64.decode(base64dotted_unicode) == decoded_str
    assert querystringsafe_base64.decode(base64dotted_str) == decoded_str
