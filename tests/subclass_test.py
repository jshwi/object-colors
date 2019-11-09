from object_colors import Color


class TestSubClass(object):
    def test_var_in_dir(self):
        c = Color(red={"text": "red"})
        attrs = c.__dir__()
        assert "red" in attrs

    def test_class_in_class(self):
        c = Color(red={"text": "red"})
        assert c.red
        assert isinstance(c.red, Color)

    def test_getattr(self):
        c = Color(red={"text": "red"})
        assert c.__getattr__("red")

    def test_pop_class(self):
        c = Color(red={"text": "red"})
        assert "red" in c.__dict__
        red = c.pop("red")
        assert "red" not in c.__dict__
        assert isinstance(red, Color)

    def test_print(self):
        c = Color(red={"text": "red"})
        c.red.print("Hi")

    def test_subclass_self(self):
        c = Color(red={})
        assert c.red.text == 7
        assert c.red.effect == 0
        assert c.red.background == 0

    def test_set_int_subclass_vars(self):
        c = Color(red={"text": 1, "effect": 1, "background": 4})
        assert c.red.text == 1
        assert c.red.effect == 1
        assert c.red.background == 4

    def test_set_str_subclass_vars(self):
        c = Color(red={"text": "red", "effect": "bold", "background": "blue"})
        assert c.red.text == 1
        assert c.red.effect == 1
        assert c.red.background == 4

    def test__dir__(self):
        c = Color(red={"text": "green"})
        attrs = c.red.__dir__()
        assert attrs == Color.keys

    def test_process_args_int_subclass(self):
        c = Color(red=(114,))
        assert c.red.text == 1
        assert c.red.effect == 1
        assert c.red.background == 4

    def test_process_args_multi_int_subclass(self):
        c = Color(red=(11, 4))
        assert c.red.text == 1
        assert c.red.effect == 1
        assert c.red.background == 4

    def test_process_args_multi_int_subclass_1(self):
        c = Color(red=(1, 1, 4))
        assert c.red.text == 1
        assert c.red.effect == 1
        assert c.red.background == 4

    def test_str_args_subclass(self):
        c = Color(red=("red",))
        assert c.red.text == 1
        assert c.red.effect == 0
        assert c.red.background == 0

    def test_str_args_subclass_2(self):
        c = Color(red=("red", "bold"))
        assert c.red.text == 1
        assert c.red.effect == 1
        assert c.red.background == 0

    def test_str_args_subclass_3(self):
        c = Color(red=("red", "bold", "yellow"))
        assert c.red.text == 1
        assert c.red.effect == 1
        assert c.red.background == 3

    def test_skip_wrong_input_subclass(self):
        c = Color(red={"txt": "red", "eff": "bold", "back": "black"})
        assert c.red.text == 7
        assert c.red.effect == 0
        assert c.red.background == 0

    def test_pop_var_subclass(self):
        c = Color(red={"text": "red"})
        assert c.red.__dict__["text"] == 1
        red = c.red.pop("text")
        assert "text" in c.red.__dict__
        assert red is None
        c.red.set(cyan=({"text": "cyan"}))
        assert isinstance(c.red.cyan, Color)
        cyan = c.red.pop("cyan")
        assert isinstance(cyan, Color)

    def test_get_subclass(self):
        c = Color(red={"text": "red", "effect": "bold", "background": "blue"})
        got = c.red.get("this string is for testing")
        assert got == "\u001b[1;31;44mthis string is for testing\u001b[0;0m"

    def test_class_ints_subclass(self):
        c = Color(red={})
        kwargs = {"kwarg": 114}
        kwargs = c.red.class_ints(kwargs)
        assert kwargs == {"kwarg": {"text": 1, "effect": 1, "background": 4}}

    def test_class_ints_ignore_subclass(self):
        c = Color(red={})
        kwargs = {"kwarg": {"text": 1, "effect": 1, "background": 4}}
        kwargs = c.red.class_ints(kwargs)
        assert kwargs == {"kwarg": {"text": 1, "effect": 1, "background": 4}}

    def test_process_args_subclass(self):
        c = Color(red={})
        args = c.red.process_args((114,))
        assert isinstance(args, list)
        assert args == [1, 1, 4]

    def test_process_kwargs_int_kwarg_subclass(self):
        c = Color(red={})
        kwargs = c.red.get_processed((), {"text": 1})
        assert kwargs["text"] == 1

    def test_process_kwargs_str_kwarg_subclass(self):
        c = Color(red={})
        kwargs = c.red.get_processed((), {"text": "red"})
        assert kwargs["text"] == 1

    def test_process_kwargs_int_arg(self):
        c = Color(red={})
        kwargs = c.red.get_processed((1, 1, 4), {})
        assert kwargs["text"] == 1
        assert kwargs["effect"] == 1
        assert kwargs["background"] == 4

    def test_process_kwargs_mistake_kwargs_subclass(self):
        c = Color(red={})
        kwargs = c.red.get_processed(
            (), {"text": "rainbow", "effect": "3d", "background": "forrest"}
        )
        assert kwargs["text"] == 7
        assert kwargs["effect"] == 0
        assert kwargs["background"] == 0

    def test_high_numbers_subclass(self):
        c = Color(red={"text": 100, "effect": 100, "background": 100})
        assert c.red.text == 7
        assert c.red.effect == 0
        assert c.red.background == 0

    def test_no_pop_defaults_subclass(self):
        c = Color(red={})
        c.red.pop("text")
        c.red.pop("effect")
        c.red.pop("background")
        assert c.red.__dict__
        assert "text" in c.red.__dict__
        assert "effect" in c.red.__dict__
        assert "background" in c.red.__dict__

    def test_none_subclass(self):
        c = Color(
            red={"text": "white", "effect": "none", "background": "none"}
        )
        assert c.red.text == 7
        assert c.red.effect == 0
        assert c.red.background == 0

    def test_none_in_tuple_effect_subclass(self):
        c = Color(red={"text": "red", "effect": None, "background": "blue"})
        assert c.red.text == 1
        assert c.red.effect == 0
        assert c.red.background == 4

    def test_none_in_tuple_text_background(self):
        c = Color(red={"text": None, "effect": "bold", "background": "blue"})
        assert c.red.text == 7
        assert c.red.effect == 1
        assert c.red.background == 4

    def test_instantiate_two(self):
        c = Color(red={"text": "red"}, yellow={"text": "yellow"})
        c.red.print("testing")
        c.yellow.print("testing")
