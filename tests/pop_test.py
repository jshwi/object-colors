#!/usr/bin/env python3
from object_colors import Color


class TestPop:
    def test_pop_result(self, color):
        assert hasattr(color, "red")
        red = color.pop("red")
        assert "red" not in color.__dict__
        red_string = red.get("This is red")
        assert red_string == f"\u001b[0;31;40mThis is red\u001b[0;0m"

    def test_pop_no_result(self):
        color = Color()
        assert "red" not in color.__dict__
        red = color.pop("red")
        assert red is None
