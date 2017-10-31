import logging
import wsc.logging
from wsc.server.protocol import Adapter
from wsc.server.handler import ConnectionHandler
from wsc.server.manager import ConnectionsManger
from socketserver import TCPServer, ThreadingMixIn


logger = logging.getLogger(__name__)
logging.basicConfig(**wsc.logging.config)


class Server(ThreadingMixIn, TCPServer):
    """
    WebSocket server
    """
    # Server options
    DEFAULT_HOST = '0.0.0.0'
    DEFAULT_PORT = 8088

    # TCP Server options
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, hostname=DEFAULT_HOST, port=DEFAULT_PORT, access_key=None):
        TCPServer.__init__(self, (hostname, port), ConnectionHandler)
        self.connections = ConnectionsManger()
        self.access_key = (access_key or '').strip()

        logger.warning('Server started on {}:{}'.format(hostname, port))
        logger.warning('Server API Access KEY: {}'.format(access_key))
