#!/usr/bin/env python3
from pytest import fixture

from object_colors import Color


@fixture
def obj():
    c = Color("text", "blue")
    c.set(red={"text": "red"})
    c.set(rand=114)
    c.set(rand_2=(1, 43))
    c.set(rand_3=(13, 4))
    c.set(yellow={"text": 3})
    c.set(c={"color": {"text": "blue"}})
    c.c.set({"red": {"text": "red"}})
    c.c.set(rand={"rand": 114})
    c.c.set(rand_2={"rand_2": (1, 43)})
    c.c.set(rand_3={"rand_3": (13, 4)})
    c.c.set(yellow={"test": "yellow"})
    c.c.set(c={"color": {"red": {"text": "red"}}})
    return c


class TestPopSubclass:
    def test_pop_subclass(self, obj):
        red = obj.pop("red")
        assert red.text == 1

    def test_pop_tuple_subclass(self, obj):
        rand = obj.pop("rand")
        assert rand.text == 1
        assert rand.effect == 1
        assert rand.background == 4

    def test_pop_split_tuple_subclass_1(self, obj):
        rand_2 = obj.pop("rand_2")
        assert rand_2.text == 1
        assert rand_2.effect == 4
        assert rand_2.background == 3

    def test_pop_split_tuple_subclass_2(self, obj):
        rand_3 = obj.pop("rand_3")
        assert rand_3.text == 1
        assert rand_3.effect == 3
        assert rand_3.background == 4

    def test_pop_set_subclass(self, obj):
        yellow = obj.pop("yellow")
        assert yellow.text == 3


class TestPopClass:
    def test_pop_class(self, obj):
        c = obj.pop("c")
        assert isinstance(c, Color)
        return c

    def test_pop_class_subclass(self, obj):
        c = self.test_pop_class(obj)
        c.red = obj.pop("red")
        assert c.red.text == 1

    def test_pop_tuple_class_subclass(self, obj):
        c = self.test_pop_class(obj)
        c.rand = obj.pop("rand")
        assert c.rand.text == 1
        assert c.rand.effect == 1
        assert c.rand.background == 4

    def test_pop_split_tuple_class_subclass_1(self, obj):
        c = self.test_pop_class(obj)
        c.rand_2 = obj.pop("rand_2")
        assert c.rand_2.text == 1
        assert c.rand_2.effect == 1
        assert c.rand_2.background == 4

    def test_pop_split_tuple_class_subclass_2(self, obj):
        c = self.test_pop_class(obj)
        c.rand_3 = obj.pop("rand_3")
        assert c.rand_3.text == 1
        assert c.rand_3.effect == 3
        assert c.rand_3.background == 4

    def test_pop_set_subclass_subclass(self, obj):
        c = self.test_pop_class(obj)
        c.yellow = obj.pop("yellow")
        assert c.yellow.text == 3
