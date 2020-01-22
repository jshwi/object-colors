#!/usr/bin/env python 3
from object_colors import Color


class TestSpacedSearchesNoColor:
    def test_exact_word_in_string(
        self, all_colors: Color, small_no_color_test_string, marked_word: str
    ) -> None:
        """Test uncolored string entered in Color.get_key() to make sure
        an individual word which matches a word in the string exactly
        comes out colored if no scatter or ignore argument is given with
        "Cc:" key entered
        Ensure no other items are colored
        """
        colored_keys = all_colors.red.get_key(
            small_no_color_test_string, ["C", "c", ":"]
        )
        assert colored_keys == marked_word

    def test_word_in_string(
        self, all_colors: Color, small_no_color_test_string
    ) -> None:
        """Test uncolored string entered in Color.get_key() to make sure
        an individual word which does not match a word in the string
        exactly comes out the same way it came in if no scatter or
        ignore argument is given with "cc:" key entered
        """
        colored_keys = all_colors.red.get_key(
            small_no_color_test_string, ["c", "c", ":"]
        )
        assert colored_keys == small_no_color_test_string

    def test_word_in_string_ignore_case(
        self, all_colors: Color, small_no_color_test_string, marked_word
    ) -> None:
        """Test uncolored string entered in Color.get_key() to make sure
        an individual word which does not match a word in the string
        exactly comes out the same way it came in if no scatter or
        ignore argument is given with "cc:" key entered
        """
        colored_keys = all_colors.red.get_key(
            small_no_color_test_string, ["c", "c", ":"], ignore_case=True
        )
        assert colored_keys == marked_word

    def test_words_in_string(
        self, all_colors: Color, small_no_color_test_string, marked_word
    ) -> None:
        """Test uncolored string entered in Color.get_key() to make sure
        an individual word which does not match a word in the string
        exactly comes out the same way it came in if no scatter or
        ignore argument is given with "cc:" key entered
        """
        colored_keys = all_colors.red.get_key(
            small_no_color_test_string, ["Cc:", "Business"]
        )
        assert colored_keys == (
            "\u001b[0;31;40mCc:\u001b"
            "[0;0m My \u001b[0;31;40mBusiness\u001b[0;0m "
            "<me@mybusiness.com>;"
        )
