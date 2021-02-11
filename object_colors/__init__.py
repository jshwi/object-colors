"""
object-colors
=============

Object-oriented library for stylizing terminal output.
"""

import colorama

__version__ = "1.0.8"


class Color:
    """Color object."""

    keys = ["fore", "effect", "back"]
    opts = {
        "colors": [
            "black",
            "red",
            "green",
            "yellow",
            "blue",
            "purple",
            "cyan",
            "white",
        ],
        "effect": ["none", "bold", "bright", "underline", "negative"],
    }
    code = "\u001b"
    reset = f"{code}[0;0m"
    colorama.init()

    def __init__(self, *args, **kwargs):
        self.fore = 7
        self.effect = 0
        self.back = 0
        self.set(*args, **kwargs)

    def __getattr__(self, item):
        # look up dynamic subclasses
        return item

    def __dir__(self):
        # primarily here so linters know that the subclass calling
        # methods are not strings strings attempting to call attributes
        return [str(item) for item in self.__dict__]

    def _get_colored_tuple(self, args):
        args = list(args)
        # replace tuples containing strings with corresponding colored
        # strings
        for count, arg in enumerate(args):
            args[count] = self._get_colored_str(arg)

        return tuple(args)

    def _color_settings(self):
        # get the colored string with ansi-escape code settings added
        return f"{Color.code}[{self.effect};3{self.fore};4{self.back}m"

    def _get_colored_str(self, _str):
        setting = self._color_settings()
        return f"{setting}{_str}{self.reset}"

    @staticmethod
    def _get_opts(key):
        # get list of values to represent ansi escape codes whether
        # colors are needed or effects are needed
        if key in Color.opts:
            return Color.opts[key]

        return Color.opts["colors"]

    def _populate_defaults(self, kwargs):
        # Set any gaps in kwargs with the existing class values
        # (not subclasses) so as not to override them with the defaults
        for key in self.__dict__:
            if key in Color.keys and key not in kwargs:
                kwargs[key] = self.__dict__[key]

        return kwargs

    @staticmethod
    def _resolve_arg_type(arg):
        # if codes are entered all together e.g.
        # >>> color = Color(112)
        # {"fore": "red", "effect": "bold", "back": "green"}
        # then separate them to be used as individual arguments
        # otherwise return as is
        if isinstance(arg, int):
            for item in list(str(arg)):
                return int(item)

        return arg

    def _process_args(self, args):
        # e.g. instead of fore="red", effect="bold", back="blue"
        # 114 would get the same result
        args = list(args)
        for count, arg in enumerate(args):
            args[count] = self._resolve_arg_type(arg)

        return args

    @staticmethod
    def _kwargs_in_range(index_, args, kwargs, key):
        # the index is good to use if the value is not None and is less
        # than the length of the arguments given
        if 0 <= index_ < len(args):
            kwargs.update({key: args[index_]})

        return kwargs

    @staticmethod
    def _keywords_not_ready(key, kwargs, opts):
        # determine whether keyword arguments provided aren't valid
        # check whether the args given are not integers or are not
        # within the length of opts that can be used
        # return positive value if kwargs will need to be resolved
        if key in kwargs:
            return not isinstance(kwargs[key], int) or kwargs[key] > len(opts)

        return True

    @staticmethod
    def _resolve_alternate_opts(key, kwargs, opts, default):
        # will assign the default value to kwargs if invalid value is
        # provided otherwise if keypair is string - but valid - value
        # will be converted to integer
        if key not in kwargs or key in kwargs and kwargs[key] not in opts:
            kwargs.update({key: default})

        elif kwargs[key] in opts:
            kwargs.update({key: opts.index(kwargs[key])})

        return kwargs

    def _resolve_kwargs(self, key, kwargs):
        # if kwargs are not able to be used as they are then run methods
        # which convert kwargs from alternative values to integer codes
        default = 7 if key == "fore" else 0
        opts = self._get_opts(key)
        if self._keywords_not_ready(key, kwargs, opts):
            kwargs = self._resolve_alternate_opts(key, kwargs, opts, default)

        return kwargs

    def _get_processed(self, args, kwargs):
        # organise args and kwargs into a parsable dictionary
        # ensure values given are withing the range of values that can
        # be used and if they aren't instantiate with default values
        # check whether keywords are good to go or need to be resolved
        # first
        for index_, key in enumerate(Color.keys):
            kwargs = self._kwargs_in_range(index_, args, kwargs, key)
            kwargs = self._resolve_kwargs(key, kwargs)

        return kwargs

    def _set_subclass(self, key, value, args):
        # set subclass as an instance attribute so dynamic names are
        # recognised as correct attributes belonging to class
        value = self._get_processed(args, value)
        color = Color(*args, **value)
        setattr(self, key, color)

    def _make_subclass(self, args, kwargs):
        # make subclass attribute and return boolean value so method
        # calling this method can determine whether subclass has
        # successfully been made
        for key, value in list(kwargs.items()):
            if isinstance(value, dict):
                self._set_subclass(key, value, args)
                return True

        return False

    def _set_class_attrs(self, args, kwargs):
        # if not making a subclass then process args and kwargs and add
        # compiled dict to masterclass
        if not self._make_subclass(args, kwargs):
            params = self._get_processed(args, kwargs)
            self.__dict__.update(params)

    def _set_bold_attr(self):
        # Instantiate bold class object if bold is not set for more
        # flexible usage and less setting up when using this module to
        # manipulate particular colored strings
        bold = {
            "bold": {
                "fore": self.__dict__["fore"],
                "effect": "bold",
                "back": self.__dict__["back"],
            }
        }
        self._make_subclass((), bold)

    def _bold_switch(self):
        # bold switch:
        # - if used in a class instantiated as bold, switch bold off
        # - if used in a class instantiated without bold, switch bold on
        if self.effect != 1:
            self._set_bold_attr()

    def populate_colors(self):
        """This will create a subclass for every available color"""
        for color in self._get_opts("colors"):
            kwargs = {color: {"fore": color}}
            self._make_subclass((), kwargs)

    def set(self, *args, **kwargs):
        """Call to set new instance values

        :param args:    Colors or effects as integers or strings
        :param kwargs:  More precise keyword arguments
        """
        kwargs = self._populate_defaults(kwargs)
        args = self._process_args(args)
        self._set_class_attrs(args, kwargs)
        self._bold_switch()

    def get(self, *args):
        """Return colored string

        :param args:    Manipulate string(s)
        :return:        Colored string
        """
        if len(args) > 1:
            return self._get_colored_tuple(args)

        return self._get_colored_str(args[0])

    def print(self, *args, **kwargs):
        """Print colored strings straight to stdout
        builtin print() kwargs valid keyword arguments

        :param args:    Arbitrary number of strings or integers
        :param kwargs:  builtin print() kwargs
        """
        print(self.get(*args), **kwargs)
