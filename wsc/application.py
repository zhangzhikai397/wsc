# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from wsc.server import Server
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('access_key', help='HTTP API Server Access Key', type=str)
parser.add_argument('--host', help='Server hostname', default='0.0.0.0', type=str)
parser.add_argument('--port', help='Server port number', default=8088, type=int)


def run_server():
    args = parser.parse_args()
    server = Server(
        access_key=args.access_key,
        hostname=args.host,
        port=args.port
    )

    server.serve_forever()
