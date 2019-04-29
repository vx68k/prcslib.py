# setup - setup script for the prcslib package
# Copyright (C) 2019 Kaz Nishimura
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

"""setup script for the prcslib package
"""

from os import path
from setuptools import setup, find_packages

# Set this to 'True' if the current version is a snapshot.
_SNAPSHOT = False

def _version_suffix():
    """return the version suffix

    This method returns a string to be appended to the package version,
    or "" if none needed.
    """
    value = "b2"
    if _SNAPSHOT:
        from datetime import datetime
        timestamp = datetime.utcnow()
        value = timestamp.strftime(".dev%Y%m%d%H%M%S")
    return value

def long_description():
    """return the long description from the 'README.md' file
    """
    cwd = path.abspath(path.dirname(__file__))
    with open(path.join(cwd, "README.md"), encoding="UTF-8") as file:
        # To ignore lines until a level-1 ATX header is found.
        while True:
            line = file.readline()
            if line.startswith("# "):
                break
        return line + file.read()

if __name__ == "__main__":
    setup(
        name="prcslib",
        version="1.0" + _version_suffix(),
        description="Python API for PRCS.",
        url="https://vx68k.bitbucket.io/prcslib.py/",
        author="Kaz Nishimura",
        author_email="kazssym@vx68k.org",
        long_description=long_description(),
        long_description_content_type="text/markdown",
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
        ],
        obsoletes=["prcs2hg (< 2.0)"],
        python_requires=">= 3.4",

        packages=find_packages(exclude=["testsuite", "testsuite.*"]),
        test_suite="testsuite",
    )
