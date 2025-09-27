import pytest
from linkfinder import check_url

@pytest.mark.parametrize("input_url", [
    ("/abc",),
    ("/abc.py",),
    ("/abc/def.py",),
    ("abc",),
    ("abc.py",),
    ("abc/def.py",),
    ("abc/def.js.py",)
])
def test_check_url_not_js_returns_false(input_url):
    actual = check_url(input_url, input="http://example.com")

    assert actual == False

@pytest.mark.parametrize("input_url", [
    ("/node_modules/abc.js",),
    ("node_modules/abc.js",),
    ("/abc/node_modules/def.js",),
    ("abc/node_modules/def.js",),
])
def test_check_url_node_module_returns_false(input_url):
    actual = check_url(input_url, input="http://example.com")

    assert actual == False

@pytest.mark.parametrize("input_url", [
    ("/abc.jquery.js",),
    ("/abc/def.jquery.js",),
    ("abc.jquery.js",),
    ("abc/def.jquery.js",),
])
def test_check_url_jquery_returns_false(input_url):
    actual = check_url(input_url, input="http://example.com")

    assert actual == False

@pytest.mark.parametrize("input_url,input_domain,expected", [
    ("//example.com/script.js","https://example.com","https://example.com/script.js"),
    ("https://example2.com/script.js", "https://example1.com", "https://example2.com/script.js"),
    ("js/script.js", "https://example.com", "https://example.com/js/script.js"),
    ("js/script.js", "http://example.com", "http://example.com/js/script.js"),
    ("/js/script.js", "https://example.com", "https://example.com/js/script.js"),
    ("/js/script.js", "http://example.com", "http://example.com/js/script.js")
])
def test_check_url_valid_returns_correct_url(input_url, input_domain, expected):
    actual = check_url(input_url, input_domain)

    assert actual == expected