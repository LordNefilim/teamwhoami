#1/usr/bin/env python3
#
# Todo lo que sea vea aquí y en otros script's, modulos, utilidades,
# entre otros; podrá y será cambiado, ya que lo que se observa es una
# demostración.
#
# ~ DtxdF

import socket
import ssl
from json import dumps, loads
from http.server import (SimpleHTTPRequestHandler,
                        ThreadingHTTPServer)

# Modulos

from Python.Modules.UI import log_system

# Utilidades

from Python.Utils.Parsers import conf_parser

# Importante

from Python.Utils import (version,
                          api,
                          config)

# Información de los encabezados

SimpleHTTPRequestHandler.server_version = config.Config.app_name
SimpleHTTPRequestHandler.sys_version = version.get_version()

# Obtenemos la información parseada

parsed = conf_parser.get_conf()

# Obtenemos los valores para configurar el servidor

host_config = conf_parser.get_host_config(parsed)

# Obtenemos los valores para configurar https

sec_config = conf_parser.get_security_config(parsed)

class Handler(SimpleHTTPRequestHandler):
    def send_code(self, code):
        self.send_response(code)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = self.headers['Content-Length']

        if (content_length == None):
            self.send_code(411)
            
            return

        else:
            content_length = int(content_length)

        if (content_length <= 0):
            self.send_code(400)

            return

        post_data = self.rfile.read(content_length)

        if (len(post_data) <= 0):
            self.send_code(400)

            return

        info = api.execute_action(loads(post_data.decode()))

        self.send_code(200) # o info['response']

        self.wfile.write(dumps(info).encode())

httpd = ThreadingHTTPServer((host_config.LHOST, host_config.LPORT),
                            Handler)
httpd.socket = ssl.wrap_socket(httpd.socket,
                               keyfile=sec_config.key,
                               certfile=sec_config.cert,
                               server_side=True)

try:
    log_system.stdout('Escuchando en https://%s:%d' % (host_config.LHOST,
                                                       host_config.LPORT))

    httpd.serve_forever()

except KeyboardInterrupt:
    log_system.stderr("CTRL-C...")

finally:
    httpd.shutdown()
