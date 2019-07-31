.. image:: https://travis-ci.org/ClearcodeHQ/querystringsafe_base64.svg?branch=v1.2.0
    :target: https://travis-ci.org/ClearcodeHQ/querystringsafe_base64
    :alt: Tests

.. image:: https://coveralls.io/repos/ClearcodeHQ/querystringsafe_base64/badge.png?branch=v1.2.0
    :target: https://coveralls.io/r/ClearcodeHQ/querystringsafe_base64?branch=v1.2.0
    :alt: Coverage Status

Query string safe Base64
========================

Encoding and decoding arbitrary strings into strings that are safe to put into a URL query param.

The problem
-----------

`urlsafe_b64encode` and `urlsafe_b64decode` from base64 are not enough because they leave `=` used for padding chars unquoted:

.. code-block:: python

    import base64

    base64.urlsafe_b64encode('a')
    'YQ=='

And there are 2 problems with that

I. `=` sign gets quoted:

.. code-block:: python

    import urllib

    urllib.quote('=')
    '%3D'

II. Some libraries tolerate the `=` in query string values:

.. code-block:: python

    from urlparse import urlsplit, parse_qs

    parse_qs(urlsplit('http://aaa.com/asa?q=AAAA=BBBB=CCCC').query)
    {'q': ['AAAA=BBBB=CCCC']}

but the RFC 3986 underspecifies the query string so we cannot rely on `=` chars being handled by all web applications as it is done by urlparse.

Therefore we consider chars: `['+', '/', '=']` unsafe and we replace them with `['-', '_', '.']`.
Characters `+` and `/` are already handled by `urlsafe_*` functions from base64 so only `=` is left.
Since the `=` is used exclusively for padding, we simply remove it, and re-attach the padding during decoding.
Because of that, `querystringsafe_base64` is able to decode padded and unpadded string.

The solution
------------

.. code-block:: python

    import querystringsafe_base64

    querystringsafe_base64.encode(b'foo-bar')
    b'Zm9vLWJhcg'

    querystringsafe_base64.decode(b'Zm9vLWJhcg..')
    b'foo-bar'

    querystringsafe_base64.decode(b'Zm9vLWJhcg')
    b'foo-bar'
