"""
setup
=====

``setuptools`` for package.
"""
import setuptools

with open("README.rst") as file:
    README = file.read()


setuptools.setup(
    name="object_colors",
    version="2.0.1",
    description="Adding colours to Python simplified into a single class",
    long_description=README,
    long_description_content_type="text/x-rst",
    author="Stephen Whitlock",
    author_email="stephen@jshwisolutions.com",
    url="https://github.com/jshwi/object-colors",
    license="MIT",
    platforms="GNU/Linux",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    keywords=[],
    packages=setuptools.find_packages(exclude=["tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=["colorama==0.4.4"],
    python_requires=">=3.8",
)
