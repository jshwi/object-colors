#!/usr/bin/env python3

from object_colors import Color


class Test:
    def test_color_string(self, str_, green, color_str, reset):
        assert color_str == f"{green}{str_}{reset}"

    def test__getattr__(self, attrs):
        color = Color()
        for attr in attrs:
            assert hasattr(color, attr)

    def test__dir__(self, color, instances, capsys):
        color_instances = color.__dir__()
        assert color_instances == instances

    def test_str_args(self):
        color = Color("red", "bold", "green")
        assert color.text == 1
        assert color.effect == 1
        assert color.background == 2

    def test_str_ints(self):
        color = Color(1, 1, 2)
        assert color.text == 1
        assert color.effect == 1
        assert color.background == 2

    def test_int_dict(self):
        color = Color(orange=1)
        assert color.text == 7
