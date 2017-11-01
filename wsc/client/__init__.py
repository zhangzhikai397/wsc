# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests


class PublishException(Exception):
    pass


class PublishResponse(object):
    def __init__(self, data):
        self._raw = data or dict()

        self.status = data.get('status')
        self.sent_bytes = data.get('content_length', 0)
        self.channel_id = data.get('channel_id', '/')
        self.recipients = data.get('recipients', 0)

    @property
    def raw(self):
        return self._raw


class StatResponse(object):
    def __init__(self, data):
        self._raw = data or dict()

        stat = data.get('stat', dict())
        self.channel_id = data.get('channel_id', '/')
        self.peers = stat.get('peers', 0)
        self.sent_bytes = stat.get('sent_bytes', 0)
        self.sent_messages = stat.get('sent_messages', 0)

    @property
    def raw(self):
        return self._raw


class WSC(object):
    """
    WebSocketChannel library
    """
    def __init__(self, access_key=None, hostname='127.0.0.1', port=8088):
        """
        Create client instance
        :param hostname:
        :param port:
        """
        self._access_key = access_key
        self._base_url = 'http://{}:{}/'.format(hostname, port)

    def get_endpoint(self, channel_id):
        """
        Returns endpoint for selected channel
        :param channel_id:
        :return:
        """
        return '{}{}'.format(
            self._base_url, channel_id.strip('/').lower()
        )

    def send(self, channel_id='/', message=''):
        """
        Send message to server
        :param channel_id:
        :param message:
        :return PublishResponse:
        """
        response = requests.post(
            self.get_endpoint(channel_id),
            data=message,
            headers={
                'Access-Key': self._access_key
            }
        )

        if response.status_code == 201:
            return PublishResponse(response.json())
        raise PublishException('Failed to post message: {}'.format(
            response.json().get('status', 'Unknown exception'))
        )

    def stat(self, channel_id='/'):
        """
        Returns channel statistic
        :param channel_id:
        :return StatResponse:
        """
        response = requests.get(
            self.get_endpoint(channel_id),
            headers={
                'Access-Key': self._access_key
            }
        )

        return StatResponse(response.json())
