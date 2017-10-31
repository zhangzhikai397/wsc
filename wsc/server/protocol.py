import base64
import hashlib


class Adapter(object):
    """
    Websocket protocol adapter
    """
    GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

    FIN = 0x80
    OPCODE = 0x0f
    MASKED = 0x80
    PAYLOAD_LEN = 0x7f
    PAYLOAD_LEN_EXT16 = 0x7e
    PAYLOAD_LEN_EXT64 = 0x7f

    OPCODE_CONTINUATION = 0x0
    OPCODE_TEXT = 0x1
    OPCODE_BINARY = 0x2
    OPCODE_CLOSE_CONN = 0x8
    OPCODE_PING = 0x9
    OPCODE_PONG = 0xA

    @staticmethod
    def handshake(key):
        """
        Calculate handshake response
        :param key:
        :return:
        """
        hash = hashlib.sha1(key.encode() + Adapter.GUID.encode())
        response_key = base64.b64encode(hash.digest()).strip()
        return response_key.decode('ASCII')

    @staticmethod
    def handshake_response(key):
        """
        Get
        :param key:
        :return:
        """
        return \
            'HTTP/1.1 101 Switching Protocols\r\n' \
            'Upgrade: websocket\r\n' \
            'Connection: Upgrade\r\n' \
            'Sec-WebSocket-Accept: %s\r\n' \
            '\r\n' % Adapter.handshake(key)

    @staticmethod
    def process_ping(handler, msg):
        """
        Process ping request
        :param handler:
        :param msg:
        :return:
        """
        handler.send_text(msg, Adapter.OPCODE_PONG)

    @staticmethod
    def process_pong(handler, msg):
        """
        Process pong request
        :param handler:
        :param msg:
        :return:
        """
        pass

    @staticmethod
    def process_message(handler, msg):
        """
        Messages are not supported
        :param handler:
        :param msg:
        :return:
        """
        handler.send_text('Server doesn\'t support message processing')
