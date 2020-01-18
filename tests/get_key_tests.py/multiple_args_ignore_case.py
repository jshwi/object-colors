#!/usr/bin/env python3
from object_colors import Color


class TestMultipleArgs:
    def test_exact_word_in_string_ignore_case(
            self, all_colors: Color, small_test_string: str, marked_word: str
    ) -> None:
        """Test uncolored string entered in Color.get_key() to make sure
        an individual word which matches a word in the string exactly
        comes out colored if no scatter or ignore argument is given with
        "Cc:" key entered
        Ensure no other items are colored
        """
        colored_keys = all_colors.red.get_key(
            small_test_string, ["C", "c", ":"], ignore_case=True
        )
        assert colored_keys == marked_word

    def test_word_in_string_ignore_case(
            self, all_colors: Color, small_test_string: str, marked_word: str
    ) -> None:
        """Test uncolored string entered in Color.get_key() to make sure
        an individual word which does not match a word in the string
        exactly comes out the same way it came in if no scatter or
        ignore argument is given with "cc:" key entered
        """
        colored_keys = all_colors.red.get_key(
            small_test_string, ["c", "c", ":"], ignore_case=True
        )
        assert colored_keys == marked_word
