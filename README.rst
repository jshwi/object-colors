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

.. code-block:: python

    >>> from object_colors import Color
    >>> color = Color()
..

    Without keywords args are positional like so:

.. code-block:: python

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

    >>> color = Color()
    >>> color.set(2, 1, 1)
..

    - text:       green
    - effect:     bold
    - background: red

.. code-block:: python

    >>> color = Color()
..

.. code-block:: python

    >>> # instance attributes
    >>> color.set(
    ...     text="green",
    ...     effect="bold",
    ...     background="red"
    ... )
..

.. code-block:: python

    >>> # subclasses -  set like those for
    >>> # original class only keyword arguments
    >>> # are expressed as dictionary
    >>> color.set(
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

    >>> color = Color()
    >>> color.populate_colors()
    >>> print(color.__dict__)
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
..

    This can be further enhanced with the Color.bold object, initialized when bold has not been activated

.. code:: python

    >>> color.red.print("not bold")
    >>> color.red.bold.print("bold")
..

    All colors, effects and objects can be manipulated however the user pleases, provided a keyword is not used outside its purpose

Methods

- set():

.. code-block:: python

    >>> # Set values with keyword arguments
    >>> color.set(text="red", effect="bold", background="blue")
    >>> color.set("red", "bold", "blue")
    >>> color.set(114)
    >>> print(c.__dict__)
    {'text': 1, 'effect': 1, 'background': 4}
..

.. code-block:: python

    >>> # Set a new class with a keyword (any key) followed by a dict
    >>> # value
    >>> color.set(red={"text": "red"}, yellow={"text": "yellow"})
    >>> print(c.__dict__)
    'text': 1,
    'effect': 0,
    'background': 4,
    'red': <object_colors.Color object at 0x0000020C10D06080>,
    'yellow': <object_colors.Color object at 0x0000020C10D06B00>
..

.. code-block:: python

    >>> print(color.yellow.__dict__)
    {'text': 3, 'effect': 1, 'background': 0}
..

- get():

.. code-block:: python

    >>> # store values
    >>> # useful for multicolored printing
    >>> bullet = color.red.get("[!] ")
    >>> warning = color.yellow("Warning")
    >>> print(bullet + warning)
    "\u001b[0;31;40m[!]\u001b[0;0m\u001b[0;33;40mWarning\u001b[0;0m"
..

.. code-block:: python

    >>> # returns a string or a tuple
    >>> a, b, c = color.red.get("a", "b", "c")
..

- print():

.. code-block:: python

    >>> # Instance includes enhanced print() function for color output
    >>> color.print("no color print")
    >>> color.red.print("red print", flush=True)
    >>> color.yellow.print("yellow print", end="")
..

- pop():

.. code-block:: python

    >>> # remove unused attributes
    >>> color.pop("bold_red")
    >>> print(color.__dict__)
    'text': 1,
    'effect': 1,
    'background': 4,
    'red': <object_colors.Color object at 0x0000020C10D06080>,
    'yellow': <object_colors.Color object at 0x0000020C10D06B00>
..

.. code-block:: python

    >>> # or create new instances
    >>> red = color.pop("red")
    >>> print(color.__dict__)
    'text': 1,
    'effect': 1,
    'background': 4,
    'yellow': <object_colors.Color object at 0x0000020C10D06B00>
..

.. code-block:: python

    >>> print(red.__dict__)
    {'text': 1, 'effect': 0, 'background': 0}
..

.. code-block:: python

    >>> red.print()
    >>> red.get()
    >>> red.set()
..
