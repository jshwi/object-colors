#!/usr/bin/env python3
from pytest import fixture

from object_colors.color_class import Color


@fixture
def keys_():
    return ["color", "effect", "background"]


def test_color_self():
    c = Color()
    assert c.color == 9
    assert c.effect == 0
    assert c.background == 9


def test_set_int_class_vars():
    c = Color(color=1, effect=1, background=4)
    assert c.color == 1
    assert c.effect == 1
    assert c.background == 4


def test_set_str_class_vars():
    c = Color(color='red', effect='bold', background='blue')
    assert c.color == 1
    assert c.effect == 1
    assert c.background == 4


def test__dir__(keys_):
    c = Color(color='green')
    attrs = c.__dir__()
    assert attrs == keys_


def test_var_in_dir():
    c = Color(red={'color': 'red'})
    attrs = c.__dir__()
    assert 'red' in attrs


def test_process_args_int():
    c = Color(114)
    assert c.color == 1
    assert c.effect == 1
    assert c.background == 4


def test_process_args_multi_int():
    c = Color(11, 4)
    assert c.color == 1
    assert c.effect == 1
    assert c.background == 4


def test_str_args():
    c = Color('red', 'bold', 'yellow')
    assert c.color == 1
    assert c.effect == 1
    assert c.background == 3


def test_skip_wrong_input():
    c = Color(txt='red', eff='bold', back='black')
    assert c.color == 9
    assert c.effect == 0
    assert c.background == 9


def test_class_in_class():
    c = Color(red={'color': 'red'})
    assert c.red
    assert isinstance(c.red, Color)


def test_getattr():
    c = Color(red={'color': 'red'})
    assert c.__getattr__('red')


def test_pop_class():
    c = Color(red={'color': 'red'})
    assert 'red' in c.__dict__
    red = c.pop('red')
    assert 'red' not in c.__dict__
    assert red == {'red': {'background': 9, 'color': 1, 'effect': 0}}


def test_pop_var():
    c = Color(color='red')
    assert c.__dict__['color'] == 1
    red = c.pop('color')
    assert 'color' not in c.__dict__
    assert red == 1
    none = c.pop('cyan')
    assert not none


def test_get():
    c = Color(color='red', effect='bold', background='blue')
    got = c.get('this string is for testing')
    assert got == '\033[1;31;44mthis string is for testing\033[0;0m'


def test_print():
    c = Color(red={'color': 'red'})
    c.red.print("Hi")


def test_methods():
    """c = Color()
    [+] c.class_ints()
    [+] c.process_args()
    [ ] c.process_kwargs()
    [+] c.process_args_kwargs()
    [+] c.pop()
    [+] c.set()
    [+] c.print()
    [+] c.get()
    """
    pass


def test_class_ints(keys_):
    c = Color()
    kwargs = {'kwarg': 114}
    c.class_ints(keys_, kwargs)
    assert kwargs == {'kwarg': {'color': 1, 'effect': 1, 'background': 4}}


def test_class_ints_ignore(keys_):
    c = Color()
    kwargs = {'kwarg': {'color': 1, 'effect': 1, 'background': 4}}
    c.class_ints(keys_, kwargs)
    assert kwargs == {'kwarg': {'color': 1, 'effect': 1, 'background': 4}}


def test_process_args():
    args = Color().process_args((114,))
    assert isinstance(args, list)
    assert args == [1, 1, 4]


def test_process_kwargs_int_kwarg(keys_):
    c = Color().process_kwargs(keys_, (), {'color': 1})
    assert c['color'] == 1


def test_process_kwargs_str_kwarg(keys_):
    c = Color().process_kwargs(keys_, (), {'color': 'red'})
    assert c['color'] == 1


def test_process_kwargs_int_arg(keys_):
    c = Color().process_kwargs(keys_, (1, 1, 4), {})
    assert c['color'] == 1
    assert c['effect'] == 1
    assert c['background'] == 4


def test_process_kwargs_mistake_kwargs(keys_):
    c = Color().process_kwargs(keys_, (), {
        'color': 'rainbow',
        'effect': '3d',
        'background': 'forrest'
    })
    assert c['color'] == 9
    assert c['effect'] == 0
    assert c['background'] == 9
