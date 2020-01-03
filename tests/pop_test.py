#!/usr/bin/env python3
from object_colors import Color
from pytest import fixture


@fixture
def obj():
    c = Color(text="blue")
    c.set(
        red={"text": "red"},
        rand=114,
        rand_2=(1, 43),
        rand_3=(13, 4),
        yellow={"text": 3},
    )
    c.set(c={"text": "blue"})
    c.c.set(
        red={"text": "red"},
        rand=114,
        rand_2=(1, 43),
        rand_3=(13, 4),
        yellow={"test": "yellow"},
    )
    c.c.set(c={"color": {"red": {"text": "red"}}})
    return c


@fixture
def sub_obj(obj):
    c = obj
    return c.pop("c")


class TestPopSubclass:
    def test_pop_subclass(self, obj):
        red = obj.pop("red")
        assert red.text == 1

    def test_pop_tuple_subclass(self, obj):
        rand = obj.pop("rand")
        assert rand.text == 1 and rand.effect == 1 and rand.background == 4

    def test_pop_split_tuple_subclass_1(self, obj):
        rand_2 = obj.pop("rand_2")
        assert (
            rand_2.text == 1 and rand_2.effect == 4 and rand_2.background == 3
        )

    def test_pop_split_tuple_subclass_2(self, obj):
        rand_3 = obj.pop("rand_3")
        assert (
            rand_3.text == 1 and rand_3.effect == 3 and rand_3.background == 4
        )

    def test_pop_set_subclass(self, obj):
        yellow = obj.pop("yellow")
        assert yellow.text == 3


class TestPopClass:
    def test_pop_class(self, obj):
        c = obj.pop("c")
        assert isinstance(c, Color)

    def test_pop_class_subclass(self, sub_obj, obj):
        sub_obj.red = obj.pop("red")
        assert sub_obj.red.text == 1

    def test_pop_tuple_class_subclass(self, sub_obj, obj):
        sub_obj.rand = obj.pop("rand")
        assert (
            sub_obj.rand.text == 1
            and sub_obj.rand.effect == 1
            and sub_obj.rand.background == 4
        )

    def test_pop_split_tuple_class_subclass_1(self, sub_obj, obj):
        sub_obj.rand_2 = obj.pop("rand_2")
        assert (
            sub_obj.rand_2.text == 1
            and sub_obj.rand_2.effect == 4
            and sub_obj.rand_2.background == 3
        )

    def test_pop_split_tuple_class_subclass_2(self, sub_obj, obj):
        sub_obj.rand_3 = obj.pop("rand_3")
        assert (
            sub_obj.rand_3.text == 1
            and sub_obj.rand_3.effect == 3
            and sub_obj.rand_3.background == 4
        )

    def test_pop_set_subclass_subclass(self, sub_obj, obj):
        sub_obj.yellow = obj.pop("yellow")
        assert sub_obj.yellow.text == 3

    def test_pop_var(self):
        c = Color(text="red")
        assert c.__dict__["text"] == 1
        red = c.pop("text")
        assert "text" in c.__dict__ and red is None

    def test_pop_instance(self):
        c = Color()
        c.set(cyan=({"text": "cyan"}))
        assert isinstance(c.cyan, Color)
        cyan = c.pop("cyan")
        assert isinstance(cyan, Color)
