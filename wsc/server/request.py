# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from wsc.server.compatiblity import BaseHTTPRequestHandler, BytesIO


class HTTPRequest(BaseHTTPRequestHandler):
    """
    HTTP Request parser
    """
    def __init__(self, request_text, addr):
        """
        Parse headers
        :param request_text:
        """
        self.rfile = BytesIO(request_text)
        self.wfile = BytesIO()
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.client_address = addr
        self.parse_request()

        self._body = None

    @property
    def body(self):
        """
        Read body
        :return:
        """
        if self._body is None:
            self._body = self.rfile.read(int(self.headers.get('content-length', 0)))
        return self._body.decode('utf-8')
