# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from wsc.client import WSC
from random import randint


if __name__ == '__main__':
    w = WSC('key')
    while True:
        print(w.send('main/room', 'Hello' + str(randint(0, 999999))).raw)
        print(w.stat('main/room').raw)
