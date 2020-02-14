#!/usr/bin/env python3

from Python.Utils.config import Config

def get_version():
    with open(Config.file_version, 'rt') as _obj:
        return(_obj.read().strip())
