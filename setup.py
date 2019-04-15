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

from os import getenv
from setuptools import setup, find_packages

def version_suffix():
    """Returns the version suffix."""
    value = "b2"
    build = getenv("BITBUCKET_BUILD_NUMBER")
    if build is not None:
        value = ".dev" + build
    return value

if __name__ == "__main__":
    setup(
        name="prcslib",
        version="1.0" + version_suffix(),
        description="Python API for Project Revision Control System (PRCS).",
        url="https://vx68k.bitbucket.io/prcslib-python/",
        author="Kaz Nishimura",
        author_email="kazssym@vx68k.org",
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
        ],
        obsoletes=["prcs2hg (< 2.0)"],

        python_requires=">= 3",
        packages=find_packages(exclude=["testsuite", "testsuite.*"]),
        test_suite="testsuite",
    )
