import pytest
import pyfakefs
from pyfakefs.fake_filesystem import OSType
from linkfinder import parser_input

@pytest.fixture
def linux_fake_filesystem(fs):
    fs.os = OSType.LINUX

    fs.create_dir("/abc/a")
    fs.create_dir("/abc/b")
    fs.create_dir("/abc/c")
    fs.create_dir("/def/d")
    fs.create_dir("/ghi")

    fs.create_file("/file1.js")
    fs.create_file("/file2.js")
    fs.create_file("/file3.js")
    fs.create_file("/abc/a/file4.js")
    fs.create_file("/abc/a/file5.js")
    fs.create_file("/abc/b/file6.js")
    fs.create_file("/abc/file7.js")
    fs.create_file("/def/d/file8.js")
    fs.create_file("/def/d/file9.js")
    fs.create_file("/def/d/file10.js")
    fs.create_file("/ghi/file_11.js")
    fs.create_file("/ghi/file_111.js")

    yield fs

@pytest.mark.parametrize("input,expected", [
    ("http://example.com", "http://example.com"),
    ("https://example.com", "https://example.com"),
    ("ftp://ftpserver/file", "ftp://ftpserver/file"),
    ("ftps://secure.ftpserver/file", "ftps://secure.ftpserver/file"),
    ("file:///etc/passwd", "file:///etc/passwd")
])
def test_parser_input_url_returns_same(input, expected):
    actual = parser_input(input)
    
    assert actual.__class__.__name__ == "list"
    assert len(actual) == 1
    assert actual[0] == expected

@pytest.mark.parametrize("input,expected", [
    ("view-source:https://example.com/", "https://example.com/")
])
def test_parser_input_view_source_removed(input, expected):
    actual = parser_input(input)

    assert actual.__class__.__name__ == "list"
    assert len(actual) == 1
    assert actual[0] == expected

@pytest.mark.parametrize("input,expected", [
    ("/*", ["file:///file1.js", "file:///file2.js", "file:///file3.js"]),
    ("/abc/*.js", ["file:///abc/file7.js"]),
    ("/abc/a/file*", ["file:///abc/a/file4.js", "file:///abc/a/file5.js"]),
    ("/abc/**/", ["file:///abc/file7.js"]),
    ("/def/**/*.js", ["file:///def/d/file8.js", "file:///def/d/file9.js", "file:///def/d/file10.js"]),
])
def test_parser_input_wildcard_returns_paths(input, expected, linux_fake_filesystem):
    actual = parser_input(input)
    actual.sort()
    expected.sort()
    
    assert actual.__class__.__name__ == "list"
    assert len(actual) == len(expected)
    assert all(actual_path == expected_path for actual_path, expected_path in zip(actual, expected))

@pytest.mark.parametrize("input,expected", [
    ("/file1.js", "file:///file1.js"),
    ("/abc/./a/file4.js", "file:///abc/a/file4.js"),
    ("/abc/../ghi/file_11.js", "file:///ghi/file_11.js"),
    ("/./abc/../ghi/file_11.js", "file:///ghi/file_11.js"),
    ("/./abc/./../def/../ghi/./file_111.js", "file:///ghi/file_111.js")
])
def test_parser_input_filename_returns_file_wrapper(input, expected, linux_fake_filesystem):
    actual = parser_input(input)
    
    assert actual.__class__.__name__ == "list"
    assert len(actual[0]) == len(expected)
    assert actual[0] == expected
