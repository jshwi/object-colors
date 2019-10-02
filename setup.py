from pathlib import Path

from setuptools import setup, find_packages

HERE = Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="object-colors",
    version="1.0.1",
    description='Adding colours to Python terminal simplified into a single class',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/jshwi/object_colors',
    author='Stephen Whitlock',
    author_email='stephen@jshwisolutions.com',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    py_modules=['object_colors'],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
)
