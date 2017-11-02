# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from wsc.server import Server
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('access_key', help='HTTP API Server Access Key', type=str)
parser.add_argument('--host', help='Server hostname', default='0.0.0.0', type=str)
parser.add_argument('--port', help='Server port number', default=8088, type=int)
parser.add_argument('--ssl-key', help='Path to SSL key file', default=None, type=str)
parser.add_argument('--ssl-cert', help='Path to SSL cert file', default=None, type=str)


def run_server():
    args = parser.parse_args()
    server = Server(
        access_key=args.access_key,
        hostname=args.host,
        port=args.port,
        ssl_key=args.ssl_key,
        ssl_cert=args.ssl_cert
    )

    try:
        server.serve_forever(poll_interval=0.05)
    except KeyboardInterrupt:
        print('Shutting down connections...')
        server.connections.disconnect()
        server.server_close()
