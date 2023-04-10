import sys
import os
from cryptography.fernet import Fernet


def generate_key(raw_key=None):
    """Genera una clave Fernet."""
    return Fernet.generate_key(raw_key)


def encrypt_file(path, key, verbose=False):
    """Cifra un archivo utilizando una clave Fernet.

    Args:
        path (str): Ruta del archivo a cifrar.
        key (bytes): Clave Fernet utilizada para cifrar el archivo.
        verbose (bool, optional): Si es True, imprime un mensaje de depuración en la salida estándar. 
            Por defecto es False.

    """
    if verbose:
        print('Encrypting: ', path)

    fernet = Fernet(key)

    with open(path, 'rb') as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    with open(path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


def decrypt_file(path, key, verbose=True):
    """Descifra un archivo utilizando una clave Fernet.

    Args:
        path (str): Ruta del archivo a descifrar.
        key (bytes): Clave Fernet utilizada para descifrar el archivo.
        verbose (bool, optional): Si es True, imprime un mensaje de depuración en la salida estándar. 
            Por defecto es True.

    """
    if verbose:
        print('Decrypting: ', path)

    fernet = Fernet(key)

    with open(path, 'rb') as enc_file:
        encrypted = enc_file.read()

    decrypted = fernet.decrypt(encrypted)

    with open(path, 'wb') as dec_file:
        dec_file.write(decrypted)


def encrypt_dir(dirpath, key, verbose=False):
    """Cifra todos los archivos dentro de un directorio utilizando una clave Fernet.

    Args:
        dirpath (str): Ruta del directorio a cifrar.
        key (bytes): Clave Fernet utilizada para cifrar los archivos.
        verbose (bool, optional): Si es True, imprime un mensaje de depuración en la salida estándar. 
            Por defecto es False.

    Returns:
        dict: Diccionario que contiene las rutas de los archivos cifrados y los archivos ignorados.

    """
    encrypted = []
    skipped = []

    for filename in os.listdir(dirpath):
        path = os.path.join(dirpath, filename)

        if os.path.isdir(path):
            encrypt_dir(path, key, verbose)
        elif os.path.isfile(path):
            encrypt_file(path, key, verbose)
            encrypted.append(path)
        else:
            if verbose:
                print('Skipped: ', path)
            skipped.append(path)

    return {
        'encrypted': encrypted,
        'skipped': skipped
    }


def decrypt_dir(dirpath, key, verbose=False):
    """Decifra todos los archivos dentro de un directorio utilizando una clave Fernet.

    Args:
        dirpath (str): Ruta del directorio a cifrar.
        key (bytes): Clave Fernet utilizada para cifrar los archivos.
        verbose (bool, optional): Si es True, imprime un mensaje de depuración en la salida estándar. 
            Por defecto es False.

    Returns:
        dict: Diccionario que contiene las rutas de los archivos decifrados y los archivos ignorados.

    """
    decrypted = []
    skipped = []

    for filename in os.listdir(dirpath):
        path = os.path.join(dirpath, filename)

        if os.path.isdir(path):
            decrypt_dir(path, key, verbose)
        elif os.path.isfile(path):
            decrypt_file(path, key, verbose)
            decrypted.append(path)
        else:
            if verbose:
                print('Skipped: ', path)
            skipped.append(path)

    return {
        'decrypted': decrypted,
        'skipped': skipped
    }


def main(*args, **kwargs):
    if not args or '--help' in args[0]:
        print('[mode] [key] [path]')
        print('mode is "encrypt" or "decrypt"')
        print('Encrypt a file: encrypt MySecretKey1 directory/myfile.csv')
        print('Encrypt a directory: encrypt MySecretKey1 directory')
        print('Encrypt a directory with auto-generated key: encrypt --generate_key directory')
        print('Decrypt a file: decrypt MySecretKey1 directory/myfile.csv')
        return

    try:
        key = generate_key(args[0][2]) if not '--no-generate-key' in args[0] else args[0][2]
    except IndexError:
        print('Error: Please provide a key')
        return

    verbose = '--verbose' in args[0]
    mode = args[0][1] # encrypt or decrypt

    if mode not in ['encrypt', 'decrypt']:
        print('Error: Invalid mode')
        return

    funcs = {
        'encrypt': [encrypt_dir, encrypt_file],
        'decrypt': [decrypt_dir, decrypt_file]
    }

    try:
        fileOrDir = args[0][3]
    except IndexError:
        print('Error: Please provide a path')
        return

    path = os.path.abspath(fileOrDir)

    if not os.path.exists(path):
        print('Error: Path does not exist')
        return

    if os.path.isdir(path):
        out = funcs[mode][0](path, key, verbose)
    elif os.path.isfile(path):
        funcs[mode][1](path, key, verbose)
    else:
        print('Error: Path is not a file or directory')
        return


if __name__ == '__main__':
    main(sys.argv)
