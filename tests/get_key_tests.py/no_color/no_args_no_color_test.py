#!/usr/bin/env python3
from object_colors import Color


class TestNoArgsNoColor:
    def test_exact_letter_in_colored_string_no_color(
        self, all_colors: Color, small_no_color_test_string
    ) -> None:
        colored_keys = all_colors.red.get_key(small_no_color_test_string, "c")
        assert colored_keys == small_no_color_test_string

    def test_exact_word_in_string_no_color(
        self, all_colors: Color, small_no_color_test_string
    ) -> None:
        colored_keys = all_colors.red.get_key(
            small_no_color_test_string, "Cc:"
        )
        assert colored_keys == (
            "\u001b[0;31;40mCc:\u001b[0;0m My Business " "<me@mybusiness.com>;"
        )

    def test_dupe_words_no_color(self, all_colors: Color, dupes: str) -> None:
        colored_keys = all_colors.red.get_key(dupes, "one")
        assert colored_keys == (
            "This is a string that says \u001b[0;31;40mone\u001b[0;0m several "
            "times. "
            "It says \u001b[0;31;40mone\u001b[0;0m in this "
            "sentence. And \u001b[0;31;40mone\u001b[0;0m in this sentence. "
            "This sentence also has \u001b[0;31;40mone\u001b[0;0m in "
            "it. Lastly this sentence will also say \u001b[0;31;40mone"
            "\u001b[0;0m"
        )

    def test_word_in_string_no_color(
        self, all_colors: Color, small_no_color_test_string
    ) -> None:
        colored_keys = all_colors.red.get_key(
            small_no_color_test_string, "cc:"
        )
        assert colored_keys == small_no_color_test_string
