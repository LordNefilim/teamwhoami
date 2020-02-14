#!/usr/bin/env python3

import sys

from time import strftime

def _fprintf(std, *args, **kwargs):
    # Se puede modificar el primer argumento para mostrar información antes
    # del mensaje. Cómo es la hora en este caso.

    print(strftime('[%H:%M:%S]:'), *args, **kwargs,
          file=sys.stderr)

def stderr(*args, **kwargs):
    _fprintf(sys.stderr, *args, **kwargs)

def stdout(*args, **kwargs):
    _fprintf(sys.stdout, *args, **kwargs)
