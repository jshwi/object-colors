README
======
`Pypi <https://pypi.org/project/object-colors/>`_ |
`Read the Docs <https://object-colors.readthedocs.io/en/latest/>`_ |
`Github Pages <https://jshwi.github.io/object_colors/index.html>`_

.. image:: https://travis-ci.org/jshwi/object_colors.svg?branch=master
    :target: https://travis-ci.org/jshwi/object_colors
    :alt: Build Status
.. image:: https://codecov.io/github/jshwi/object_colors/coverage.svg?branch=master
    :target: https://codecov.io/github/jshwi/object_colors?branch=master
    :alt: codecov.io
.. image:: https://badge.fury.io/py/object-colors.svg
    :target: https://badge.fury.io/py/object-colors
    :alt: PyPi Version
.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: Licence

Installation

.. code-block:: console

    pip install object-colors

Setup

.. code:: python

    from object_colors import Color
    c = Color()
..

Usage

`key-values`
    Match `effects` with `effect` and `colors` with `text` and `background`

.. code:: javascript

    keys = ["text", "effect", "background"]
    values = {
        "colors": ["black", "red", "green", "yellow", "blue", "purple", "cyan", "white"]
        "effects": ['none', "bold", 'bright', "underline", "negative"]
    }
..

For most versatile usage simply instantiate the class with the string argument "colors"

This will populate the instance with a subclass for every key in the "colors" object

.. code:: python

    >>> from object_colors import Color
    >>> c = Color("colors")
    >>> print(c.__dict__)
    {
        'text': 7,
        'effect': 0,
        'background': 0,
        'black': <object_colors.Color object at 0x7f3302cf4b10>,
        'red': <object_colors.Color object at 0x7f3303aa5d10>,
        'green': <object_colors.Color object at 0x7f33037a7710>,
        'yellow': <object_colors.Color object at 0x7f3302bd4710>,
        'blue': <object_colors.Color object at 0x7f3302bd4d50>,
        'purple': <object_colors.Color object at 0x7f3302ce0910>,
        'cyan': <object_colors.Color object at 0x7f33037ddc10>,
        'white': <object_colors.Color object at 0x7f33005e4c10>,
        'bold': <object_colors.Color object at 0x7f3303b09a90>
    }
..

This can be further enhanced with the Color.bold object, initialized when bold has not been activated

.. code:: python

    >>> c.red.print("not bold")
    >>> c.red.bold.print("bold")

..

All colors, effects and objects can be manipulated however the user pleases, provided a keyword is not used outside its purpose

Methods

`set()`
    Set values with keyword arguments

.. code:: python

    >>> c.set(text="red", effect="bold", background="blue")
    >>> c.set("red", "bold", "blue")
    >>> c.set(114)
    >>> print(c.__dict__)
..

.. code:: python

    {'text': 1, 'effect': 1, 'background': 4}
..

    `Set a new class with a keyword (any key) followed by a dict value`

.. code:: python

    >>> c.set(
            red={"text": "red"},
            bold_red={"text": "red", "effect": "bold"},
            yellow={"text": "yellow"}
        )
    >>> c.yellow.set(effect="bold")
    >>> print(c.__dict__)
..
.. code:: python

    {
        'text': 1,
        'effect': 1,
        'background': 4,
        'red': <object_colors.Color object at 0x0000020C10D06080>,
        'bold_red': <object_colors.Color object at 0x0000020C10D066D8>,
        'yellow': <object_colors.Color object at 0x0000020C10D06B00>
    }
..
.. code:: python

    >>> print(c.yellow.__dict__)
..
.. code:: python

    {'text': 3, 'effect': 1, 'background': 0}
..

`get()`
    Store values for multicolored printing

.. code:: python

    >>> bullet = c.red.get("[!] ")
    >>> warning = c.yellow("Warning")
    >>> print(bullet + warning)
..

    returns a string or a tuple

.. code:: python

    >>> a, b, c = c.red.get("a", "b", "c")

..

print()
    Instance includes enhanced print() function for color output

.. code:: python

    >>> c.print("no color print")
    >>> c.red.print("red print", flush=True)
    >>> c.yellow.print("yellow print", end="")
..

`pop()`
    Remove unused attributes

.. code:: python

    >>> c.pop("bold_red")
    >>> print(c.__dict__)
..

.. code:: python

    {
        'text': 1,
        'effect': 1,
        'background': 4,
        'red': <object_colors.Color object at 0x0000020C10D06080>,
        'yellow': <object_colors.Color object at 0x0000020C10D06B00>
    }
..

    Or create new instances

.. code:: python

    >>> red = c.pop("red")
    >>> print(c.__dict__)
..

.. code:: python

    {
        'text': 1,
        'effect': 1,
        'background': 4,
        'yellow': <object_colors.Color object at 0x0000020C10D06B00>
    }
..

.. code:: python

    >>> print(red.__dict__)
..

.. code:: python

    {'text': 1, 'effect': 0, 'background': 0}
..

.. code:: python

    >>> red.print()
    >>> red.get()
    >>> red.set()
..
