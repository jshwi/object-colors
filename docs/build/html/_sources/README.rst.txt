=======================================================
The minimalist - all purpose - color class for printing
=======================================================

Installation

.. code-block:: console

    pip install object-colors

Setup

.. code:: python

    from object_colors import Color
    c = Color()
..

Usage

* key-values
    Match `effects` with `effect` and `colors` with `text` and `background`

    .. code:: javascript

        keys = ["text", "effect", "background"]
        values = {
            "colors": ["black", "red", "green", "yellow", "blue", "purple", "cyan", "white"]
            "effects": ['none', "bold", 'bright', "underline", "negative"]
        }
    ..

Methods

* set()
    `Set values with keyword arguments`

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

* print()
    `Instance includes enhanced print() function for color output`

    .. code:: python

        >>> c.print("no color print")
        >>> c.red.print("red print", flush=True)
        >>> c.yellow.print("yellow print", end="")
    ..

* get()
    `Store values for multicolored printing`

    .. code:: python

        >>> bullet = c.red.get("[!] ")
        >>> warning = c.yellow("Warning")
        >>> print(bullet + warning)
    ..

* pop()
    `Remove unused attributes`

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

    `Or create new instances`

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
