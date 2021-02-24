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

    *To configure the current object either ``effect``, ``fore``, or ``back`` can be provided and they must be an ``int``, ``str``, or ``None``*

    *Create new objects with by providing a ``dict`` object with any keyword argument*

    *Use ``set`` to set multiple parameters*

.. code-block:: python

    >>> from object_colors import Color
    >>> c = Color()
    >>> c.set(effect="bold", fore="red", back="red")
    >>> print(c)
    Color(effect=1, fore=1, back=1)
    >>> c.set(bold_green={"effect": "bold", "fore": "green"})
    >>> print(c)
    Color(effect=1, fore=1, back=1, bold_green=Color(effect=1, fore=2, back=None))
..

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

    *Load all ``effect``, ``fore``, or ``back`` elements using ``populate``*

.. code-block:: python

    >>> from object_colors import Color
    >>> c = Color()
    >>> c.populate("fore")
    >>> print(c)
    Color(effect=0, fore=7, back=None, black=Color(effect=0, fore=0, back=None), bold=Color(effect=1, fore=7, back=None), red=Color(effect=0, fore=1, back=None), green=Color(effect=0, fore=2, back=None), yellow=Color(effect=0, fore=3, back=None), blue=Color(effect=0, fore=4, back=None), magenta=Color(effect=0, fore=5, back=None), cyan=Color(effect=0, fore=6, back=None), white=Color(effect=0, fore=7, back=None))
    >>> c.red.populate("effect")
    >>> print(c.red)
    Color(effect=0, fore=1, back=None, none=Color(effect=0, fore=7, back=None), bold=Color(effect=1, fore=1, back=None), dim=Color(effect=2, fore=7, back=None), italic=Color(effect=3, fore=7, back=None), underline=Color(effect=4, fore=7, back=None), blink=Color(effect=5, fore=7, back=None), blinking=Color(effect=6, fore=7, back=None), negative=Color(effect=7, fore=7, back=None), empty=Color(effect=8, fore=7, back=None), strikethrough=Color(effect=9, fore=7, back=None))
..
