#!/usr/bin/env python3
from pytest import fixture

from object_colors import Color


@fixture
def all_colors():
    return Color(populate=True)


@fixture
def small_colored_string(all_colors, small_test_string):
    return all_colors.green.get(small_test_string)


@fixture()
def small_test_string():
    return "Cc: My Business <me@mybusiness.com>;"


@fixture()
def large_test_string():
    return (
        "Cc: My Business <me@mybusiness.com>; "
        "'Some Agent' <s.agent@observe.com>; "
        "Co Worker <c.worker@observe.com>; "
        "This Sender <t.sender@observe.com>;"
    )
