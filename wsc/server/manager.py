# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class ConnectionItem(object):
    """
    Connection item wrapper
    """
    def __init__(self, handler, addr):
        """
        Instance
        :param Connection handler handler:
        :param addr:
        """
        self._addr = addr
        self._handler = handler

    def send(self, content):
        """
        Send message
        :param content:
        :return:
        """
        try:
            self._handler.send_text(content)
        except Exception as e:
            self._handler.finish()

    def disconnect(self):
        """
        Disconnect socket
        :return:
        """
        try:
            self._handler.close()
        except Exception as e:
            pass


class ConnectionList(object):
    """
    Connections list manager
    """
    def __init__(self):
        """
        List instance
        """
        self._connections = set()

    def send(self, content):
        """
        Send content to each connection
        :param content:
        :return:
        """
        for conn in self._connections:
            conn.send(content)

    def disconnect(self):
        """
        Disconnect and remove all connections
        :return:
        """
        for conn in self._connections:
            conn.disconnect()
            self.remove(conn)

    def add(self, handler, addr=None):
        """
        Add new peer
        :param handler:
        :param addr:
        :return:
        """
        item = self._get_item_instance(handler, addr)
        self._connections.add(item)

    def remove(self, handler, addr=None):
        """
        Disconnect and remove peer
        :param handler:
        :param addr:
        :return:
        """
        item = self._get_item_instance(handler, addr)
        item.disconnect()

        self._connections.remove(item)

    @staticmethod
    def _get_item_instance(handler, addr=None):
        """
        Returns ConnectionItem instance
        :param handler:
        :param addr:
        :return ConnectionItem:
        """
        return handler if isinstance(handler, ConnectionItem) else ConnectionItem(handler, addr)


class ConnectionsManger(object):
    """
    Connections queue manager
    """
    def __init__(self):
        """
        Connections queue instance
        """
        self._channels = dict()

    def send(self, queue_id, message):
        """
        Sends message to selected queue
        :param str queue_id:
        :param any message:
        :return:
        """
        if queue_id in self._channels:
            self._channels[queue_id].send(message)

    def disconnect(self, queue_id):
        """
        Disconnect from the queue
        :param str queue_id:
        :return:
        """
        if queue_id in self._channels:
            self._channels[queue_id].disconnect()

    def add_peer(self, queue_id, handler, addr=None):
        """
        Add new peer to queue
        :param str queue_id:
        :param handler:
        :param addr:
        :return:
        """
        if queue_id not in self._channels:
            self._channels[queue_id] = ConnectionList()

        self._channels[queue_id].add(handler, addr)

    def remove_peer(self, handler, addr=None):
        """
        Remove peer to queue
        :param handler:
        :param addr:
        :return:
        """
        for cid, clist in self._channels.items():
            clist.remove(handler, addr)

    def get_list(self, queue_id):
        """
        Returns queue connections list
        :param queue_id:
        :return:
        """
        return self._channels.get(queue_id, ConnectionList())

    @property
    def queues(self):
        """
        Queues names list
        :return:
        """
        return self._channels.keys()

    @property
    def channels(self):
        """
        Returns queues names and connection lists
        :return:
        """
        return self._channels.items()
