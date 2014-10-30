#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 Lorenz Quack
# 
# This software is provided 'as-is', without any express or implied warranty.
# In no event will the authors be held liable for any damages arising from the
# use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
#    1. The origin of this software must not be misrepresented; you must not
#       claim that you wrote the original software. If you use this software
#       in a product, an acknowledgment in the product documentation would be
#       appreciated but is not required.
#
#    2. Altered source versions must be plainly marked as such, and must not
#       be misrepresented as being the original software.
#
#    3. This notice may not be removed or altered from any source distribution.


try:
    import builtins
except ImportError:
    import __builtin__ as builtins
import sys
import importlib
import base64
import zlib
import io
import argparse
import re
import tokenize
import keyword
import os
from datetime import datetime

__all__ = ["ResourceFile"]
version = "1.0"

_resourceTemplate = '''# generated by data2py. Do not edit!
"""Resource file (v{{version}}) generated by data2py on the {{datetime}}
This module provides access to data files that have been embedded in the module.
`keys()` returns a list of the embedded resources.
`get(resourcePath)` returns the raw content of the resource, i.e. binary mode.
`open(resourcePath, mode="r")` returns a file-like object to the resource.

List of embedded resources:
{{resourceList}}
"""

version = "{version}"
generation_date = "{datetime}"

def get(resourcePath):
    """returns the raw/binary content of the resource."""
    import base64
    import zlib
    encodedData, storedCRC, modTime = _encodedData[resourcePath]
    data = base64.b64decode(encodedData)
    crc = zlib.crc32(data) & 0xffffffff
    if crc != storedCRC:
        raise RuntimeError("data is corrupted")
    return data

def open(resourcePath, mode="r", encoding=None):
    """returns a file-like object to the resource."""
    import io
    data = get(resourcePath)
    if mode == "r":
        if not encoding:
            import locale
            encoding = locale.getpreferredencoding(False)
        return io.StringIO(data.decode(encoding))
    elif mode == "rb":
        return io.BytesIO(data)
    else:
        raise RuntimeError('Unsupported mode "%s". Should be "r" or "rb"' % mode)

def keys():
    """returns a list of all available resources in this file."""
    return list(_encodedData.keys())


_encodedData = {data}

__doc__ = __doc__.format(version=version, datetime=generation_date,
                         resourceList="  " + "\\n  ".join(keys()))

'''

class ResourceFile(object):
    def __init__(self):
        self._resources = {}
        
    def _assertResourceDir(self, resourceDir):
        if not resourceDir.startswith("/"):
            raise RuntimeError('resourceDir should be an absolute path not "%s"' % resourceDir)

    def add_resource(self, path, resourceDir="/"):
        self._assertResourceDir(resourceDir)
        if os.path.isfile(path):
            self._add_file(path, resourceDir)
        elif os.path.isdir(path):
            self._add_directory(path, resourceDir)

    def _add_file(self, path, resourceDir):
        with builtins.open(path, "rb") as inFile:
            data = inFile.read()
            crc = zlib.crc32(data) & 0xffffffff
            encodedData = base64.b64encode(data)
            filename = os.path.basename(path)
            resourcePath = os.path.join(resourceDir, filename)
            self._resources[resourcePath] = (encodedData, crc,
                                             datetime.utcnow().isoformat())

    def _add_directory(self, path, baseResourceDir):
        for root, dirs, files in os.walk(path):
            relpath = os.path.relpath(root, path)
            resourceDir = os.path.join(baseResourceDir, relpath)
            for f in files:
                self.add_file(os.path.join(root, f), resourceDir)
            for d in dirs:
                self.add_directory(os.path.join(root, d), resourceDir)

    def list(self):
        return self.resources.keys()

    def save(self, path):
        content = _resourceTemplate.format(datetime=datetime.utcnow().isoformat(),
                                           version=version, 
                                           data=self._resources)
        if not path:
            sys.stdout.write(content)
        else:
            with builtins.open(path, "w") as f:
                f.write(content)

    def _load_v1(self, module):
        self._resources = module._encodedData        
        
    def load(self, path):
        dirname, filename = os.path.split(path)
        sys.path.insert(0, dirname)
        module = importlib.import_module(path)
        sys.path = sys.path[1:]
        if module.version == "1.0":
            self._load_v1(module)
        else:
            raise RuntimeError("Unsupported resource version %s" % module.version)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert a data file to a python resource module")
    parser.add_argument('--version', action='version', version=version)
    parser.add_argument('-o', '--output', action='store', dest="outFile", metavar="foo", help="path to where the resource file should be written to.")
    parser.add_argument('PATH', nargs="+", action='store', help="path to resource that should be embedded into the python resource file.")
    args = parser.parse_args()
    resourceFile = ResourceFile()
    for path in args.PATH:
        resourceFile.add_resource(path)
    resourceFile.save(args.outFile)
    

