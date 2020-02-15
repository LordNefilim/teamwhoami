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

# Por defecto es mejor que sea https

proto = 'https'

class Handler(SimpleHTTPRequestHandler):
    def handle(self):
        # Imitamos el snippet de HTTPServer pero evitando las excepciones

        self.close_connection = True

        try:
            self.handle_one_request()

            while not (self.close_connection):
                self.handle_one_request()

        except Exception as Except:
            log_system.stderr('Exception: {}'.format(Except))

    def send_code(self, code):
        # Con este código ahorramos mucho...

        self.send_response(code)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

    # Los siguiente métodos HTTP ya no estaran disponibles

    def do_GET(self):
        self.send_code(501)

    def do_HEAD(self):
        self.send_code(501)

    def do_OPTIONS(self):
        self.send_code(501)

    def do_DELETE(self):
        self.send_code(501)

    def do_PUT(self):
        self.send_code(501)

    # POST sí por que es parte de la API

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

        self.send_code(info['response'])

        self.wfile.write(dumps(info).encode())

    def log_error(self, *args):
        # No necesitamos este método

        return

    def log_message(self, *args):
        args = args[1:]

        method = args[0]
        status_code = args[1]

        log_system.stdout("{}: {}".format(method, status_code))

httpd = ThreadingHTTPServer((host_config.LHOST, host_config.LPORT),
                            Handler)
try:
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   keyfile=sec_config.key,
                                   certfile=sec_config.cert,
                                   server_side=True)

except Exception as Except:
    log_system.stderr('NO se usará la clave o el certificado debido a un posible error: {}'.format(Except))

    proto = 'http' # Indicamos al usuario que ya no se usará https

try:
    log_system.stdout('Escuchando en %s://%s:%d' % (proto,
                                                    host_config.LHOST,
                                                    host_config.LPORT))

    httpd.serve_forever()

except KeyboardInterrupt:
    log_system.stderr("CTRL-C...")

finally:
    httpd.shutdown()
