# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# HTTP Status
try:  # Python 3.5+
    from http import HTTPStatus
except ImportError:
    try:  # Python 3
        from http import client as HTTPStatus
    except ImportError:  # Python 2
        import httplib as HTTPStatus

# Stream request handler
try:  # Python 3
    from socketserver import StreamRequestHandler, TCPServer, ThreadingMixIn
except ImportError:  # Python 2
    from SocketServer import StreamRequestHandler, TCPServer, ThreadingMixIn

# HTTP Request handler
try:  # Python 3
    from http.server import BaseHTTPRequestHandler
except ImportError:  # Python 2
    from BaseHTTPServer import BaseHTTPRequestHandler

# BytesIO
try:  # Python 3
    from io import BytesIO
except ImportError:  # Python 2
    from StringIO import StringIO as BytesIO
