import requests


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
        :return:
        """
        return requests.post(
            self.get_endpoint(channel_id),
            data=message,
            headers={
                'Access-Key': self._access_key
            }
        ).json()
