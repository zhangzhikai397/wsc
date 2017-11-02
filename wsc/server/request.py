# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class RequestParser(object):
    MAX_BODY_SIZE = 1024*1024
    HEADER_SIZE = 1024*16

    def __init__(self, request):
        """
        Socket read manager
        :param socket:
        """
        self._req = request
        self._package_buffer = b''
        self._headers = dict()
        self._body = ''

        self._http = 'HTTP/1.1'
        self._path = '/'
        self._method = 'get'

        self._read()
        self._parse()

    @property
    def raw(self):
        """
        Returns raw request
        :return:
        """
        return self._package_buffer

    @property
    def http(self):
        """
        Returns HTTP Version
        :return:
        """
        return self._http

    @property
    def path(self):
        """
        Returns request URI
        :return:
        """
        return self._path

    @property
    def method(self):
        """
        Returns request method
        :return:
        """
        return self._method

    @property
    def body(self):
        """
        Returns request body
        :return:
        """
        body = self._package_buffer.decode('utf-8').split('\r\n\r\n', 1)
        return body[1] if len(body) > 1 else ''

    @property
    def headers(self):
        """
        Returns headers dict
        :return dict:
        """
        return self._headers

    def _read(self, max_size=MAX_BODY_SIZE):
        """
        Read
        :param max_size:
        :return:
        """
        if len(self._package_buffer) > 0:
            return self._package_buffer

        # Read headers
        headers, body_start = self._read_part()
        self._package_buffer += (b'\r\n'*2).join([headers, body_start])

        # Read body
        self._parse()
        content_length = int(self.headers.get('content-length', 0)) - len(body_start)
        if content_length > 0:
            self._package_buffer += self._req.recv(content_length if content_length <= max_size else max_size)
        return self._package_buffer

    def _read_part(self):
        """
        Reads headers and then body
        :return:
        """
        sep = b'\r\n'*2

        # Read headers
        buffer = self._req.recv(self.HEADER_SIZE)
        while sep not in buffer:
            chunk = self._req.recv(self.HEADER_SIZE)
            buffer += chunk
            if len(chunk) < self.HEADER_SIZE:
                break
        buffer = tuple(buffer.split(sep, 1))
        return buffer if len(buffer) == 2 else tuple([buffer[0], b''])

    def _parse(self):
        """
        Parse headers
        :return:
        """
        headers = self._package_buffer.decode('utf-8').split('\r\n\r\n', 1)[0]
        for index, line in enumerate(headers.split('\r\n')):
            # Process head line
            if index == 0:
                head = tuple(line.split())
                if len(head) < 3:
                    print('Weired head: {}'.format(line))
                    method, uri, http = ('GET', '/', 'HTTP/1.1')
                else:
                    method, uri, http = head

                self._method = method.lower().strip()
                self._path = uri.lower().strip()
                self._http = http.strip()
                continue

            # Process other headers
            key, value = line.split(':', 1)
            self._headers[key.lower().strip()] = value.strip()
