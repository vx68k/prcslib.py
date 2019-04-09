#
# prcslib/__init__.py - command interface package for PRCS
# Copyright (C) 2012-2015 Kaz Nishimura
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

"""provide command line interface to PRCS
"""

import sys
import re
import os
from datetime import datetime
from email.utils import parsedate
from subprocess import Popen, PIPE
import prcslib.sexpdata as sexpdata

# Regular expression pattern for splitting versions.
_VERSION_RE = re.compile(r"^(.*)\.(\d+)$")

class PrcsError(Exception):
    """Base exception for this module."""
    pass

class PrcsCommandError(PrcsError):
    """Error from the PRCS command."""

    def __init__(self, error_message):
        """Construct a command error with an error message from PRCS."""
        super(PrcsCommandError, self).__init__(self)
        self.error_message = error_message

class PrcsVersion(object):
    """Version identifier of PRCS."""

    def __init__(self, major, minor=None):
        if minor is None:
            m = _VERSION_RE.match(major)
            major, minor = m.groups()

        self.major = major
        self.minor = int(minor)

    def __str__(self):
        return self.major + "." + str(self.minor)

class PrcsProject(object):

    def __init__(self, name):
        """construct a Project object."""
        self.name = name
        self.info_re = re.compile(
                "^([^ ]+) ([^ ]+) (.+) by ([^ ]+)( \*DELETED\*|)")

    def revisions(self):
        out, err = self._run_prcs(["info", "-f", self.name]);

        revisions = {}
        if (not err):
            # We use iteration over lines so that we can detect parse errors.
            for line in out.splitlines():
                m = self.info_re.search(line)
                if (m):
                    # The prcs info command always returns the local time.
                    date = parsedate(m.group(3))
                    revisions[m.group(2)] = {
                        "project": m.group(1),
                        "id": m.group(2),
                        "date": datetime(*date[0:6]),
                        "author": m.group(4),
                        "deleted": bool(m.group(5))
                    }
        else:
            raise PrcsCommandError(err)
        return revisions

    def descriptor(self, id = None):
        return PrcsDescriptor(self, id)

    def checkout(self, revision = None, files = []):
        args = ["checkout", "-fqu"]
        if not files:
            args.append("-P")
        if revision is not None:
            args.extend(["-r", revision])
        args.append(self.name)
        args.extend(files)
        out, err = self._run_prcs(args)
        if err:
            sys.stderr.write(err)

    def _run_prcs(self, args, input = None):
        """run a PRCS subprocess."""
        prcs = Popen(["prcs"] + args, stdin = PIPE, stdout = PIPE,
                stderr = PIPE)
        return prcs.communicate(input)

class PrcsDescriptor(object):

    def __init__(self, project, id = None):
        prj_name = project.name + ".prj"
        project.checkout(id, [prj_name])
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
