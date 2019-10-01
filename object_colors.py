#!/usr/bin/env python3
"""object_colors

This is a simple to use module designed to print to the terminal in
color with minimal setup and instantiation
"""
from json import dumps
from typing import Union, Any


class Color:
    """Instantiate with escape codes, values or key-values and get or
    print processed arguments
    """
    def __init__(self, *args: Any, **kwargs: Union[str, int, dict]):
        """Set desired attributes for Color.print() or Color.get()

        :param args:    Codes can be entered in any number of arguments
                        The first three integers/strings will be used
        :param kwargs:  Three specific keys can be used
                        color, effect, background
        """
        self.color = 9
        self.effect = 0
        self.background = 9
        self.set(*args, **kwargs)

    def __call__(self, *args: Any, **kwargs: Union[str, int, dict]):
        self.set(*args, **kwargs)

    def __getattr__(self, item: str) -> str:
        return self[item]

    def __dir__(self) -> list:
        return [str(k) for k in self.__dict__]

    def set(self, *args: Any, **kwargs: Union[str, int, dict]):
        """

        :param args:
        :param kwargs:
        """
        self.process_args_kwargs(args, kwargs)

    @staticmethod
    def process_args(args: Any) -> list:
        """e.g. instead of color="red", effect="bold", background="blue"
        114 will get the same result

        :param args:    Integer list or individual args
        :return:        List to be iterated through for arguments
        """
        values = []
        for arg in args:
            if isinstance(arg, int):
                items = list(str(arg))
                for item in items:
                    values.append(int(item))
            else:
                values.append(arg)
        return values

    @staticmethod
    def get_opts(key: str) -> list:
        """Match against args then convert to int for escape codes

        :param key: Keyword to match with list of valid arguments
        :return:    List to validate argument
        """
        if key == 'effect':
            return [None, "bold", "underline", "negative"]
        return ["black", "red", "green", "yellow", "blue", "purple", "cyan"]

    def process_args_kwargs(self, args: Any, kwargs: dict):
        """Compile the dictionary to be used as values for get and print

        :param args:    Class arguments
        :param kwargs   Class keyword-arguments
                        returned list and dict will replace the arg and
                        kwarg parameters
        :return:        validated dictionary for class __dict__
        """
        args = self.process_args(args)
        for key, val in list(kwargs.items()):
            if isinstance(val, dict):
                val = self.process_kwargs(args, val)
                color = Color(*args, **val)
                setattr(self, key, color)
                return
        self.__dict__.update(self.process_kwargs(args, kwargs))
        return

    def process_kwargs(self, args: Any, kwargs: dict) -> dict:
        """Organise arguments and keyword arguments into a valid
        dictionary

        :param args:    User defined arguments: list(s) of integers or
                        tuple of strings
        :param kwargs:  Keyword arguments for class attributes or new
                        subclass attributes
        :return:        Dictionary for class attributes
        """
        keys = ["color", "effect", "background"]
        for idx, key in enumerate(keys):
            opts = self.get_opts(key)
            val = 0 if key == "effect" else 9
            if 0 <= idx < len(args):
                val = args[idx]
            elif key in kwargs and kwargs[key] in opts:
                val = kwargs[key]
            elif key in kwargs and 0 <= idx < len(opts):
                continue
            val = opts.index(val) if isinstance(val, str) else val
            kwargs.update({key: val})
        return kwargs

    def get(self, string: str) -> str:
        """String can be return as variables for mixed printing or can
        be printed directly by calling Color.print() instead of
        Color.get()

        :param string:  User args to be processed
        :return:        Colored string
        """
        color = f"3{self.color}"
        effect = self.effect
        background = f"4{self.background}"
        return f"\033[{effect};{color};{background}m{string}\033[0;0m"

    def print(self, *args: Any, **kwargs: Union[str, int]):
        """Enhanced print function for class and subclasses

        :param args:    Variable number of strings can be entered if
                        syntax allows so this method behaves just like
                        the __builtin__
        :param kwargs:  Keyword arguments for print() function
        """
        print(self.get(" ".join(str(string) for string in args)), **kwargs)

    def pop(self, select: str) -> Union[str, dict, None]:
        """Delete key and value from list and return them to a variable,
        if that's what you want to do...

        :param select:  Key selection to delete
        :return:        Dictionary item if removing class, str if a
                        keypair and None if there was nothing to remove
        """
        for key in list(self.__dict__):
            if select == key:
                popped = self.__dict__[key]
                del self.__dict__[key]
                if isinstance(popped, Color):
                    return {key: popped.__dict__}
                return popped
        return

    def vals(self):
        """Resolve type errors for the various types that the class may
        contain so that they may be printed as a string

        :return: Temporary key values to be printed in a readable form
        """
        key_values = {}
        for key in self.__dict__:
            opts = self.get_opts(key)
            try:
                value = opts[self.__dict__[key]]
            except TypeError:
                value = self.__dict__[key]
            except IndexError:
                value = None
            key_values[key] = value
        while True:
            try:
                print(dumps(key_values, indent=4, sort_keys=True))
                break
            except TypeError:
                for key, value in key_values.items():
                    try:
                        value = value.__dict__
                        key_values[key] = value
                    except AttributeError:
                        continue
