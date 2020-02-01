__author__ = "Stephen Whitlock"
__copyright__ = "Copyright 2019, Stephen Whitlock"
__license__ = "MIT"
__version__ = "1.0.8"
__maintainer__ = "Stephen Whitlock"
__email__ = "stephen@jshwisolutions.com"
__status__ = "Production"

from os import path
from pathlib import Path

from setuptools import setup, find_packages

HERE = Path(__file__).parent

README = (HERE / path.join("README.rst")).read_text()

setup(
    name="object-colors",
    version=__version__,
    description="Adding colours to Python simplified into a single class",
    long_description=README,
    long_description_content_type="text/x-rst",
    url="https://github.com/jshwi/object_colors",
    author=__author__,
    maintainer=__maintainer__,
    author_email=__email__,
    license=__license__,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    py_modules=["object_colors"],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    zip_safe=True,
    install_requires=["pytest"],
)
