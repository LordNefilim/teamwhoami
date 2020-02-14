#!/usr/bin/env python3

# Los algoritmos válidos

algo_available = ['RSA', 'DSA', 'ELG-E']

# El máximo de la longitud del par de claves.
#
# ¡Evita una posible sobrecarga en el servidor!

key_length = 4096

# Al igual qué la longitud de las claves para el firmado.

sign_key_length = key_length # No necesariamente tienen por qué ser iguales
