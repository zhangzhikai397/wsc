# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import ssl
import logging
import wsc.logging
from wsc.server.protocol import Adapter
from wsc.server.handler import ConnectionHandler
from wsc.server.manager import ConnectionsManger
from wsc.server.compatiblity import TCPServer, ThreadingMixIn


logger = logging.getLogger(__name__)
logging.basicConfig(**wsc.logging.config)


class Server(ThreadingMixIn, TCPServer):
    """
    WebSocket server
    """
    # Server options
    DEFAULT_HOST = '0.0.0.0'
    DEFAULT_PORT = 8088
    TLS_VERSION = ssl.PROTOCOL_TLSv1

    # TCP Server options
    allow_reuse_address = True
    daemon_threads = True
    request_queue_size = 100

    def __init__(self, hostname=DEFAULT_HOST, port=DEFAULT_PORT, access_key=None, ssl_cert=None, ssl_key=None):
        """
        Create server instance
        :param hostname:
        :param port:
        :param access_key:
        :param ssl_cert:
        :param ssl_key:
        """
        # SSL Context
        self.tls_enabled = ssl_cert and ssl_key
        self.ssl_cert = ssl_cert
        self.ssl_key = ssl_key

        if self.tls_enabled:
            logger.info('SSL Mode enabled. Creating context...')
            self.context = self._get_ssl_context()

        # Run TCP Server
        TCPServer.__init__(self, (hostname, port), ConnectionHandler)

        # Connections manager
        self.connections = ConnectionsManger()
        self.access_key = (access_key or '').strip()

        # Server information
        logger.warning('Server started on {}://{}:{}'.format(
            'wss' if self.tls_enabled else 'ws',
            hostname,
            port
        ))

        logger.warning('Server API Access KEY: {}'.format(access_key))
        logger.debug('Reuse ADDR:\t{}'.format(self.allow_reuse_address))
        logger.debug('TLS Enabled:\t{}'.format(self.tls_enabled))
        logger.debug('Daemon threads:\t{}'.format(self.daemon_threads))
        logger.debug('Request queue size:\t{}'.format(self.request_queue_size))

    def server_bind(self):
        """
        Wrap TLS
        :return:
        """
        if self.tls_enabled:
            logger.info('Wrapping socket using SSL...')
            self.socket = self.context.wrap_socket(self.socket, server_side=True)
        TCPServer.server_bind(self)

    def _get_ssl_context(self):
        """
        Creates new SSL context
        :return:
        """
        context = ssl.SSLContext(self.TLS_VERSION)
        context.load_cert_chain(self.ssl_cert, self.ssl_key)
        return context

    @staticmethod
    def set_option(opt_name, value):
        """
        Updates static option for server
        :param opt_name:
        :param value:
        :return:
        """
        assert hasattr(Server, opt_name), (
            "Attribute {} doesn't exists at "
            "Server class"
        ).format(opt_name)

        setattr(Server, opt_name, value)
