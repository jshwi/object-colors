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
    >>> print(c)
    Color(effect=1, fore=1, back=2)
    >>> c = Color(effect=1, fore=1, back=2)
    >>> print(c)
    Color(effect=1, fore=1, back=2)
..

    *The above options are part of the below mapping*

.. code-block:: python

    >>> from object_colors import Color
    >>> for i, c in enumerate(Color.colors):
    ...     print(i, c)
    0 black
    1 red
    2 green
    3 yellow
    4 blue
    5 magenta
    6 cyan
    7 white
    >>> for i, e in enumerate(Color.effects):
    ...     print(i, e)
    0 none
    1 bold
    2 dim
    3 italic
    4 underline
    5 blink
    6 blinking
    7 negative
    8 empty
    9 strikethrough
..

**Usage**

    *create new objects with ``set``*

.. code-block:: python

    >>> from object_colors import Color
    >>> c = Color()
    >>> c.set(fore="green", effect="bold", back="red")
    >>> print(c)
    Color(effect=1, fore=2, back=1)
    >>> c.set(bold_green={"fore": "green", "effect": "bold"})
    >>> print(c)
    Color(effect=1, fore=2, back=1, bold_green=Color(effect=1, fore=2, back=None))
..

    *Return values using ``get``*

    *Return ``str`` or ``tuple`` using ``get``*

.. code-block:: python

    >>> from object_colors import Color
    >>> c = Color()
    >>> c.set(red={"fore": "red"})
    >>> c.set(yellow={"fore": "yellow"})
    >>> print(c.red.get("*") + " " + c.yellow.get("Warning"))
    '\u001b[0;31m*\u001b[0;0m \u001b[0;33mWarning\u001b[0;0m'
    >>> x, y, z = c.red.get("x", "y", "z")
    >>> print(x, y, z)
    '\u001b[0;31mx\u001b[0;0m \u001b[0;31my\u001b[0;0m \u001b[0;31mz\u001b[0;0m'
..

    *Print the result using ``print``*

.. code-block:: python

    >>> from object_colors import Color
    >>> c = Color(effect="bold", fore="cyan")
    >>> c.print("bold cyan")
    '\u001b[1;36mbold cyan\u001b[0;0m'
..

    *Load all colors using ``populate_colors``*

.. code-block:: python

    >>> from object_colors import Color
    >>> c = Color()
    >>> c.populate_colors()
    >>> c.red.print("red")
    '\u001b[0;31mred\u001b[0;0m'
    >>> c.green.print("green")
    '\u001b[0;32mgreen\u001b[0;0m'
    >>> c.yellow.print("yellow")
    '\u001b[0;33myellow\u001b[0;0m'
..
