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
    .. code:: javascript

        keys = ["text", "effect", "background"]
        values = {
            "colors": ["black", "red", "green", "yellow", "blue", "purple", "cyan", "white"]
            "effects": ['none', "bold", 'bright', "underline", "negative"]
        }
    ..

    "text" and "background" are matched with colors, and "effect" is match with
    effects


* set()

    * Values

        >>> c.set(text="red", effect="bold", background="blue")
        >>> c.set("red", "bold", "blue")
        >>> c.set(114)

        .. code:: python

                {'text': 1, 'effect': 1, 'background': 4}
        ..


    * New classes

        .. code:: python

            c.set(
                red={"text": "red"},
                bold_red={"text": "red", "effect": "bold"},
                yellow={"text": "yellow"}
            )
        ..

        >>> c.yellow.set(effect="bold")
        >>> print(c.__dict__)

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

        >>> print(c.yellow.__dict__)

        .. code:: python

            {'text': 3, 'effect': 1, 'background': 0}
        ..

* print()

    * Instance includes enhanced print() function for color output

        >>> c.print("no color print")
        >>> c.red.print("red print", flush=True)
        >>> c.yellow.print("yellow print", end="")

* get()

    * Store values for multicolored printing

        >>> bullet = c.red.get("[!] ")
        >>> warning = c.yellow("Warning")
        >>> print(bullet + warning)


* pop()

    * Remove unused attributes

        >>> c.pop("bold_red")
        >>> print(c.__dict__)

        .. code:: python

            {
                'text': 1,
                'effect': 1,
                'background': 4,
                'red': <object_colors.Color object at 0x0000020C10D06080>,
                'yellow': <object_colors.Color object at 0x0000020C10D06B00>
            }
        ..



    * Or create brand new instances

        >>> red = c.pop("red")
        >>> print(c.__dict__)

        .. code:: python

            {
                'text': 1,
                'effect': 1,
                'background': 4,
                'yellow': <object_colors.Color object at 0x0000020C10D06B00>
            }
        ..

        >>> print(red.__dict__)

        .. code:: python

            {'red': <object_colors.Color object at 0x0000020C10D06080>}
        ..

        >>> red.print()
        >>> red.get()
        >>> red.set()