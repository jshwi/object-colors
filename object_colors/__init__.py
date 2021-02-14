"""
object-colors
=============

Object-oriented library for stylizing terminal output.
"""
import builtins

import colorama

__version__ = "1.0.8"


class Color:
    """Color object."""

    effects = ("none", "bold", "bright", "underline", "negative")
    colors = (
        "black",
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
        "white",
    )
    _opts = dict(effect=effects, fore=colors, back=colors)
    colorama.init()

    def __init__(self, effect=0, fore=7, back=None):
        self.effect = effect
        self.fore = fore
        self.back = back
        self.set(effect=effect, fore=fore, back=back)

    def __getattr__(self, item):
        # look up dynamic subclasses
        return item

    def __dir__(self):
        # primarily here so linters know that the subclass calling
        # methods are not strings attempting to call attributes
        return tuple([str(item) for item in self.__dict__])

    def __repr__(self):
        """View the containing attributes within the ``str``
        representation.

        :return:  ``str`` representation of this class.
        """
        return "{}({})".format(
            type(self).__name__,
            ", ".join(
                "{}={}".format(k, v)
                if not isinstance(v, dict)
                else "objects({})".format(", ".join(v))
                for k, v in vars(self).items()
            ),
        )

    def _get_colored_str(self, _str):
        # get the colored string with ANSI escape code settings added
        return "\u001b[{};3{}{}m{}\u001b[0;0m".format(
            self.effect,
            self.fore,
            f";4{self.back}" if self.back is not None else "",
            _str,
        )

    def _get_processed(self, **kwargs):
        # organise args and kwargs into a parsable dictionary
        # ensure values given are withing the range of values that can
        # be used and if they aren't instantiate with default values
        # check whether keywords are good to go or need to be resolved
        # first
        for key, value in dict(kwargs).items():

            # determine whether keyword arguments provided aren't valid
            # check whether the args given are not integers or are not
            # within the length of opts that can be used
            # return positive value if kwargs will need to be resolved
            if isinstance(value, str):
                kwargs.update({key: self._opts[key].index(value)})

        return kwargs

    def _make_subclass(self, **kwargs):
        # make subclass attribute and return boolean value so method
        # calling this method can determine whether subclass has
        # successfully been made
        for key, value in list(kwargs.items()):
            if isinstance(value, dict):

                # set subclass as an instance attribute so dynamic names
                # are recognised as correct attributes belonging to
                # class
                value = self._get_processed(**value)
                color = Color(**value)
                setattr(self, key, color)
                return True

        return False

    def populate_colors(self):
        """This will create a subclass for every available color"""
        for color in self.colors:
            kwargs = {color: {"fore": color}}
            self._make_subclass(**kwargs)

    def set(self, **kwargs):
        """Call to set new instance values

        :param kwargs:  More precise keyword arguments
        """
        # if not making a subclass then process args and kwargs and add
        # compiled dict to masterclass
        if not self._make_subclass(**kwargs):
            params = self._get_processed(**kwargs)
            for key, value in params.items():
                setattr(self, key, value)

        # bold switch:
        # - if used in a class instantiated as bold, switch bold off
        # - if used in a class instantiated without bold, switch bold on
        if self.effect != 1:

            # Instantiate bold class object if bold is not set for more
            # flexible usage and less setting up when using this module
            # to manipulate particular colored strings
            self._make_subclass(
                bold={
                    "fore": self.__dict__["fore"],
                    "effect": "bold",
                    "back": self.__dict__["back"],
                }
            )

    def get(self, *args, **kwargs):
        """Return colored ``str`` or ``tuple`` depending on the arg
        passed to method.

        :param args:    Manipulate string(s).
        :key format:    Return a string instead of a tuple if strings
                        are passed as tuple.
        :return:        Colored string.
        """
        if len(args) > 1:
            if kwargs.get("format", False):
                return self._get_colored_str(" ".join(args))

            return tuple(self._get_colored_str(i) for i in list(args))

        return self._get_colored_str(args[0])

    def print(self, *args, **kwargs):
        """Print colored strings straight to stdout. Prints the values
        to a stream, or to sys.stdout by default.

        :param args:    String or strings to print.
        :key file:      A file-like object (stream); defaults to the
                        current sys.stdout.
        :key sep:       String inserted between values, default a space.
        :key end:       String appended after the last value, default a
                        newline.
        :key flush:     Whether to forcibly flush the stream.
        """
        builtins.print(self.get(*args, format=True), **kwargs)
