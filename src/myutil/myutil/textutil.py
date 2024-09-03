import base64
import urllib.parse as urlparse
from collections.abc import Buffer


def base64_encode(data: Buffer):
    return base64.b64encode(data).decode('utf-8')


def base64_decode(data: Buffer):
    return str(base64.b64decode(data), 'utf-8')


def url_decode(data: str):
    return urlparse.unquote(data)


def url_encode(data: str):
    return urlparse.quote(data)

