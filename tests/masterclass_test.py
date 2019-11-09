from object_colors import Color


class TestMasterClass(object):
    def test_text_self(self):
        c = Color()
        assert c.text == 7 and c.effect == 0 and c.background == 0

    def test_set_int_class_vars(self):
        c = Color(text=1, effect=1, background=4)
        assert c.text == 1 and c.effect == 1 and c.background == 4

    def test_set_str_class_vars(self):
        c = Color(text="red", effect="bold", background="blue")
        assert c.text == 1 and c.effect == 1 and c.background == 4

    def test__dir__(self):
        c = Color(text="green")
        attrs = c.__dir__()
        Color.keys.append("bold")
        assert attrs == Color.keys

    def test_process_args_int(self):
        c = Color(114)
        assert c.text == 1 and c.effect == 1 and c.background == 4

    def test_process_args_multi_int(self):
        c = Color(11, 4)
        assert c.text == 1 and c.effect == 1 and c.background == 4

    def test_str_args(self):
        c = Color("red", "bold", "yellow")
        assert c.text == 1 and c.effect == 1 and c.background == 3

    def test_skip_wrong_input(self):
        c = Color(txt="red", eff="bold", back="black")
        assert c.text == 7 and c.effect == 0 and c.background == 0

    def test_get(self):
        c = Color(text="red", effect="bold", background="blue")
        got = c.get("this string is for testing")
        assert got == "\u001b[1;31;44mthis string is for testing\u001b[0;0m"

    def test_high_numbers(self):
        c = Color(text=100, effect=100, background=100)
        assert c.text == 7 and c.effect == 0 and c.background == 0

    def test_no_pop_defaults(self):
        c = Color()
        c.pop("text")
        c.pop("effect")
        c.pop("background")
        assert (
            c.__dict__
            and "text" in c.__dict__
            and "effect" in c.__dict__
            and "background" in c.__dict__
        )

    def test_none(self):
        c = Color(test="white", effect="none", background="none")
        assert c.text == 7 and c.effect == 0 and c.background == 0

    def test_none_in_tuple_effect(self):
        c = Color(text="red", effect=None, background="blue")
        assert c.text == 1 and c.effect == 0 and c.background == 4

    def test_none_in_tuple_text(self):
        c = Color(text=None, effect="bold", background="blue")
        assert c.text == 7 and c.effect == 1 and c.background == 4

    def test_unpacking_tuples(self):
        cc = Color(text="red")
        a, b, c = cc.get("a", "b", "c")
        assert (
            a == "\u001b[0;31;40ma\u001b[0;0m"
            and b == "\u001b[0;31;40mb\u001b[0;0m"
            and c == "\u001b[0;31;40mc\u001b[0;0m"
        )

    def test_tup_return(self):
        c = Color(text="red")
        tup = c.get("a", "b", "c")
        assert isinstance(tup, tuple)

    def test_unpack_return(self):
        cc = Color(text="red")
        tup = cc.get("a", "b", "c")
        a, b, c = tup
        assert (
            isinstance(a, str)
            and isinstance(b, str)
            and isinstance(c, str)
            and a == "\u001b[0;31;40ma\u001b[0;0m"
            and b == "\u001b[0;31;40mb\u001b[0;0m"
            and c == "\u001b[0;31;40mc\u001b[0;0m"
        )

    def test_populate_colors(self):
        c = Color("colors")
        assert (
            isinstance(c.black, Color)
            and isinstance(c.red, Color)
            and isinstance(c.green, Color)
            and isinstance(c.yellow, Color)
            and isinstance(c.blue, Color)
            and isinstance(c.purple, Color)
            and isinstance(c.cyan, Color)
            and isinstance(c.white, Color)
        )
