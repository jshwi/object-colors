object-colors
=============
.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License
.. image:: https://img.shields.io/pypi/v/object-colors
    :target: https://pypi.org/project/object-colors/
    :alt: PyPI
.. image:: https://github.com/jshwi/object-colors/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/jshwi/object-colors/actions/workflows/ci.yml
    :alt: CI
.. image:: https://results.pre-commit.ci/badge/github/jshwi/object-colors/master.svg
   :target: https://results.pre-commit.ci/latest/github/jshwi/object-colors/master
   :alt: pre-commit.ci status
.. image:: https://github.com/jshwi/object-colors/actions/workflows/codeql-analysis.yml/badge.svg
    :target: https://github.com/jshwi/object-colors/actions/workflows/codeql-analysis.yml
    :alt: CodeQL
.. image:: https://codecov.io/gh/jshwi/object-colors/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jshwi/object-colors
    :alt: codecov.io
.. image:: https://readthedocs.org/projects/object-colors/badge/?version=latest
    :target: https://object-colors.readthedocs.io/en/latest/?badge=latest
    :alt: readthedocs.org
.. image:: https://img.shields.io/badge/python-3.8-blue.svg
    :target: https://www.python.org/downloads/release/python-380
    :alt: python3.8
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Black
.. image:: https://img.shields.io/badge/linting-pylint-yellowgreen
    :target: https://github.com/PyCQA/pylint
    :alt: pylint

Object-oriented library for stylizing terminal output
-----------------------------------------------------

Installation
------------

.. code-block:: console

    $ pip install object-colors
..

Usage
-----

Import the ``Color`` object from ``object_colors``

.. code-block:: python

    >>> from object_colors import Color

Args can be provided as strings or as indices corresponding to their index in an ANSI escape sequence

.. code-block:: python

    >>> Color(effect="bold", fore="red", back="green")
    Color(effect=1, fore=1, back=2, objects())

The following would yield the same result

.. code-block:: python

    >>> Color(effect=1, fore=1, back=2)
    Color(effect=1, fore=1, back=2, objects())

The above options are part of the below mapping

.. code-block:: python

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

.. code-block:: python

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


To configure the current object either ``effect``, ``fore``, or ``back`` can be provided

They must be an ``int``, ``str``, or ``None`` type

.. code-block:: python

    >>> c = Color()
    >>> c.set(effect="bold", fore="red", back="red")
    >>> c
    Color(effect=1, fore=1, back=1, objects())

Create new objects with by providing a ``dict`` object with any keyword argument

Use ``set`` to set multiple parameters

.. code-block:: python

    >>> c = Color()
    >>> c.set(bold_green=dict(effect="bold", fore="green"))
    >>> c
    Color(effect=None, fore=None, back=None, objects(bold_green))

Return ``str`` or ``tuple`` using ``get``

.. code-block:: python

    >>> c = Color()
    >>> c.set(red=dict(fore="red"))
    >>> c.set(yellow=dict(fore="yellow"))
    >>> f"{c.red.get('*')} {c.yellow.get('Warning')}"
    '\x1b[31m*\x1b[0;0m \x1b[33mWarning\x1b[0;0m'

.. code-block:: python

    >>> c = Color()
    >>> c.set(red=dict(fore="red"))
    >>> xyz = c.red.get("x", "y", "z")
    >>> xyz
    ('\x1b[31mx\x1b[0;0m', '\x1b[31my\x1b[0;0m', '\x1b[31mz\x1b[0;0m')
    >>> x, y, z = xyz
    >>> f"{x} {y} {z}"
    '\x1b[31mx\x1b[0;0m \x1b[31my\x1b[0;0m \x1b[31mz\x1b[0;0m'

Print the result using ``print``

.. code-block:: python

    >>> c = Color(effect="bold", fore="cyan")
    >>> # doctest strips ansi codes from print
    >>> c.print("bold cyan")  # '\x1b[1;36mbold cyan\x1b[0;0m'
    bold cyan

Load all ``effect``, ``fore``, or ``back`` elements using ``populate()``

.. code-block:: python

    >>> c = Color()
    >>> c.populate("fore")
    >>> c
    Color(effect=None, fore=None, back=None, objects(black, red, green, yellow, blue, magenta, cyan, white))

.. code-block:: python

    >>> c = Color()
    >>> c.set(red=dict(fore="red"))
    >>> c.red.populate("effect")
    >>> c.red
    Color(effect=None, fore=1, back=None, objects(none, bold, dim, italic, underline, blink, blinking, negative, empty, strikethrough))
    >>> # doctest strips ansi codes from print
    >>> c.red.strikethrough.print("strikethrough red")  # '\x1b[9;31mstrikethrough red\x1b[0;0m'
    strikethrough red
