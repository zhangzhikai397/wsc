import json
from http.server import HTTPStatus as status


class HTTPResponse(object):
    SERVER_NAME = 'WSC 1.0/Python 3'

    def __init__(self, status=status.OK, **data):
        self.status = status
        self.content = json.dumps(data)

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
            status=' '.join([str(self.status.value), self.status.phrase]),
            server=self.SERVER_NAME,
            content=self.content,
            content_length=len(self.content),
        )

    @property
    def bytes(self):
        return self.document.encode()
