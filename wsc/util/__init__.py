import six
import sys
from importlib import import_module


def get_bytes(str_o):
    """
    Returns bytes
    :param str str_o:
    :return bytes:
    """
    return str.encode(str_o)


def get_string(bytes_o):
    """
    Returns str
    :param bytes bytes_o:
    :return str:
    """
    return bytes_o.decode()


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
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return False


def recv_chunks(sock, chunk_size=1024, max_size=None):
    """
    Receive chunks generator
    :param sock:
    :param int chunk_size:
    :param int max_size:
    :return:
    """
    chunk = sock.recv(chunk_size)
    yield chunk

    while len(chunk) == chunk_size or (max_size is not None and len(chunk) >= max_size):
        chunk = sock.recv(chunk_size)
        yield chunk


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        msg = "%s doesn't look like a module path" % dotted_path
        six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError:
        msg = 'Module "%s" does not define a "%s" attribute/class' % (
            module_path, class_name)
        six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])

