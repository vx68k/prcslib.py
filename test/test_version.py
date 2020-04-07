# test_version.py
# Copyright (C) 2020 Kaz Nishimura
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
unit tests for the 'PrcsVersion' class
"""

from __future__ import absolute_import, unicode_literals
from unittest import TestCase
from prcslib import PrcsVersion

class VersionTests(TestCase):
    """
    Test case class for the 'PrcsVersion' class.
    """

    def setUp(self):
        """
        Set up the test fixture.
        """
        self._version1 = PrcsVersion("0.1")
        self._version2 = PrcsVersion("1.2", 3)

    def test_major(self):
        """
        Test the 'major' method.
        """
        self.assertEqual("0", self._version1.major())
        self.assertEqual("1.2", self._version2.major())

    def test_minor(self):
        """
        Test the 'minor' method.
        """
        self.assertEqual(1, self._version1.minor())
        self.assertEqual(3, self._version2.minor())

    def test_equality(self):
        """
        Test equality of versions.
        """
        self.assertEqual(self._version1, self._version1)
        self.assertNotEqual(self._version2, self._version1)
        self.assertEqual(self._version1, PrcsVersion(self._version1))

    def test_hash(self):
        """
        Test hash values of versions.
        """
        self.assertEqual(hash(self._version1), hash(self._version1))
        self.assertNotEqual(hash(self._version2), hash(self._version1))
        self.assertEqual(hash("0.1"), hash(self._version1))
