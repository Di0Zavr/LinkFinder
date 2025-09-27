import pytest
from linkfinder import parser_file, regex_str 

TEST_CONTENT = """one two "http://example1.com"
\"index.php\"
three
four "https://example2.com"
five
    "/api/endpoint1", "/api/endpoint2", "/api/endpoint3"
six "index.php"
"/static/js/main.js"
seven eight "/get?path=/etc/passwd"
nine "//example3.com"
ten "/?param=test"
"index.php"
"index.php"
eleven "login.php"
twelve "register.php"
thirteen
"""

EXPECTED_LINKS = [
    {"link": "http://example1.com", "context": "one two \"http://example1.com\""},
    {"link": "index.php", "context": "\"index.php\""},
    {"link": "https://example2.com", "context": "four \"https://example2.com\""},
    {"link": "/api/endpoint1", "context": "    \"/api/endpoint1\", \"/api/endpoint2\", \"/api/endpoint3\""},
    {"link": "/api/endpoint2", "context": "    \"/api/endpoint1\", \"/api/endpoint2\", \"/api/endpoint3\""},
    {"link": "/api/endpoint3", "context": "    \"/api/endpoint1\", \"/api/endpoint2\", \"/api/endpoint3\""},
    {"link": "index.php", "context": "six \"index.php\""},
    {"link": "/static/js/main.js", "context": "\"/static/js/main.js\""},
    {"link": "/get?path=/etc/passwd", "context": "seven eight \"/get?path=/etc/passwd\""},
    {"link": "//example3.com", "context": "nine \"//example3.com\""},
    {"link": "/?param=test", "context": "ten \"/?param=test\""},
    {"link": "index.php", "context": "\"index.php\""},
    {"link": "index.php", "context": "\"index.php\""},
    {"link": "login.php", "context": "eleven \"login.php\""},
    {"link": "register.php", "context": "twelve \"register.php\""},
]

UNIQUE_LINKS = [
    "http://example1.com",
    "index.php",
    "https://example2.com",
    "/api/endpoint1",
    "/api/endpoint2",
    "/api/endpoint3",
    "/static/js/main.js",
    "/get?path=/etc/passwd",
    "//example3.com",
    "/?param=test",
    "login.php",
    "register.php",
]

def test_parser_file_returns_list_of_dicts():
    actual = parser_file(TEST_CONTENT, regex_str)

    assert actual.__class__.__name__ == "list"
    assert all([item.__class__.__name__ == "dict" for item in actual])

def test_parser_file_mode0_returns_only_links():
    actual = parser_file(TEST_CONTENT, regex_str, mode=0, no_dup=0)

    assert all([item.get("link") for item in actual])

    # no context
    assert not any([item.get("context") for item in actual])

    assert all([actual[index]["link"] == EXPECTED_LINKS[index]["link"] for index in range(len(EXPECTED_LINKS))])

def test_parser_file_mode1_returns_with_context():
    actual = parser_file(TEST_CONTENT, regex_str, mode=1, no_dup=0)

    assert all([item.get("link") for item in actual])
    assert all([item.get("context") for item in actual])

    assert all([actual[index]["link"] == EXPECTED_LINKS[index]["link"] for index in range(len(EXPECTED_LINKS))])
    assert all([actual[index]["context"] == EXPECTED_LINKS[index]["context"] for index in range(len(EXPECTED_LINKS))])

def test_parser_file_nodup_remove_duplicated():
    actual = parser_file(TEST_CONTENT, regex_str, mode=0, no_dup=1)
    actual_links = [item["link"] for item in actual]

    actual_links.sort()
    UNIQUE_LINKS.sort()
    assert len(actual) == len(UNIQUE_LINKS)
    assert all([actual_link == expected_link for actual_link, expected_link in zip(actual_links, UNIQUE_LINKS)])
    assert all([actual_link == expected_link for actual_link, expected_link in zip(actual_links, UNIQUE_LINKS)])