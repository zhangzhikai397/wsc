# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import struct
import logging
import wsc.logging
from wsc.server.api import APIHandler
from wsc.server.protocol import Adapter
from wsc.server.request import RequestParser
from wsc.server.compatiblity import StreamRequestHandler
from wsc.util import unicode_decodeable, unicode_encodable, to_unicode, is_unicode


logger = logging.getLogger(__name__)
logging.basicConfig(**wsc.logging.config)


class ConnectionHandler(StreamRequestHandler):
    """
    Connections handler
    """

    def __init__(self, socket, addr, server):
        """
        Initialize connection handler
        :param socket:
        :param addr:
        :param server:
        """
        self.server = server
        self.keep_alive = True
        self.valid_client = False
        self.handshake_done = False
        self.is_subscribed = False
        self.rp = None
        StreamRequestHandler.__init__(self, socket, addr, server)

    def setup(self):
        """
        Setup connection
        :return:
        """
        StreamRequestHandler.setup(self)
        self.keep_alive = True
        self.handshake_done = False
        self.valid_client = False

    def handle(self):
        """
        Dispatch request
        :return:
        """
        self.rp = RequestParser(self.request)
        while self.keep_alive:
            if not self.handshake_done:
                self.handshake()
            elif self.valid_client:
                try:
                    self.read_next_message()
                except:
                    continue

    def handle_post(self):
        """
        Handle post request and serve message to channel
        subscribers
        :return:
        """
        APIHandler(self, self.rp).dispatch()

    def finish(self):
        """
        Close connection
        :return:
        """
        if self.is_subscribed:
            try:
                self.server.connections.remove_peer(self, self.client_address)
                logger.debug('Peer {}:{} removed from queue'.format(*self.client_address))
            except Exception as e:
                logger.error('{}: {}'.format(type(e).__name__, str(e)))

        try:
            super(ConnectionHandler, self).finish()
        except Exception as e:
            logger.error('{}: {}'.format(type(e).__name__, str(e)))

    def subscribe(self, message):
        """
        Adding new listener to channel
        :param message:
        :return:
        """
        try:
            channel_id = self.channel_id(message)
            self.server.connections.add_peer(channel_id, self, self.client_address)
            self.is_subscribed = True
            logger.debug('New peer {}:{} connected to channel: {}'.format(
                self.client_address[0], self.client_address[1], channel_id
            ))
        except Exception as e:
            logger.error('Failed to subscribe new peer {}:{} - {}'.format(
                self.client_address[0], self.client_address[1], str(e)
            ))

    def read_bytes(self, num):
        """
        Read NUM bytes
        :param num:
        :return:
        """
        return self.rfile.read(num)

    def read_next_message(self):
        """
        Read next message
        :return:
        """
        try:
            b1, b2 = self.read_bytes(2)
        except ValueError as e:
            b1, b2 = 0, 0

        fin = b1 & Adapter.FIN
        opcode = b1 & Adapter.OPCODE
        masked = b2 & Adapter.MASKED
        payload_length = b2 & Adapter.PAYLOAD_LEN

        # Wrong request type
        if not b1:
            self.keep_alive = 0
            return

        # Closed by peer
        if opcode == Adapter.OPCODE_CLOSE_CONN:
            self.keep_alive = 0
            return

        # Not masked
        if not masked:
            self.keep_alive = 0
            return

        # Request opcodes dispatcher
        if opcode == Adapter.OPCODE_CONTINUATION:
            return
        elif opcode == Adapter.OPCODE_BINARY:
            return
        elif opcode == Adapter.OPCODE_TEXT:
            opcode_handler = Adapter.process_message
        elif opcode == Adapter.OPCODE_PING:
            opcode_handler = Adapter.process_ping
        elif opcode == Adapter.OPCODE_PONG:
            opcode_handler = Adapter.process_pong
        else:
            logger.warn("Unknown opcode %#x." % opcode)
            self.keep_alive = 0
            return

        if payload_length == 126:
            payload_length = struct.unpack(">H", self.rfile.read(2))[0]
        elif payload_length == 127:
            payload_length = struct.unpack(">Q", self.rfile.read(8))[0]

        masks = self.read_bytes(4)
        decoded = ""
        for char in self.read_bytes(payload_length):
            char ^= masks[len(decoded) % 4]
            decoded += chr(char)
        opcode_handler(self, decoded)

    def send_text(self, message, opcode=Adapter.OPCODE_TEXT):
        """
        Important: Fragmented(=continuation) messages are not supported since
        their usage cases are limited - when we don't know the payload length.
        """
        # Validate message
        message = to_unicode(message)
        if isinstance(message, bytes):
            message = unicode_decodeable(message)  # this is slower but ensures we have UTF-8
            if not message:
                logger.warning("Can\'t send message, message is not valid UTF-8")
                return False
        elif is_unicode(message):
            pass
        else:
            logger.warning('Can\'t send message, message has to be a string or bytes. Given type is %s' % type(message))
            return False

        header = bytearray()
        payload = unicode_encodable(message)
        payload_length = len(payload)

        # Normal payload
        if payload_length <= 125:
            header.append(Adapter.FIN | opcode)
            header.append(payload_length)

        # Extended payload
        elif 126 <= payload_length <= 65535:
            header.append(Adapter.FIN | opcode)
            header.append(Adapter.PAYLOAD_LEN_EXT16)
            header.extend(struct.pack(">H", payload_length))

        # Huge extended payload
        elif payload_length < 16**16:
            header.append(Adapter.FIN | opcode)
            header.append(Adapter.PAYLOAD_LEN_EXT64)
            header.extend(struct.pack(">Q", payload_length))

        else:
            raise Exception("Message is too big. Consider breaking it into chunks.")

        self.request.send(header + payload)

    def handshake(self):
        """
        Should dispatch request and send handshake if needs
        :return:
        """
        message = self.rp.raw.decode('utf-8', errors='strict').strip()
        upgrade = re.search('\nupgrade[\s]*:[\s]*websocket', message.lower())

        if not upgrade:
            self.keep_alive = False
            self.handle_post()
            return

        key = re.search('\nsec-websocket-key[\s]*:[\s]*(.*)\r\n', message, re.I)
        if key:
            key = key.group(1)
        else:
            logger.warning("Client tried to connect but was missing a key")
            self.keep_alive = False
            return

        response = Adapter.handshake_response(key)
        self.handshake_done = self.request.send(response.encode('utf-8'))
        self.valid_client = True

        # Add new client
        self.subscribe(message)

    @staticmethod
    def channel_id(request_head):
        """
        Returns channel ID
        :return:
        """
        try:
            request_path = re.search(r'GET (.*) HTTP', request_head, re.I).group(1)
            return ConnectionHandler.filter_path(request_path)
        except Exception as e:
            return '/'

    @staticmethod
    def filter_path(path):
        """
        Returns filtered request URI
        :param path:
        :return:
        """
        return path.strip(' /').lower() or '/'
