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
        # get the colored string with ansi-escape code settings added
        setting = f"{Color.code}[{self.effect};3{self.fore};4{self.back}m"
        return f"{setting}{_str}{self.reset}"

    @staticmethod
    def _get_opts(key):
        # get list of values to represent ansi escape codes whether
        # colors are needed or effects are needed
        if key in Color.opts:
            return Color.opts[key]

        return Color.opts["colors"]

    def _get_processed(self, args, kwargs):
        # organise args and kwargs into a parsable dictionary
        # ensure values given are withing the range of values that can
        # be used and if they aren't instantiate with default values
        # check whether keywords are good to go or need to be resolved
        # first
        for index_, key in enumerate(Color.keys):

            # the index is good to use if the value is not None and is
            # less than the length of the arguments given
            if 0 <= index_ < len(args):
                kwargs.update({key: args[index_]})

            # if kwargs are not able to be used as they are then run
            # methods which convert kwargs from alternative values to
            # integer codes
            default = 7 if key == "fore" else 0
            opts = self._get_opts(key)

            # determine whether keyword arguments provided aren't valid
            # check whether the args given are not integers or are not
            # within the length of opts that can be used
            # return positive value if kwargs will need to be resolved
            not_ready = True
            if key in kwargs:
                not_ready = not isinstance(kwargs[key], int) or kwargs[
                    key
                ] > len(opts)

            if not_ready:

                # will assign the default value to kwargs if invalid
                # value is provided otherwise if keypair is string -
                # but valid - value will be converted to integer
                if (
                    key not in kwargs
                    or key in kwargs
                    and kwargs[key] not in opts
                ):
                    kwargs.update({key: default})

                elif kwargs[key] in opts:
                    kwargs.update({key: opts.index(kwargs[key])})

        return kwargs

    def _make_subclass(self, args, kwargs):
        # make subclass attribute and return boolean value so method
        # calling this method can determine whether subclass has
        # successfully been made
        for key, value in list(kwargs.items()):
            if isinstance(value, dict):

                # set subclass as an instance attribute so dynamic names
                # are recognised as correct attributes belonging to
                # class
                value = self._get_processed(args, value)
                color = Color(*args, **value)
                setattr(self, key, color)
                return True

        return False

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
        # Set any gaps in kwargs with the existing class values
        # (not subclasses) so as not to override them with the defaults
        for key in self.__dict__:
            if key in Color.keys and key not in kwargs:
                kwargs[key] = self.__dict__[key]

        # e.g. instead of fore="red", effect="bold", back="blue"
        # 114 would get the same result
        args = list(args)
        for count, arg in enumerate(args):

            # if codes are entered all together then separate them to be
            # used as individual arguments otherwise return as is
            if isinstance(arg, int):
                args[count] = int(str(arg)[0])
            else:
                args[count] = arg

        # if not making a subclass then process args and kwargs and add
        # compiled dict to masterclass
        if not self._make_subclass(args, kwargs):
            params = self._get_processed(args, kwargs)
            self.__dict__.update(params)

        # bold switch:
        # - if used in a class instantiated as bold, switch bold off
        # - if used in a class instantiated without bold, switch bold on
        if self.effect != 1:

            # Instantiate bold class object if bold is not set for more
            # flexible usage and less setting up when using this module
            # to manipulate particular colored strings
            bold = {
                "bold": {
                    "fore": self.__dict__["fore"],
                    "effect": "bold",
                    "back": self.__dict__["back"],
                }
            }
            self._make_subclass((), bold)

    def get(self, *args):
        """Return colored string

        :param args:    Manipulate string(s)
        :return:        Colored string
        """
        if len(args) > 1:
            args = list(args)  # type: ignore

            # replace tuples containing strings with corresponding
            # colored strings
            for count, arg in enumerate(args):
                args[count] = self._get_colored_str(arg)  # type: ignore

            return tuple(args)

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
        builtins.print(self.get(*args), **kwargs)
