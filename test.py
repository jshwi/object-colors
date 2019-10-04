#!/usr/bin/env python3

from object_colors import Color


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


def test__dir__():
    c = Color(color='green')
    attrs = c.__dir__()
    assert attrs == Color.keys


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
    assert isinstance(red, Color)


def test_pop_var():
    c = Color(color='red')
    assert c.__dict__['color'] == 1
    red = c.pop('color')
    assert 'color' in c.__dict__
    assert red is None
    c.set(cyan=({'color': 'cyan'}))
    assert isinstance(c.cyan, Color)
    cyan = c.pop('cyan')
    assert isinstance(cyan, Color)


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


def test_class_ints():
    c = Color()
    kwargs = {'kwarg': 114}
    c.class_ints(kwargs)
    assert kwargs == {'kwarg': {'color': 1, 'effect': 1, 'background': 4}}


def test_class_ints_ignore():
    c = Color()
    kwargs = {'kwarg': {'color': 1, 'effect': 1, 'background': 4}}
    c.class_ints(kwargs)
    assert kwargs == {'kwarg': {'color': 1, 'effect': 1, 'background': 4}}


def test_process_args():
    args = Color().process_args((114,))
    assert isinstance(args, list)
    assert args == [1, 1, 4]


def test_process_kwargs_int_kwarg():
    c = Color().process_kwargs((), {'color': 1})
    assert c['color'] == 1


def test_process_kwargs_str_kwarg():
    c = Color().process_kwargs((), {'color': 'red'})
    assert c['color'] == 1


def test_process_kwargs_int_arg():
    c = Color().process_kwargs((1, 1, 4), {})
    assert c['color'] == 1
    assert c['effect'] == 1
    assert c['background'] == 4


def test_process_kwargs_mistake_kwargs():
    c = Color().process_kwargs((), {
        'color': 'rainbow',
        'effect': '3d',
        'background': 'forrest'
    })
    assert c['color'] == 9
    assert c['effect'] == 0
    assert c['background'] == 9


def test_high_numbers():
    c = Color(color=100, effect=100, background=100)
    assert c.color == 9
    assert c.effect == 0
    assert c.background == 9


def test_no_pop_defaults():
    c = Color()
    c.pop('color')
    c.pop('effect')
    c.pop('background')
    assert c.__dict__
    assert 'color' in c.__dict__
    assert 'effect' in c.__dict__
    assert 'background' in c.__dict__
