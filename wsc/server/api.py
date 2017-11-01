# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from wsc.server.response import JSONResponse, status


def authenticate(fn):
    """
    Check is request is authenticated
    :return:
    """

    def _method(self, *args, **kwargs):
        if self.request.headers.get('access-key', '').strip().lower() == self.handler.server.access_key:
            return fn(self, *args, **kwargs)
        return JSONResponse(status.UNAUTHORIZED, message="Not authorized")

    return _method


class APIHandler(object):
    def __init__(self, handler, request):
        """
        Init API Handler
        :param ConnectionHandler handler:
        :param HTTPRequest request:
        """
        self.request = request
        self.handler = handler

    @property
    def request_channel(self):
        """
        Returns channel ID
        :return:
        """
        return self.handler.filter_path(self.request.path)

    @property
    def connection_manager(self):
        """
        Returns connections manager
        :return ConnectionsManager:
        """
        return self.handler.server.connections

    def dispatch(self):
        """
        Dispatch request
        :return:
        """
        cmd = self.request.method.strip().lower()
        if hasattr(self, 'process_{}'.format(cmd)):
            response = getattr(self, 'process_{}'.format(cmd))(self.request_channel)
            if not isinstance(response, JSONResponse):
                return self.handler.request.send(
                    JSONResponse(status.INTERNAL_SERVER_ERROR, message="Invalid command response").bytes
                )

            return self.handler.request.send(response.bytes)

        return self.handler.request.send(
            JSONResponse(status.NOT_FOUND, message="Requested command is not found").bytes
        )

    @authenticate
    def process_post(self, channel):
        """
        Publish requested message
        :param str channel:
        :return:
        """
        try:
            message = self.request.body
            return JSONResponse(
                status_code=status.CREATED,
                channel_id=channel,
                status="Message sent",
                content_length=len(message),
                recipients=self.connection_manager.send(channel, message)
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.BAD_REQUEST,
                channel_id=channel,
                status="Error {}: {}".format(type(e).__name__, str(e))
            )

    @authenticate
    def process_get(self, channel):
        """
        Retrieve statistics
        :param str channel:
        :return:
        """
        return JSONResponse(
            status_code=status.OK,
            channel_id=channel,
            stat=dict(
                peers=self.connection_manager.connected_peers(channel),
                sent_messages=self.connection_manager.sent_messages(channel),
                sent_bytes=self.connection_manager.sent_bytes(channel)
            )
        )
