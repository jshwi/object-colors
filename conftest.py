#!/usr/bin/env python3
from pytest import fixture

from object_colors import Color


@fixture
def all_colors():
    return Color(populate=True)


@fixture
def small_colored_string(all_colors, small_test_string):
    return all_colors.green.get(small_test_string)


@fixture
def small_test_string():
    return "Cc: My Business <me@mybusiness.com>;"


@fixture
def marked_word():
    return "\u001b[0;31;40mCc:\u001b[0;0m My Business <me@mybusiness.com>;"


@fixture
def all_cs_marked():
    return (
        "\u001b[0;31;40mC\u001b[0;0m\u001b[0;31;40mc\u001b[0;0m"
        "\u001b[0;31;40m:\u001b[0;0m My Business <me@mybusiness."
        "\u001b[0;31;40mc\u001b[0;0mom>;"
    )
