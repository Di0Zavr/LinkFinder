import gzip
import io
import importlib
import pytest
import types

linkfinder = importlib.import_module("linkfinder")

class FakeInfo:
    def __init__(self, encoding):
        self._encoding = encoding
    def get(self, name):
        if name == 'Content-Encoding':
            return self._encoding
        return None

class FakeResponseGzip:
    def __init__(self, payload_bytes):
        self._payload = payload_bytes
    def info(self):
        return FakeInfo('gzip')
    def read(self):
        # return gzip-compressed bytes
        buf = io.BytesIO()
        with gzip.GzipFile(fileobj=buf, mode='wb') as gz:
            gz.write(self._payload)
        return buf.getvalue()

class FakeResponsePlain:
    def __init__(self, payload_bytes):
        self._payload = payload_bytes
    def info(self):
        return FakeInfo(None)
    def read(self):
        return self._payload

class FakeResponseDeflate:
    def __init__(self, payload_bytes):
        self._payload = payload_bytes
    def info(self):
        return FakeInfo('deflate')
    def read(self):
        # return an object that has a read() method (to match broken original code path)
        return types.SimpleNamespace(read=lambda: self._payload)


def test_send_request_handles_gzip(monkeypatch):
    expected = b'hello gzip'
    fake = FakeResponseGzip(expected)

    def fake_urlopen(req, timeout, context):
        return fake

    monkeypatch.setattr(linkfinder, 'urlopen', fake_urlopen)

    result = linkfinder.send_request('http://example.com', cookies=None, timeout=5)
    assert isinstance(result, str)
    assert result == expected.decode('utf-8')


def test_send_request_handles_plain(monkeypatch):
    expected = b'plain text'
    fake = FakeResponsePlain(expected)

    def fake_urlopen(req, timeout, context):
        return fake

    monkeypatch.setattr(linkfinder, 'urlopen', fake_urlopen)

    result = linkfinder.send_request('http://example.com', cookies=None, timeout=5)
    assert result == expected.decode('utf-8')


def test_send_request_handles_deflate(monkeypatch):
    expected = b'deflated text'
    fake = FakeResponseDeflate(expected)

    def fake_urlopen(req, timeout, context):
        return fake

    monkeypatch.setattr(linkfinder, 'urlopen', fake_urlopen)

    result = linkfinder.send_request('http://example.com', cookies=None, timeout=5)
    assert result == expected.decode('utf-8')
