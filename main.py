# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from wsc.server import Server


if __name__ == '__main__':
    s = Server()
    s.serve_forever()
