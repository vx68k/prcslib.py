# sexp.stream - streaming API for S-expressions
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

"""streaming API for S-expressions

This package provides a streaming API for S-expressions.
"""

class SExpParserEvent:
    """S-expression parser event
    """

    START_LIST = "("
    END_LIST = ")"
    QUOTE = "'"
    VALUE_STRING = "string"
    VALUE_SYMBOL = "symbol"

    def __init__(self, eventtype, eventvalue=None):
        self._type = eventtype
        self._value = eventvalue

    def type(self):
        """return the type of this event
        """
        return self._type

    def value(self):
        """return the value of this event
        """
        return self.value
