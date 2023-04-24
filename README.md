# Cifrado de archivos y directorios
Este script es capaz de cifrar y descifrar archivos y directorios utilizando una clave Fernet.

## Instalación
El script requiere que se tenga instalado Python 3 y el paquete cryptography. Se puede instalar cryptography ejecutando el siguiente comando en la terminal:

```py
pip install cryptography
```

## Modos de uso:

```sh
encrypt MySecretKey1 directory/myfile.csv # cifra un archivo.
```

```sh
encrypt MySecretKey1 directory # cifra un directorio.
```

```sh
encrypt --generate_key directory # cifra un directorio con una clave generada automáticamente.
```

```sh
decrypt MySecretKey1 directory/myfile.csv # descifra un archivo.
```
