import base64
import urllib.parse as urlparse


def base64_encode(data):
    return base64.b64encode(data).decode('utf-8')


def base64_decode(data):
    return str(base64.b64decode(data), 'utf-8')


def url_decode(data):
    return urlparse.unquote(data)


def url_encode(data):
    return urlparse.quote(data)

