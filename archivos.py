"""Funciones sencillas para guardar y recuperar la boveda cifrada."""

import os

from crypto_utils import generate_salt, derive_key, encrypt_data, decrypt_data

CARPETA_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
ARCHIVO_SAL = os.path.join(CARPETA_DATOS, "salt.bin")
ARCHIVO_BOVEDA = os.path.join(CARPETA_DATOS, "vault.enc")


def existe_boveda():
    """Comprueba si ya existe la sal y el archivo cifrado."""
    if os.path.exists(ARCHIVO_SAL) and os.path.exists(ARCHIVO_BOVEDA):
        return True
    return False


def crear_boveda(contraseña_maestra):
    """Crea la sal, obtiene la llave y guarda una boveda vacia."""
    os.makedirs(CARPETA_DATOS, exist_ok=True)
    sal = generate_salt()
    llave = derive_key(contraseña_maestra, sal)

    with open(ARCHIVO_SAL, "wb") as archivo:
        archivo.write(sal)

    guardar_datos({"entries": []}, llave)
    return llave


def cargar_datos(llave):
    """Lee el archivo cifrado y devuelve los registros."""
    with open(ARCHIVO_BOVEDA, "rb") as archivo:
        contenido_cifrado = archivo.read()

    datos = decrypt_data(contenido_cifrado, llave)
    return datos


def guardar_datos(datos, llave):
    """Cifra los registros y los guarda en el disco."""
    os.makedirs(CARPETA_DATOS, exist_ok=True)
    contenido_cifrado = encrypt_data(datos, llave)

    with open(ARCHIVO_BOVEDA, "wb") as archivo:
        archivo.write(contenido_cifrado)


def obtener_llave(contraseña_maestra):
    """Obtiene la llave usando la contraseña maestra y la sal guardada."""
    with open(ARCHIVO_SAL, "rb") as archivo:
        sal = archivo.read()

    llave = derive_key(contraseña_maestra, sal)
    return llave
