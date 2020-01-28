#!/usr/bin/env python3
from object_colors import Color


class TestNoArgsNoColor:
    def test_exact_letter_in_colored_string_no_color(
        self, colors, str_
    ) -> None:
        colored_keys = colors.red.get_key(str_, "c")
        assert colored_keys == str_

    def test_exact_word_in_string_no_color(self, colors, str_) -> None:
        colored_keys = colors.red.get_key(str_, "Cc:")
        assert colored_keys == (
            "\u001b[0;31;40mCc:\u001b[0;0m My Business " "<me@mybusiness.com>;"
        )

    def test_dupe_words_no_color(self, colors, dupes: str) -> None:
        colored_keys = colors.red.get_key(dupes, "one")
        assert colored_keys == (
            "This is a string that says \u001b[0;31;40mone\u001b[0;0m several "
            "times. "
            "It says \u001b[0;31;40mone\u001b[0;0m in this "
            "sentence. And \u001b[0;31;40mone\u001b[0;0m in this sentence. "
            "This sentence also has \u001b[0;31;40mone\u001b[0;0m in "
            "it. Lastly this sentence will also say \u001b[0;31;40mone"
            "\u001b[0;0m"
        )

    def test_word_in_string_no_color(self, colors, str_) -> None:
        colored_keys = colors.red.get_key(str_, "cc:")
        assert colored_keys == str_
