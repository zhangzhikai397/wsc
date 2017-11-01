# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from wsc.server.compatiblity import HTTPStatus as status


class JSONResponse(object):
    SERVER_NAME = 'WSC 1.0/Python 3'

    def __init__(self, status_code=status.OK, **data):
        self.status = status_code
        self.content = json.dumps(data)

    def get_status(self):
        if hasattr(self.status, 'value') and hasattr(self.status, 'phrase'):
            return ' '.join([str(self.status.value), self.status.phrase])
        return ' '.join([str(self.status), status.responses[self.status]])

    @property
    def document(self):
        return (
            "HTTP/1.1 {status}\r\n"
            "Server: {server}\r\n"
            "Content-Length: {content_length}\r\n"
            "Content-Type: application/json\r\n"
            "Connection: Closed\r\n\r\n"
            "{content}"
        ).format(
            status=self.get_status(),
            server=self.SERVER_NAME,
            content=self.content,
            content_length=len(self.content),
        )

    @property
    def bytes(self):
        return self.document.encode('utf-8')
