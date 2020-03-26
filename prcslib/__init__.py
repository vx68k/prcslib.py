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

"""Python API for PRCS

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
    re.compile(br"^([^ ]+) ([^ ]+) (.+) by ([^ ]+) ?(\*DELETED\*)?")

class PrcsError(Exception):
    """base exception class for the prcslib package
    """

class PrcsCommandError(PrcsError):
    """Error from the PRCS command."""

    def __init__(self, error_message):
        """Construct a command error with an error message from PRCS."""
        super(PrcsCommandError, self).__init__(self)
        self.error_message = error_message

class PrcsVersion:
    """
    version identifier on PRCS
    """

    def __init__(self, major, minor=None):
        """
        construct a version identifier
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
        return self._major + "." + str(self._minor)

    def major(self):
        """
        major part of the version identifier
        """
        return self._major

    def minor(self):
        """
        minor part of the version identifier
        """
        return self._minor

class PrcsProject:
    """project on PRCS
    """

    def __init__(self, name):
        """construct a Project object."""
        self._command = "prcs"
        self.name = name

    def versions(self):
        """return a dictionary of the summary records for all the versions
        """
        out, err, status = self._run_prcs(["info", "-f", self.name])

        versions = {}
        if not err:
            # We use iteration over lines so that we can detect parse errors.
            for line in out.splitlines():
                match = _INFO_RECORD_PATTERN.match(line)
                if match:
                    # Note: the 'prcs info' command returns local times.
                    project, version, date, author, deleted = match.groups()
                    versions[version.decode()] = {
                        "project": project.decode(),
                        "id": version.decode(),
                        "date": datetime(*parsedate(date.decode())[0:6]),
                        "author": author.decode(),
                        "deleted": bool(deleted),
                    }
        else:
            raise PrcsCommandError(err)
        return versions

    def descriptor(self, version=None):
        """
        return the project descriptor for a version
        """
        return PrcsDescriptor(self, version)

    def checkout(self, version=None, files=None):
        """
        check out a version
        """
        if files is None:
            files = []
        args = ["checkout", "-fqu"]
        if version is not None:
            args.extend(["-r", str(version)])
        args.append(self.name)
        args.extend(files)
        __, err, status = self._run_prcs(args)
        if err:
            sys.stderr.write(err)

    def _run_prcs(self, args=None, stdin=None):
        """
        run a PRCS command as a subprocess
        """
        if args is None:
            args = []
        prcs = Popen(
            [self._command] + args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = prcs.communicate(stdin)
        return out, err, prcs.returncode

class PrcsDescriptor:
    """project descriptor on PRCS
    """

    def __init__(self, project, version=None):
        prj_name = project.name + ".prj"
        project.checkout(version, [prj_name])
        self.properties = _readdescriptor(prj_name)
        os.unlink(prj_name)

    def version(self):
        """Return the version in this descriptor."""
        v = self.properties["Project-Version"]
        return PrcsVersion(v[1].value(), v[2].value())

    def parentversion(self):
        """Return the major and minor parent versions."""
        v = self.properties["Parent-Version"]
        major = v[1].value()
        minor = v[2].value()
        if v[0].value() == "-*-" and major == "-*-" and minor == "-*-":
            return None
        return PrcsVersion(major, minor)

    def mergeparents(self):
        """Return the list of merge parents."""
        p = []
        for i in self.properties["Merge-Parents"]:
            if i[1].value() == "complete":
                p.append(i[0].value())
        return p

    def message(self):
        """Return the log message."""
        return self.properties["Version-Log"][0]

    def files(self):
        """Return the file information as a dictionary."""
        files = {}
        for i in self.properties["Files"]:
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

def _readdescriptor(name):
    with open(name, "r") as f:
        string = f.read()

    descriptor = {}
    # Encloses the project descriptor in a single list.
    for i in sexpdata.loads("(\n" + string + "\n)"):
        if isinstance(i, list) and isinstance(i[0], sexpdata.Symbol):
            descriptor[i[0].value()] = i[1:]
    return descriptor
