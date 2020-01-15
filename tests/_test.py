#!/usr/bin/env python3
from object_colors import Color


def test_color_string(
    small_test_string: str, small_colored_string: str
) -> None:
    """Tests if strings are correctly colored"""
    assert small_colored_string == (
        f"\u001b[0;32;40m{small_test_string}\u001b[0;0m"
    )


class TestNoArgsColor:
    def test_exact_letter_in_colored_string(
        self, all_colors: Color, small_colored_string: str
    ) -> None:
        """Test uncolored string entered in Color.get_key() to make sure
        it comes out the same way it went in if no scatter or ignore
        argument is given with "c" key entered
        """
        colored_keys = all_colors.get_key(small_colored_string, "c")
        assert colored_keys == small_colored_string

    def test_exact_word_in_string(
        self, all_colors: Color, small_colored_string: str
    ) -> None:
        """Test uncolored string entered in Color.get_key() to make sure
        an individual word which matches a word in the string exactly
        comes out colored if no scatter or ignore argument is given with
        "Cc:" key entered
        Ensure no other items are colored
        """
        colored_keys = all_colors.get_key(small_colored_string, "Cc:")
        assert colored_keys == (
            "\u001b[0;32;40m\u001b[0;31;40mCc:\u001b[0;32;40m My Business "
            "<me@mybusiness.com>;\u001b[0;0m"
        )

    def test_word_in_string(
        self, all_colors: Color, small_colored_string: str
    ) -> None:
        """Test uncolored string entered in Color.get_key() to make sure
        an individual word which does not match a word in the string
        exactly comes out the same way it came in if no scatter or
        ignore argument is given with "cc:" key entered
        """
        colored_keys = all_colors.get_key(small_colored_string, "cc:")
        assert colored_keys == small_colored_string


class TestNoArgsNoColor:
    def test_exact_letter_in_string(
        self, all_colors: Color, small_test_string: str
    ) -> None:
        """Test uncolored string entered in Color.get_key() to make sure
        it comes out the same way it went in if no scatter or ignore
        argument is given with "c" key entered
        """
        colored_keys = all_colors.get_key(small_test_string, "c")
        assert colored_keys == small_test_string

    def test_exact_word_in_string(
        self, all_colors: Color, small_test_string: str
    ) -> None:
        """Test uncolored string entered in Color.get_key() to make sure
        an individual word which matches a word in the string exactly
        comes out colored if no scatter or ignore argument is given with
        "Cc:" key entered
        Ensure no other items are colored
        """
        colored_keys = all_colors.get_key(small_test_string, "Cc:")
        assert colored_keys == (
            "\u001b[0;31;40mCc:\u001b[0;0m My Business <me@mybusiness.com>;"
        )

    def test_word_in_string(
        self, all_colors: Color, small_test_string: str
    ) -> None:
        """Test uncolored string entered in Color.get_key() to make sure
        an individual word which does not match a word in the string
        exactly comes out the same way it came in if no scatter or
        ignore argument is given with "cc:" key entered
        """
        colored_keys = all_colors.get_key(small_test_string, "cc:")
        assert colored_keys == small_test_string


class TestIgnoreCase:
    def test_exact_word_in_string_ignore_case(
        self, all_colors: Color, small_test_string: str
    ) -> None:
        """Test uncolored string entered in Color.get_key() to make sure
        an individual word which matches a word in the string exactly
        comes out colored if no scatter or ignore argument is given with
        "Cc:" key entered
        Ensure no other items are colored
        """
        colored_keys = all_colors.get_key(
            small_test_string, "Cc:", ignore_case=True
        )
        assert colored_keys == (
            "\u001b[0;31;40mCc:\u001b[0;0m My Business <me@mybusiness.com>;"
        )

    def test_word_in_string_ignore_case(
        self, all_colors: Color, small_test_string: str
    ) -> None:
        """Test uncolored string entered in Color.get_key() to make sure
        an individual word which does not match a word in the string
        exactly comes out the same way it came in if no scatter or
        ignore argument is given with "cc:" key entered
        """
        colored_keys = all_colors.get_key(
            small_test_string, "cc:", ignore_case=True
        )
        assert colored_keys == (
            "\u001b[0;31;40mCc:\u001b[0;0m My Business <me@mybusiness.com>;"
        )
