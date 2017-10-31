# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def unicode_encodable(data):
    """
    Check is can be encoded to unicode
    :param data:
    :return:
    """
    try:
        return data.encode('UTF-8')
    except UnicodeEncodeError as e:
        return False


def unicode_decodeable(data):
    """
    Tries to decode from unicode
    :param data:
    :return:
    """
    try:
        return data.decode('UTF-8', errors='strict')
    except UnicodeDecodeError:
        return False


def is_unicode(s):
    """
    Check is unicode
    :param s:
    :return:
    """
    return isinstance(s, __builtins__['unicode' if 'unicode' in __builtins__ else 'str'])


def to_unicode(s):
    """
    Convert str to unicode if needs
    :param s:
    :return:
    """
    return s.decode('utf-8') if not is_unicode(s) else s
