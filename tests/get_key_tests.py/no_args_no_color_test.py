#!/usr/bin/env python
from object_colors import Color


class TestNoArgsNoColor:
    def test_exact_letter_in_string(
            self, all_colors: Color, small_test_string: str
    ) -> None:
        """Test uncolored string entered in Color.get_key() to make sure
        it comes out the same way it went in if no scatter or ignore
        argument is given with "c" key entered
        """
        colored_keys = all_colors.red.get_key(small_test_string, "c")
        assert colored_keys == small_test_string

    def test_exact_word_in_string(
            self, all_colors: Color, small_test_string: str, marked_word: str
    ) -> None:
        """Test uncolored string entered in Color.get_key() to make sure
        an individual word which matches a word in the string exactly
        comes out colored if no scatter or ignore argument is given with
        "Cc:" key entered
        Ensure no other items are colored
        """
        colored_keys = all_colors.red.get_key(small_test_string, "Cc:")
        assert colored_keys == marked_word

    def test_word_in_string(
            self, all_colors: Color, small_test_string: str
    ) -> None:
        """Test uncolored string entered in Color.get_key() to make sure
        an individual word which does not match a word in the string
        exactly comes out the same way it came in if no scatter or
        ignore argument is given with "cc:" key entered
        """
        colored_keys = all_colors.red.get_key(small_test_string, "cc:")
        assert colored_keys == small_test_string
