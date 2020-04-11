# test_project.py
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
unit tests for the 'PrcsProject' class
"""

from __future__ import absolute_import, unicode_literals
from unittest import TestCase
from prcslib import PrcsProject

# PRCS project name for tests.
PRCS_PROJECT_NAME = "testproject"

class ProjectTests(TestCase):
    """
    Test case class for 'PrcsProject'
    """

    def setUp(self):
        """
        Set up a test case
        """
        self._project = PrcsProject(PRCS_PROJECT_NAME)

    def test_versions(self):
        """
        Test the 'versions' function
        """
        versions = self._project.versions()
        self.assertTrue("0.1" in versions)
