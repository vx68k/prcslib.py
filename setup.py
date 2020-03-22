# setup.py - setup script for the 'prcslib' package
# Copyright (C) 2019-2020 Kaz Nishimura
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
# SPDX-License-Identifier: MIT

"""
setup script for the 'prcslib' package
"""

from os import path
from setuptools import setup, find_packages

# Package version.
PACKAGE_VERSION = "1.0"

def long_description():
    """
    return the long description from the 'README.md' file
    """
    cwd = path.abspath(path.dirname(__file__))
    with open(path.join(cwd, "README.md")) as stream:
        # To ignore lines until a level-1 ATX header is found.
        while True:
            line = stream.readline()
            if line.startswith("# "):
                break
        return line + stream.read()

if __name__ == "__main__":
    setup(
        name="prcslib",
        version=PACKAGE_VERSION,
        description="Python API for PRCS.",
        url="https://vx68k.bitbucket.io/prcslib.py/",
        author="Kaz Nishimura",
        author_email="kazssym@linuxfront.com",
        long_description=long_description(),
        long_description_content_type="text/markdown",
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 2.7",
            "Topic :: Software Development :: Version Control",
        ],
        obsoletes=["prcs2hg(<2.0)"],
        python_requires=">=2.7",

        packages=find_packages(exclude=["testsuite", "testsuite.*"]),
        test_suite="testsuite",
    )
