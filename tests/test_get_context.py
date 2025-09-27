import pytest
from linkfinder import getContext

content = "one\ntwo three\nfour five six\nseven eight nine ten"

@pytest.mark.parametrize("matches", [
    [("two", 4, 7)],
])
def test_get_context_returns_list_of_dicts(matches):
    actual = getContext(matches, content)

    assert actual.__class__.__name__ == "list"
    assert all([item.__class__.__name__ == "dict" for item in actual])
    assert all([item.get("link") for item in actual])
    assert all([item.get("context") for item in actual])

@pytest.mark.parametrize("matches,expected", [
    ([("two", 4, 7)], [{"link": "two", "context": "two three"}]),
    ([("two", 4, 7), ("five", 19, 23)], [{"link": "two", "context": "two three"}, {"link": "five", "context": "four five six"}]),
    ([("two", 4, 7), ("five", 19, 23), ("six", 24, 27)], [{"link": "two", "context": "two three"}, {"link": "five", "context": "four five six"}, {"link": "six", "context": "four five six"}]),
])
def test_get_context_returns_context(matches, expected):
    actual = getContext(matches, content)

    assert len(matches) == len(actual)
    assert all([actual[index]["link"] == expected[index]["link"] for index in range(len(expected))])
    assert all([actual[index]["context"] == expected[index]["context"] for index in range(len(expected))])

@pytest.mark.parametrize("matches,expected", [
    ([("one", 0, 3)], [{"link": "one", "context": "one"}]),
    ([("ten", 45, 48)], [{"link": "ten", "context": "seven eight nine ten"}]),
    ([("one", 0, 3), ("eight", 34, 39)], [{"link": "one", "context": "one"}, {"link": "eight", "context": "seven eight nine ten"}])
])
def test_get_context_no_edge_delimeter_returns_full_content(matches, expected):
    actual = getContext(matches, content)

    assert all([actual[index]["context"] == expected[index]["context"] for index in range(len(expected))])

@pytest.mark.parametrize("matches,expected", [
    ([("two", 4, 7)], [{"link": "two", "context": "\ntwo three\n"}]),
    ([("two", 4, 7), ("five", 19, 23)], [{"link": "two", "context": "\ntwo three\n"}, {"link": "five", "context": "\nfour five six\n"}]),
    ([("one", 0, 3), ("nine", 40, 44)], [{"link": "one", "context": "one\n"}, {"link": "nine", "context": "\nseven eight nine ten"}])
])
def test_get_context_include_delimeter_returns_context_with_delimeter(matches, expected):
    actual = getContext(matches, content, include_delimiter=1)

    assert all([actual[index]["context"] == expected[index]["context"] for index in range(len(expected))])
