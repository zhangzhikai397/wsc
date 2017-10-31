# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from wsc.client import WSC


if __name__ == '__main__':
    w = WSC('key')
    w.send('main/room', 'Hello')
