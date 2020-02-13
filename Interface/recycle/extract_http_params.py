#!/usr/bin/env python3

def extract(params):
    info = {}

    params = params.strip()

    if (params == ''):
        return

    for _ in params.split('&'):
        keys = _.split('=')

        if (len(keys) == 1):
            (key, value) = (keys[0], None)

        else:
            (key, value) = keys

        info[key] = value

    return(info)
