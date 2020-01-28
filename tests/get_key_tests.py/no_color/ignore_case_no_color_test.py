#!/usr/bin/env python3
from object_colors import Color


class TestIgnoreCaseNoColor:
    def test_exact_word_in_string_ignore_case(
        self, colors, str_, marked
    ) -> None:
        colored_keys = colors.red.get_key(str_, "Cc:", case=True)
        assert colored_keys == marked

    def test_word_in_string_ignore_case(self, colors, str_, marked) -> None:
        colored_keys = colors.red.get_key(str_, "cc:", case=True)
        assert colored_keys == marked
