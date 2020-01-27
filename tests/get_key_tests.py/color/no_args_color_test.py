#!/usr/bin/env python3
from object_colors import Color


class TestNoArgsColor:
    def test_exact_letter_in_colored_string_color(
        self, all_colors: Color, small_color_test_string: str
    ) -> None:
        colored_keys = all_colors.red.get_key(small_color_test_string, "c")
        assert colored_keys == small_color_test_string

    def test_exact_word_in_string_color(
        self, all_colors: Color, small_color_test_string: str
    ) -> None:
        colored_keys = all_colors.red.get_key(small_color_test_string, "Cc:")
        assert colored_keys == (
            "\u001b[0;32;40m\u001b[0;31;40mCc:\u001b[0;32;40m My Business "
            "<me@mybusiness.com>;\u001b[0;0m"
        )

    def test_exact_second_word_in_string_color(
        self, all_colors: Color, small_color_test_string: str
    ) -> None:
        """verify indices are working (at least for some)"""
        colored_keys = all_colors.red.get_key(small_color_test_string, "My")
        assert colored_keys == (
            "\u001b[0;32;40mCc: \u001b[0;31;40mMy\u001b[0;32;40m Business "
            "<me@mybusiness.com>;\u001b[0;0m"
        )

    def test_dupe_words_no_color(
        self, all_colors: Color, colored_dupes: str
    ) -> None:
        colored_keys = all_colors.red.get_key(colored_dupes, "one")
        assert colored_keys == (
            "\u001b[0;32;40mThis is a string that says "
            "\u001b[0;31;40mone\u001b[0;32;40m several times. "
            "It says \u001b[0;31;40mone\u001b[0;32;40m in this "
            "sentence. And \u001b[0;31;40mone\u001b[0;32;40m in this sentence. "
            "This sentence also has \u001b[0;31;40mone\u001b[0;32;40m in "
            "it. Lastly this sentence will also say "
            "\u001b[0;31;40mone\u001b[0;32;40m\u001b[0;0m"
        )

    def test_word_in_string_color(
        self, all_colors: Color, small_color_test_string: str
    ) -> None:
        colored_keys = all_colors.red.get_key(small_color_test_string, "cc:")
        assert colored_keys == small_color_test_string
