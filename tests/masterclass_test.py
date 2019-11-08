from object_colors import Color


class TestMasterClass(object):
    def test_text_self(self):
        c = Color()
        assert c.text == 7
        assert c.effect == 0
        assert c.background == 0

    def test_set_int_class_vars(self):
        c = Color(text=1, effect=1, background=4)
        assert c.text == 1
        assert c.effect == 1
        assert c.background == 4

    def test_set_str_class_vars(self):
        c = Color(text="red", effect="bold", background="blue")
        assert c.text == 1
        assert c.effect == 1
        assert c.background == 4

    def test__dir__(self):
        c = Color(text="green")
        attrs = c.__dir__()
        assert attrs == Color.keys

    def test_process_args_int(self):
        c = Color(114)
        assert c.text == 1
        assert c.effect == 1
        assert c.background == 4

    def test_process_args_multi_int(self):
        c = Color(11, 4)
        assert c.text == 1
        assert c.effect == 1
        assert c.background == 4

    def test_str_args(self):
        c = Color("red", "bold", "yellow")
        assert c.text == 1
        assert c.effect == 1
        assert c.background == 3

    def test_skip_wrong_input(self):
        c = Color(txt="red", eff="bold", back="black")
        assert c.text == 7
        assert c.effect == 0
        assert c.background == 0

    def test_pop_var(self):
        c = Color(text="red")
        assert c.__dict__["text"] == 1
        red = c.pop("text")
        assert "text" in c.__dict__
        assert red is None
        c.set(cyan=({"text": "cyan"}))
        assert isinstance(c.cyan, Color)
        cyan = c.pop("cyan")
        assert isinstance(cyan, Color)

    def test_get(self):
        c = Color(text="red", effect="bold", background="blue")
        got = c.get("this string is for testing")
        assert got == "\u001b[1;31;44mthis string is for testing\u001b[0;0m"

    def test_class_ints(self):
        c = Color()
        kwargs = {"kwarg": 114}
        kwargs = c.class_ints(kwargs)
        assert kwargs == {"kwarg": {"text": 1, "effect": 1, "background": 4}}

    def test_class_ints_ignore(self):
        c = Color()
        kwargs = {"kwarg": {"text": 1, "effect": 1, "background": 4}}
        kwargs = c.class_ints(kwargs)
        assert kwargs == {"kwarg": {"text": 1, "effect": 1, "background": 4}}

    def test_process_args(self):
        args = Color().process_args((114,))
        assert isinstance(args, list)
        assert args == [1, 1, 4]

    def test_process_kwargs_int_kwarg(self):
        c = Color().get_processed((), {"text": 1})
        assert c["text"] == 1

    def test_process_kwargs_str_kwarg(self):
        c = Color().get_processed((), {"text": "red"})
        assert c["text"] == 1

    def test_process_kwargs_int_arg(self):
        c = Color().get_processed((1, 1, 4), {})
        assert c["text"] == 1
        assert c["effect"] == 1
        assert c["background"] == 4

    def test_process_kwargs_mistake_kwargs(self):
        c = Color().get_processed(
            (), {"text": "rainbow", "effect": "3d", "background": "forrest"}
        )
        assert c["text"] == 7
        assert c["effect"] == 0
        assert c["background"] == 0

    def test_high_numbers(self):
        c = Color(text=100, effect=100, background=100)
        assert c.text == 7
        assert c.effect == 0
        assert c.background == 0

    def test_no_pop_defaults(self):
        c = Color()
        c.pop("text")
        c.pop("effect")
        c.pop("background")
        assert c.__dict__
        assert "text" in c.__dict__
        assert "effect" in c.__dict__
        assert "background" in c.__dict__

    def test_none(self):
        c = Color(test="white", effect="none", background="none")
        assert c.text == 7
        assert c.effect == 0
        assert c.background == 0

    def test_none_in_tuple_effect(self):
        c = Color(text="red", effect=None, background="blue")
        assert c.text == 1
        assert c.effect == 0
        assert c.background == 4

    def test_none_in_tuple_text(self):
        c = Color(text=None, effect="bold", background="blue")
        assert c.text == 7
        assert c.effect == 1
        assert c.background == 4
