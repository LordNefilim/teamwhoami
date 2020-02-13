#!/usr/bin/env python3

import configparser

from Python.Utils.config import Config

def get_conf():
    parser = configparser.ConfigParser()
    parser.read(Config.file_config)

    return(parser)

# Es mejor crear funciones a parte para evitar la repetición de
# "parser.get(..., ...)".

def get_host_config(parsed):
    class Host_Configuration(object):
        LHOST = parsed.get('ADDRESSING', 'LHOST')
        LPORT = parsed.getint('ADDRESSING', 'LPORT')

    if (Host_Configuration.LPORT > 65535):
        raise OverflowError('El puerto no debe sobrepasar el número 65535')

    return(Host_Configuration)

def get_security_config(parsed):
    class Security_Configuration(object):
        key = parsed.get('SECURITY', 'key')
        cert = parsed.get('SECURITY', 'cert')

    return(Security_Configuration)
