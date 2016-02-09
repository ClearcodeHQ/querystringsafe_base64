[![Build Status](https://travis-ci.org/ClearcodeHQ/querystringsafe_base64.svg?branch=master)](https://travis-ci.org/ClearcodeHQ/querystringsafe_base64)
[![Coverage Status](https://img.shields.io/coveralls/ClearcodeHQ/querystringsafe_base64.svg)](https://coveralls.io/r/ClearcodeHQ/querystringsafe_base64)

# Query string safe Base64

Encoding and decoding arbitrary strings into strings that are safe to put into a URL query param.

## The problem

`urlsafe_b64encode` and `urlsafe_b64decode` from base64 are not enough because they leave `=` chars unquoted:

    >>> import base64

    >>> base64.urlsafe_b64encode('a')
    >>> 'YQ=='

And there are 2 problems with that

I. `=` sign gets quoted:

    >>> import urllib

    >>> urllib.quote('=')
    '%3D'

II. Some libraries tolerate the `=` in query string values:

    >>> from urlparse import urlsplit, parse_qs

    >>> parse_qs(urlsplit('http://aaa.com/asa?q=AAAA=BBBB=CCCC').query)
    {'q': ['AAAA=BBBB=CCCC']}

but the RFC 3986 underspecifies the query string so we cannot rely on `=` chars being handled by all web applications as it is done by urlparse.

Therefore we consider chars: `['+', '/', '=']` unsafe and we replace them with `['-', '_', '.']`. Characters `+` and `/` are already handled by `urlsafe_*` functions from base64 so only `=` is left for us. The `.` character has been chosen because it often appears in real world query strings and it is not used
by base64.

## The solution

    >>> import querystringsafe_base64

    >>> querystringsafe_base64.encode('foo-bar')
    >>> 'Zm9vLWJhcg..'

    >>> querystringsafe_base64.decode('Zm9vLWJhcg..')
    >>> 'foo-bar'
