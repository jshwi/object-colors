#!/usr/bin/env python
from object_colors import Color


class TestScatter:
    def test_exact_letter_in_string(
            self, all_colors: Color, small_test_string: str
    ) -> None:
        """Test uncolored string entered in Color.get_key() to make sure
        it comes out the same way it went in if no scatter or ignore
        argument is given with "c" key entered
        """
        colored_keys = all_colors.red.get_key(small_test_string, "c", scatter=True)
        assert colored_keys == (
            "C\u001b[0;31;40mc\u001b[0;0m: My Business "
            "<me@mybusiness.\u001b[0;31;40mc\u001b[0;0mom>;"
        )

    def test_exact_word_in_string(
            self, all_colors: Color, small_test_string: str, marked_word: str
    ) -> None:
        """Test uncolored string entered in Color.get_key() to make sure
        an individual word which matches a word in the string exactly
        comes out colored if no scatter or ignore argument is given with
        "Cc:" key entered
        Ensure no other items are colored
        """
        colored_keys = all_colors.red.get_key(
            small_test_string, "Cc:", scatter=True
        )
        assert colored_keys == (
            "\u001b[0;31;40mC\u001b[0;0m\u001b[0;31;40mc\u001b[0;0m"
            "\u001b[0;31;40m:\u001b[0;0m My Business <me@mybusiness."
            "\u001b[0;31;40mc\u001b[0;0mom>;"
        )

    def test_word_in_string(
            self, all_colors: Color, small_test_string: str
    ) -> None:
        """Test uncolored string entered in Color.get_key() to make sure
        an individual word which does not match a word in the string
        exactly comes out the same way it came in if no scatter or
        ignore argument is given with "cc:" key entered
        """
        colored_keys = all_colors.red.get_key(
            small_test_string, "cc:", scatter=True
        )
        assert colored_keys == (
            "C\u001b[0;31;40mc\u001b[0;0m"
            "\u001b[0;31;40m:\u001b[0;0m My Business <me@mybusiness."
            "\u001b[0;31;40mc\u001b[0;0mom>;"
        )
