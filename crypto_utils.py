#Funciones responsables de convertir la contraseña maestra en una llave de
#cifrado, y de cifrar/descifrar el contenido de la bóveda.


import os
import json
import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

SALT_SIZE = 16
KDF_ITERATIONS = 390_000  


def generate_salt() -> bytes:
    #Genera una sal aleatoria criptográficamente segura.
    return os.urandom(SALT_SIZE)


def derive_key(master_password: str, salt: bytes) -> bytes:
    #Deriva una llave Fernet (32 bytes, base64) a partir de la contraseña
    #maestra y la sal almacenada
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,
    )
    raw_key = kdf.derive(master_password.encode("utf-8"))
    return base64.urlsafe_b64encode(raw_key)


def encrypt_data(data: dict, key: bytes) -> bytes:
    #Serializa un diccionario a JSON y lo cifra con Fernet.
    fernet = Fernet(key)
    plaintext = json.dumps(data).encode("utf-8")
    return fernet.encrypt(plaintext)


def decrypt_data(token: bytes, key: bytes) -> dict:
    #Descifra un token Fernet y lo convierte de vuelta a diccionario.

    #Lanza `cryptography.fernet.InvalidToken` si la llave (es decir, la
    #contraseña maestra) es incorrecta o si el archivo fue alterado.
    fernet = Fernet(key)
    plaintext = fernet.decrypt(token)
    return json.loads(plaintext.decode("utf-8"))
