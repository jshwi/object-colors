#!/usr/bin/env python3
from pytest import fixture

from object_colors import Color


class TestPrintNoArgs:
    def test_exact_letter_in_colored_string(
            self, color:
            Color,
            color_str: str,
            str_: str,
            capsys: fixture,
            red: str,
            reset: str
    ) -> None:
        color.red.print_key(str_, "c")
        captured = capsys.readouterr()
        assert captured.out == str_ + "\n"
        color.red.print_key(color_str, "c")
        captured = capsys.readouterr()
        assert captured.out == color_str + "\n"

    def test_exact_word_in_string(
            self,
            color_str: str,
            marked_color: str,
            str_: str,
            color_keys: str,
            marked: str,
            capsys: fixture
    ) -> None:
        color = Color()
        color.populate_colors()
        color.red.print_key(str_, "Cc:")
        captured = capsys.readouterr()
        assert captured.out == marked + "\n"
        color.red.print_key(color_str, "Cc:")
        captured = capsys.readouterr()
        assert captured.out == marked_color + "\n"

    def test_exact_second_word_in_string(
            self,
            color: Color,
            color_str: str,
            marked_second_color: str,
            str_: str,
            marked_second: str,
            capsys: fixture
    ) -> None:
        """verify indices are working (at least for some)"""
        color.red.print_key(str_, "My")
        captured = capsys.readouterr()
        assert captured.out == marked_second + "\n"
        color.red.print_key(color_str, "My")
        captured = capsys.readouterr()
        assert captured.out == marked_second_color + "\n"

    def test_dupe_words(
            self,
            color: Color,
            colored_dupes: str,
            dupe_marked_color: str,
            dupes: str,
            dupe_marked: str,
            capsys: fixture
    ) -> None:
        color.red.print_key(dupes, "one")
        captured = capsys.readouterr()
        assert captured.out == dupe_marked + "\n"
        color.red.print_key(colored_dupes, "one")
        captured = capsys.readouterr()
        assert captured.out == dupe_marked_color + "\n"

    def test_word_in_string(
            self, color: Color, color_str: str, str_: str, capsys: fixture
    ) -> None:
        color.print_key(str_, "cc:")
        captured = capsys.readouterr()
        assert captured.out == str_ + "\n"
        color.print_key(color_str, "cc:")
        captured = capsys.readouterr()
        assert captured.out == color_str + "\n"

    def test_words_in_string(
            self,
            color: Color,
            color_str: str,
            spaced_words_color: str,
            str_: str,
            spaced_words: str,
            capsys: fixture
    ) -> None:
        color.red.print_key(str_, "Cc:", "Business")
        captured = capsys.readouterr()
        assert captured.out == spaced_words + "\n"
        color.red.print_key(color_str, "Cc:", "Business")
        captured = capsys.readouterr()
        assert captured.out == spaced_words_color + "\n"


class TestPrintIgnoreCaseAndScatter:
    def test_exact_letter_in_string(
            self,
            color: Color,
            color_str: str,
            exact_idx_color: str,
            all_cs_color: str,
            capsys: fixture
    ) -> None:
        color.red.print_key(
            color_str, "c", ignore_case=True, scatter=True
        )
        captured = capsys.readouterr()
        assert captured.out == exact_idx_color + "\n"

    def test_exact_word_in_string(
            self,
            color: Color,
            color_str: str,
            marked: str,
            all_cs_color: str,
            capsys: fixture
    ) -> None:
        color.red.print_key(
            color_str, "Cc:", ignore_case=True, scatter=True
        )
        captured = capsys.readouterr()
        assert captured.out == all_cs_color + "\n"

    def test_word_in_string(
            self,
            color: Color,
            color_str: str,
            all_cs_color: str,
            capsys: filter
    ) -> None:
        color.red.print_key(
            color_str, "cc:", ignore_case=True, scatter=True
        )
        captured = capsys.readouterr()
        assert captured.out == all_cs_color + "\n"


class TestPrintIgnoreCase:
    def test_exact_word_in_string_ignore_case(
            self,
            color: Color,
            color_str: str,
            marked_color: str,
            marked: str,
            str_: str,
            capsys: fixture
    ) -> None:
        color.red.print_key(str_, "Cc:", ignore_case=True)
        captured = capsys.readouterr()
        assert captured.out == marked + "\n"
        color.red.print_key(color_str, "Cc:", ignore_case=True)
        captured = capsys.readouterr()
        assert captured.out == marked_color + "\n"

    def test_word_in_string_ignore_case(
            self,
            color: Color,
            color_str: str,
            marked_color: str,
            str_: str,
            marked: str,
            capsys: fixture
    ) -> None:
        color.red.print_key(str_, "cc:", ignore_case=True)
        captured = capsys.readouterr()
        assert captured.out == marked + "\n"
        color.red.print_key(color_str, "cc:", ignore_case=True)
        captured = capsys.readouterr()
        assert captured.out == marked_color + "\n"


class TestPrintScatter:
    def test_exact_letter_in_string(
            self,
            color: Color,
            color_str: str,
            str_: str,
            scatter_cs_exact_color: str,
            scatter_cs_exact: str,
            capsys: fixture
    ) -> None:
        color.red.print_key(str_, "c", scatter=True)
        captured = capsys.readouterr()
        assert captured.out == scatter_cs_exact + "\n"
        color.red.print_key(color_str, "c", scatter=True)
        captured = capsys.readouterr()
        assert captured.out == scatter_cs_exact_color + "\n"

    def test_exact_word_in_string(
            self,
            color_str: str,
            marked: str,
            scatter_cs_blue_color: str,
            str_: str,
            scatter_cs_blue: str,
            capsys: fixture
    ) -> None:
        cs = "Cc:"
        blue = Color()
        blue.populate_colors()
        blue.blue.print_key(str_, cs, scatter=True)
        captured = capsys.readouterr()
        assert captured.out == scatter_cs_blue + "\n"
        blue.blue.print_key(color_str, cs, scatter=True)
        captured = capsys.readouterr()
        assert captured.out == scatter_cs_blue_color + "\n"

    def test_word_in_string(
            self,
            color: Color,
            color_str: str,
            all_cs_no_caps_blue_color,
            all_cs_no_caps_blue,
            str_: str,
            capsys: fixture
    ) -> None:
        cc = "cc:"
        scatter = True
        color.blue.print_key(str_, cc, scatter=scatter)
        captured = capsys.readouterr()
        assert captured.out == all_cs_no_caps_blue + "\n"
        color.blue.print_key(color_str, cc, scatter=scatter)
        captured = capsys.readouterr()
        assert captured.out == all_cs_no_caps_blue_color + "\n"
