# prcslib - Python API for PRCS
# Copyright (C) 2012-2020 Kaz Nishimura
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
Python API for PRCS

This package provides an API for PRCS.
PRCS (Project Revision Control System) is a legacy version control system
which works on a set of files at once.
"""

from __future__ import absolute_import, unicode_literals
import sys
import re
import os
from datetime import datetime
from email.utils import parsedate
from subprocess import Popen, PIPE
from . import sexpdata

# Regular expression pattern for splitting versions.
_VERSION_PATTERN = re.compile(r"^(.*)\.(\d+)$")

# Matching pattern for info records.
_INFO_RECORD_PATTERN = \
    re.compile(r"^([^ ]+) ([^ ]+) (.+) by ([^ ]+) ?(\*DELETED\*)?")

class PrcsError(Exception):
    """
    Base exception class for the prcslib package.
    """

class PrcsCommandError(PrcsError):
    """
    Error from the PRCS command.
    """

    def __init__(self, error_message):
        """
        Construct a command error with an error message from PRCS.
        """
        super(PrcsCommandError, self).__init__(self)
        self.error_message = error_message

class PrcsVersion:
    """
    Version identifier on PRCS.

    A version identifier on PRCS is composed of major and minor parts separated
    by a full stop (U+002E). The former is a string, and the latter is a
    positive integral number.
    """

    def __init__(self, major, minor=None):
        """
        Construct a version identifier.
        """
        if isinstance(major, PrcsVersion):
            if minor is None:
                minor = major.minor()
            major = major.major()
        elif minor is None:
            match = _VERSION_PATTERN.match(major)
            major, minor = match.groups()

        self._major = str(major)
        self._minor = int(minor)

    def __str__(self):
        """
        Return the version identifier as a 'str' value.
        """
        return self._major + "." + str(self._minor)

    def __eq__(self, other):
        """
        Return 'true' if 'str(self)' == 'other'.
        """
        return str(self) == other

    def __ne__(self, other):
        """
        Return 'false' if 'self' == 'other'.
        """
        equal = self.__eq__(other)
        return not equal if not (equal is NotImplemented) else NotImplemented

    def __hash__(self):
        """
        Return 'hash(str(self))'.
        """
        return hash(str(self))

    def major(self):
        """
        Return the major part of the version identifier as a 'str' value.
        """
        return self._major

    def minor(self):
        """
        Return the minor part of the version identifier as an 'int' value.
        """
        return self._minor

class PrcsVersionDescriptor:
    """
    Version descriptor on PRCS.
    """

    @staticmethod
    def _readdescriptor(name):
        with open(name, "r") as stream:
            content = stream.read()

        # Encloses the project descriptor in a single list.
        data = sexpdata.loads("(\n" + content + "\n)")
        properties = {
            (i[0].value(), i[1:]) for i in data
            if isinstance(i, list) and isinstance(i[0], sexpdata.Symbol)
        }
        return properties

    def __init__(self, name):
        self._properties = self._readdescriptor(name)

    def version(self):
        """
        Return the version of the desciptor as a 'PrcsVersion' value.
        """
        version = self._properties["Project-Version"]
        major = version[1].value()
        minor = version[2].value()
        return PrcsVersion(major, minor)

    def parentversion(self):
        """
        Return 'self.parent()'.
        """
        return self.parent()

    def parent(self):
        """
        Return the parent of the descriptor as a 'PrcsVersion' value.
        """
        version = self._properties["Parent-Version"]
        major = version[1].value()
        minor = version[2].value()
        if major == "-*-" and minor == "-*-":
            return None
        return PrcsVersion(major, minor)

    def mergeparents(self):
        """
        Return a 'list' value for the merge parents.
        """
        parents = []
        for i in self._properties["Merge-Parents"]:
            if i[1].value() == "complete":
                parents.append(i[0].value())
        return parents

    def message(self):
        """
        Return the log message.
        """
        return self._properties["Version-Log"][0]

    def files(self):
        """
        Return the file information as a dictionary.
        """
        files = {}
        for i in self._properties["Files"]:
            name = i[0].value()
            symlink = False
            for j in i[2:]:
                if j.value() == ":symlink":
                    symlink = True
            if symlink:
                files[name] = {
                    "symlink": i[1][0].value(),
                }
            else:
                files[name] = {
                    "id": i[1][0].value(),
                    "revision": i[1][1].value(),
                    "mode": int(i[1][2].value(), 8),
                }
        return files

class PrcsProject:
    """
    Project on PRCS.
    """

    def __init__(self, name):
        """
        Construct a Project object.
        """
        self._command = "prcs"
        self._name = name

    def versions(self):
        """
        Return a dictionary of the summary records for all the versions.
        """
        out, err, status = self._run_prcs(["info", "-f", self._name])
        if status != 0:
            raise PrcsCommandError(err.decode())

        versions = {}
        # We use iteration over lines so that we can detect parse errors.
        for line in out.splitlines():
            match = _INFO_RECORD_PATTERN.match(line.decode())
            if match:
                # Note: the 'prcs info' command returns local times.
                project, version, date, author, deleted = match.groups()
                versions[version] = {
                    "project": project,
                    "id": version,
                    "date": datetime(*parsedate(date)[0:6]),
                    "author": author,
                    "deleted": bool(deleted),
                }
        return versions

    def descriptor(self, version=None):
        """
        Return the descriptor for a version.
        """
        name = self._name + ".prj"
        self.checkout(version, files=[name])
        try:
            descriptor = PrcsVersionDescriptor(name)
        finally:
            os.unlink(name)
        return descriptor

    def checkout(self, version=None, files=None):
        """
        Check out a version.
        """
        if files is None:
            files = []
        args = ["checkout", "-fqu"]
        if version is not None:
            args.extend(["-r", str(version)])
        args.append(self._name)
        args.extend(files)
        __, err, status = self._run_prcs(args)
        if status != 0:
            raise PrcsCommandError(err.decode())

    def _run_prcs(self, args=None, stdin=None):
        """
        Run a PRCS command as a subprocess.
        """
        if args is None:
            args = []
        prcs = Popen(
            [self._command] + args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = prcs.communicate(stdin)
        return out, err, prcs.returncode
