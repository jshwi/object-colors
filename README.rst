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

Object-oriented library for stylizing terminal output

**Installation**

.. code-block:: console

    $ pip install object-colors
..

**Options**

    *Args can be provided as strings or as indices corresponding to their index in an ANSI escape sequence*

    *The following would yield the same result*

.. code-block:: python

    >>> from object_colors import Color
    >>> c = Color(effect="bold", fore="red", back="green")
    >>> print(vars(c))
    {'fore': 1, 'effect': 1, 'back': 2}
    >>> c = Color(effect=1, fore=1, back=2)
    >>> print(vars(c))
    {'fore': 1, 'effect': 1, 'back': 2}
..

    *The above options are part of the below mapping*

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

**Usage**

    *create new objects with ``set``*

.. code-block:: python

    >>> from object_colors import Color
    >>> c = Color()
    >>> c.set(fore="green", effect="bold", back="red")
    >>> print(vars(c))
    {'fore': 2, 'effect': 1, 'back': 1, 'bold': <object_colors.Color object at 0x7f11e209c8b0>}
    >>> c.set(bold_green={"fore": "green", "effect": "bold"})
    >>> print(vars(c))
    {'fore': 2, 'effect': 1, 'back': 1, 'bold': <object_colors.Color object at 0x7f11e20cbe80>, 'bold_green': <object_colors.Color object at 0x7f11e20cbe20>}
..

    *Return values using ``get``*

    *Return ``str`` or ``tuple`` using ``get``*

.. code-block:: python

    >>> from object_colors import Color
    >>> c = Color()
    >>> c.set(red={"fore": "red"})
    >>> c.set(yellow={"fore": "yellow"})
    >>> print(c.red.get("*") + " " + c.yellow.get("Warning"))
    '\u001b[0;31;40m*\u001b[0;0m \u001b[0;33;40mWarning\u001b[0;0m'
    >>> x, y, z = c.red.get("x", "y", "z")
    >>> print(x, y, z)
    '\u001b[0;31;40mx\u001b[0;0m \u001b[0;31;40my\u001b[0;0m \u001b[0;31;40mz\u001b[0;0m'
..

    *Print the result using ``print``*

.. code-block:: python

    >>> from object_colors import Color
    >>> c = Color(fore="cyan", effect="bold")
    >>> c.print("bold cyan")
    '\u001b[1;36;40mbold cyan\u001b[0;0m'
..

    *Load all colors using ``populate_colors``*

.. code-block:: python

    >>> from object_colors import Color
    >>> c = Color()
    >>> c.populate_colors()
    >>> c.red.print("red")
    '\u001b[0;31;40mred\u001b[0;0m'
    >>> c.green.print("green")
    '\u001b[0;32;40mgreen\u001b[0;0m'
    >>> c.yellow.print("yellow")
    '\u001b[0;33;40myellow\u001b[0;0m'
..
