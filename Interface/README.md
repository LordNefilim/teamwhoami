## Interactuando por medio de la API

Mientras que en el caso de usar la interfaz web se necesita enviar una petición por el método **GET**, para interactuar con la API se usará el método **POST**. Es sencillo, tenemos a **«requests»** de nuestro lado, pero antes que nada lo debemos tenerlo instalado.

```bash
python3 -m pip install requests # o pip3 install requests
```

Realizada la instalación de libraría que nos ayudará, ahora pasemos a la generación de claves usando **openssl**.

```bash
# Generamos la clave y el certificado para obtener el «https»

openssl req -x509 -newkey rsa:<Tamaño en Bit's de la clave> -keyout <Nombre de la clave> -out <Nombre del certificado> -days <Fecha de expiración en días>

# Ahora en caso de que no deseemos que openssl nos pregunte la contraseña que le colocamos anteriormente, debemos quitarsela

openssl rsa -in <Nombre de la clave usada en la generación> -out <Nombre de la clave nueva> # Podemos colocar las mismas para sobreescribirlas
```

Una vez creado la clave y el certificado, pasemos con la utilización de la API

```python
import requests

from urllib3 import disable_warnings

disable_warnings() # Deshabiliamos las advertencias cuando sea una conexión con un certificado inválido.

# Crear el par de claves

result = requests.post('https://localhost:8044/',
						data=json.dumps({
								'cmd':'gen_key',
								'name_email':'DtxdF@email.org',
								'passphrase':'passphrase123@',
								'name_real':'Josef Naranjo'}),
						verify=False)

print(result) # También podemos usar el método **«.json( )»** para parsear la respuesta.

# Listar todas las claves que tengamos

result = requests.post('https://localhost:8044/',
						data=json.dumps({
								'cmd':'list_keys',
								'id':'all'}),
						verify=False)

print(result)

```

*(Por ahora eso es todo, pero se irán introduciendo más comandos)...*

\~ DtxdF
