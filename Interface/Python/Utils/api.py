#!/usr/bin/env python3

from urllib.parse import urlparse

from Python.Modules.Ciphers.EasyGnuPG import GnuPG

from Python.Utils.api_utils import api_config

def execute_action(params):
    info = {
        'response' : 200,
        'content' : None

    }

    gpg = GnuPG.GPG()
    
    if not (params):
        info['response'] = 400

    cmd = params.get('cmd')

    if not (isinstance(cmd, str)):
        info['response'] = 400

    else:
        cmd = cmd.strip()

    if (cmd == 'list_keys'):
        user = params.get('id')
        keys = GnuPG.list_keys(gpg, bool(params.get('secret'))) # En caso que no esté definido el parámetro GET «secret» se detectará
                                                                # cómo «False».

        if (str(user).lower() == 'all'):
            info['content'] = keys

        else:
            for _ in keys:
                # Tanto la dirección de correo electrónico cómo el «fingerprint» están permitidos

                if (''.join(_['uids']).split(maxsplit=1)[0] == user) or (_['fingerprint'] == str(user).strip()):
                    info['content'] = _

                    break

    elif (cmd == 'gen_key'):
        credentials = {
            'name_email' : None,
            'name_real' : None,
            'passphrase' : None,
            'name_comment' : '',
            'key_type' : 'RSA',
            'key_length' : 2048,
            'subkey_type' : 'DSA',
            'subkey_length' : 1024,
            'expire_date' : '365d'

        }

        # Verificamos que los parámetros requeridos estén definidos 

        for _ in ['name_email', 'name_real', 'passphrase']:
            if not (isinstance(params.get(_), str)):
                info['response'] = 400

                return(info)

            else:
                credentials[_] = params.get(_)

        # Verificamos los opcionales

        # La sintaxis de cada uno es:
        # >>> [('<Nombre>', <Tipo de valor>), ...]

        for _ in [('name_comment', str),
                  ('key_type', str),
                  ('key_length', int),
                  ('subkey_type', str),
                  ('subkey_length', int),
                  ('expire_date', str)]:
            if (params.get(_[0]) != None): # Cómo son opcionales, en caso de no ser definidos, dan igual
                try:
                    params[_[0]] = _[1](_[0]) # Convertimos el dato a un tipo de dato correspondiente

                except Exception as Except:
                    #print("Except:", str(Except))
                    info['response'] = 406

                    return(info)

                else:
                    credentials[_[0]] = params.get(_[0]) # Ajustamos el nuevo valor

        # Verificamos que los tipos de claves sean correctos

        for _ in ['key_type', 'subkey_type']:
            if (params.get(_) != None):
                if not (params.get(_) in api_config.algo_available):
                    info['response'] = 404
                    
                    return(info)

        # Verificamos que la longitud de las claves no se sobrepase, evitando
        # una sobrecarga en el servidor

        if (params.get('key_length') != None):
            if (params.get('key_length') > api_config.key_limit):
                info['response'] = 413

                return(info)

        if (params.get('subkey_length') != None):
            if (params.get('subkey_length') > api_config.sign_limit):
                info['response'] = 413

                return(info)
        
        gen = GnuPG.gen_key(gpg, **credentials)

        result = {
            'stderr' : gen.stderr,
            'fingerprint' : gen.fingerprint

        }

        info['content'] = result

    elif (cmd == 'encrypt'):
        # Me fatal incluir algunos parámetros, cómo "output" y "armor", pero
        # los dejaré cómo estén por defecto para evitar problemas.

        data = {
                'data' : params.get('data'),
                'recipients' : params.get('id'),
                'passphrase' : params.get('passphrase'),
                'sign' : bool(params.get('sign')),
                'always_trust' : bool(params.get('always_trust')),
                'symmetric' : bool(params.get('symmetric')),
                'armor' : True,
                'output' : None

        }

        if not (isinstance(data.get('data'), str)) \
        or not (isinstance(data.get('id'), str)) \
        or not (isinstance(data.get('passphrase'), str)):
            info['response'] = 400

            return(info)

        result = GnuPG.encrypt(gpg, **data)

        info['content'] = {
            'data' : result.data,
            'ok' : result.ok,
            'status' : result.status,
            'stderr' : result.stderr

        }

    else:
        info['response'] = 404

    return(info)
