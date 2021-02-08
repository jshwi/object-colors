"""
tests.conftest
==============
"""
from pytest import fixture

from object_colors import Color


@fixture
def color():
    populated = Color()
    populated.populate_colors()
    return populated


@fixture
def color_str(color, str_):
    return color.green.get(str_)


@fixture
def str_():
    return "Cc: My Business <me@mybusiness.com>;"


@fixture
def marked(red, reset):
    return f"{red}Cc:{reset} My Business <me@mybusiness.com>;"


@fixture
def marked_color(green, red, reset):
    return f"{green}{red}Cc:{green} My Business <me@mybusiness.com>;{reset}"


@fixture
def marked_second(red, reset):
    return f"Cc: {red}My{reset} Business <me@mybusiness.com>;"


@fixture
def marked_second_color(green, red, reset):
    return f"{green}Cc: {red}My{green} Business <me@mybusiness.com>;{reset}"


@fixture
def dupe_marked_color(green, red, reset):
    """do dupe fixture but with ignore"""
    return (
        f"{green}This is a string that says {red}one{green} several times. "
        f"It says {red}one{green} in this sentence. And {red}one{green} in "
        f"this sentence. This sentence also has {red}one{green} in it. Lastly "
        f"this sentence will also say {red}one{green}{reset}"
    )


@fixture
def dupe_marked(green, red, reset):
    """do dupe fixture but with ignore"""
    return (
        f"This is a string that says {red}one{reset} several times. It says "
        f"{red}one{reset} in this sentence. And {red}one{reset} in this "
        f"sentence. This sentence also has {red}one{reset} in it. Lastly this "
        f"sentence will also say {red}one{reset}"
    )


@fixture
def exact_idx_color(green, red, reset):
    return (
        f"{green}{red}C{green}{red}c{green}: My Business "
        f"<me@mybusiness.{red}c{green}om>;{reset}"
    )


@fixture
def dupes():
    return (
        "This is a string that says one several times. It says one in this "
        "sentence. And one in this sentence. This sentence also has one in "
        "it. Lastly this sentence will also say one"
    )


@fixture
def colored_dupes():
    return (
        "\u001b[0;32;40mThis is a string that says one several times. It says "
        "one in this sentence. And one in this sentence. This sentence also "
        "has one in it. Lastly this sentence will also say one\u001b[0;0m"
    )


@fixture
def spaced_words(green, red, reset):
    return f"{red}Cc:{reset} My {red}Business{reset} <me@mybusiness.com>;"


@fixture
def spaced_words_color(green, red, reset):
    return (
        f"{green}{red}Cc:{green} My {red}Business{green} "
        f"<me@mybusiness.com>;{reset}"
    )


@fixture
def green():
    return "\u001b[0;32;40m"


@fixture
def red():
    return "\u001b[0;31;40m"


@fixture
def reset():
    return "\u001b[0;0m"


@fixture
def attrs():
    return [
        "get",
        "set",
        "get",
        "get_key",
        "print",
        "print_key",
        "pop",
        "multicolor",
        "populate_colors",
    ]


@fixture
def colors():
    return [
        "black",
        "red",
        "green",
        "yellow",
        "blue",
        "purple",
        "cyan",
        "white",
    ]


@fixture
def instances(colors):
    return ["text", "effect", "background", "bold"] + colors


@fixture
def codes():
    return [
        "0;31;40m",
        "0;32;40m",
        "0;33;40m",
        "0;34;40m",
        "0;35;40m",
        "0;36;40m",
        "0;37;40m",
    ]


@fixture
def long_str():
    return (
        "Beautiful is better than ugly."
        "Explicit is better than implicit."
        "Simple is better than complex."
        "Complex is better than complicated."
        "Flat is better than nested."
        "Sparse is better than dense."
        "Readability counts."
        "Special cases aren't special enough to break the rules."
        "Although practicality beats purity."
        "Errors should never pass silently."
        "Unless explicitly silenced."
        "In the face of ambiguity, refuse the temptation to guess."
        "There should be one-- and preferably only one --obvious way to do it."
        "Although that way may not be obvious at first unless you're Dutch."
        "Now is better than never."
        "Although never is often better than *right* now."
        "If the implementation is hard to explain, it's a bad idea."
        "If the implementation is easy to explain, it may be a good idea."
        "Namespaces are one honking great idea -- let's do more of those!"
    )
