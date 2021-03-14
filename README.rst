object-colors
=============
.. image:: https://github.com/jshwi/object-colors/workflows/build/badge.svg
    :target: https://github.com/jshwi/object_colors/workflows/build/badge.svg
    :alt: build
.. image:: https://img.shields.io/badge/python-3.8-blue.svg
    :target: https://www.python.org/downloads/release/python-380
    :alt: python3.8
.. image:: https://img.shields.io/pypi/v/object-colors
    :target: https://img.shields.io/pypi/v/object-colors
    :alt: pypi
.. image:: https://codecov.io/gh/jshwi/object-colors/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jshwi/object-colors
    :alt: codecov.io
.. image:: https://readthedocs.org/projects/object-colors/badge/?version=latest
    :target: https://object-colors.readthedocs.io/en/latest/?badge=latest
    :alt: readthedocs.org
.. image:: https://img.shields.io/badge/License-MIT-blue.svg
    :target: https://lbesson.mit-license.org/
    :alt: mit
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: black

Installation

.. code-block:: console

    pip install object-colors

Setup

.. code-block:: python

    >>> from object_colors import Color
    >>> c = Color()
..

    Without keywords args are positional like so:

.. code-block:: python

    >>> from object_colors import Color
    >>> Color("text", "effect", "background")

..

    - colors:

      - black:        0
      - red:          1
      - green:        2
      - yellow:       3
      - blue:         4
      - purple:       5
      - cyan:         6
      - white:        7

    - effects:

      - None:         0
      - bold:         1
      - bright:       2
      - underline:    3
      - negative:     4


.. code-block:: python

    >>> from object_colors import Color
    >>> c = Color()
    >>> c.set(2, 1, 1)
..

    - text:       green
    - effect:     bold
    - background: red

.. code-block:: python

    >>> from object_colors import Color
    >>> c = Color()
    >>> # instance attributes
    >>> c.set(
    ...     text="green",
    ...     effect="bold",
    ...     background="red"
    ... )
..

.. code-block:: python

    >>> from object_colors import Color
    >>> c = Color()
    >>> # subclasses -  set like those for
    >>> # original class only keyword arguments
    >>> # are expressed as dictionary
    >>> c.set(
    ...     sub_color={
    ...         "text": "green",
    ...         "effect": "bold",
    ...         "background": "red"
    ...     }
    ... )
..

    For most versatile usage simply instantiate the class with the populate_colors() method
    This will populate the instance with a subclass for every key in the "colors" object

.. code-block:: python

    >>> from object_colors import Color
    >>> c = Color()
    >>> c.populate_colors()
    >>> print(c.__dict__)
    {'text': 7, 'effect': 0, 'background': 0, 'bold': <object_colors.Color object at 0x7f3303b09a90>, 'black': <object_colors.Color object at 0x7f3302cf4b10>, 'red': <object_colors.Color object at 0x7f3303aa5d10>, 'green': <object_colors.Color object at 0x7f33037a7710>, 'yellow': <object_colors.Color object at 0x7f3302bd4710>, 'blue': <object_colors.Color object at 0x7f3302bd4d50>, 'purple': <object_colors.Color object at 0x7f3302ce0910>, 'cyan': <object_colors.Color object at 0x7f33037ddc10>, 'white': <object_colors.Color object at 0x7f33005e4c10>}
..

    This can be further enhanced with the Color.bold object, initialized when bold has not been activated

.. code-block:: python

    >>> from object_colors import Color
    >>> c = Color()
    >>> c.set(red={"text": "red"})
    >>> c.red.print("not bold")
    '\u001b[0;31;40mnot bold\u001b[0;0m'
    >>> c.red.bold.print("bold")
    '\u001b[1;31;40mbold\u001b[0;0m'
..

    All colors, effects and objects can be manipulated however the user pleases, provided a keyword is not used outside its purpose

Methods

- set():

.. code-block:: python

    >>> from object_colors import Color
    >>> c = Color()
    >>> # Set values with keyword arguments
    >>> c.set(text="red", effect="bold", background="blue")
    >>> c.set("red", "bold", "blue")
    >>> c.set(114)
    >>> print(c.__dict__)
    {'text': 1, 'effect': 1, 'background': 4, 'bold': <object_colors.Color object at 0x7f3303b09a90>}
..

.. code-block:: python

    >>> from object_colors import Color
    >>> c = Color()
    >>> # Set a new class with a keyword (any key) followed by a dict
    >>> # value
    >>> c.set(red={"text": "red"})
    >>> c.set(yellow={"text": "yellow"})
    >>> print(c.__dict__)
    {'text': 7, 'effect': 0, 'background': 0, 'bold': <object_colors.Color object at 0x7f3303b09a90>, 'red': <object_colors.Color object at 0x0000020C10D06080>, 'yellow': <object_colors.Color object at 0x0000020C10D06B00>}
..

.. code-block:: python

    >>> from object_colors import Color
    >>> c = Color()
    >>> c.set(yellow={"text": "yellow"})
    >>> print(c.yellow.__dict__)
    {'text': 3, 'effect': 0, 'background': 0, 'bold': <object_colors.Color object at 0x7f3303b09a90>}
..

- get():

.. code-block:: python

    >>> from object_colors import Color
    >>> c = Color()
    >>> # store values
    >>> # useful for multicolored printing
    >>> c.set(red={"text": "red"})
    >>> c.set(yellow={"text": "yellow"})
    >>> bullet = c.red.get("[!] ")
    >>> warning = c.yellow.get("Warning")
    >>> print(bullet + warning)
    '\u001b[0;31;40m[!] \u001b[0;0m\u001b[0;33;40mWarning\u001b[0;0m'
..

.. code-block:: python

    >>> from object_colors import Color
    >>> c = Color()
    >>> c.set(red={"text": "red"})
    >>> # returns a string or a tuple
    >>> a, b, c = c.red.get("a", "b", "c")
..

- print():

.. code-block:: python

    >>> from object_colors import Color
    >>> c = Color()
    >>> c.set(red={"text": "red"})
    >>> c.set(yellow={"text": "yellow"})
    >>> # Instance includes enhanced print() function for color output
    >>> c.print("no color print")
    '\u001b[0;37;40mno color print\u001b[0;0m'
    >>> c.red.print("red print", flush=True)
    '\u001b[0;31;40mred print\u001b[0;0m'
    >>> c.yellow.print("yellow print", end="")
    '\u001b[0;33;40myellow print\u001b[0;0m'
..

- pop():

.. code-block:: python

    >>> from object_colors import Color
    >>> c = Color()
    >>> c.set(red={"text": "red"})
    >>> c.set(yellow={"text": "yellow"})
    >>> # remove unused attributes
    >>> c.pop("bold_red")
    >>> print(c.__dict__)
    {'text': 7, 'effect': 0, 'background': 0, 'bold': <object_colors.Color object at 0x7f3303b09a90>, 'red': <object_colors.Color object at 0x0000020C10D06080>, 'yellow': <object_colors.Color object at 0x0000020C10D06B00>}
    >>> # or create new instances
    >>> red = c.pop("red")
    >>> print(c.__dict__)
    {'text': 7, 'effect': 0, 'background': 0, 'bold': <object_colors.Color object at 0x7f3303b09a90>, 'yellow': <object_colors.Color object at 0x0000020C10D06B00>}
    >>> print(red.__dict__)
    {'text': 1, 'effect': 0, 'background': 0, 'bold': <object_colors.Color object at 0x7f3303b09a90>}
..
