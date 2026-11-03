# Bóveda - Gestor de contraseñas

Aplicación de escritorio desarrollada en Python con Tkinter. Permite crear una bóveda protegida por una contraseña maestra, guardar credenciales cifradas, consultar, buscar, actualizar y eliminar registros, generar contraseñas y consultar estadísticas.

## Requisitos

- Python 3.10 o superior.
- Tkinter (incluido normalmente en Python para Windows).
- La librería adicional `cryptography`.

## Instalación en Windows

Abre PowerShell en esta carpeta y ejecuta:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Archivos principales

- `main.py`: construye la interfaz gráfica con Tkinter y conecta los botones con las funciones.
- `funciones.py`: contiene las operaciones de registros, búsqueda, validación, generación de contraseñas y estadísticas.
- `archivos.py`: crea, lee y guarda la bóveda cifrada.
- `crypto_utils.py`: deriva la llave desde la contraseña maestra y cifra/descifra los datos usando Fernet.
- `data/salt.bin`: sal aleatoria utilizada para derivar la llave.
- `data/vault.enc`: registros cifrados. No se debe borrar si se quieren conservar los datos.

## Seguridad y compatibilidad

Los registros se guardan en el mismo formato cifrado que utilizaba la versión web: un diccionario JSON con la clave `entries`, cifrado mediante las funciones de `crypto_utils.py`. Por eso, si se conserva `salt.bin` y `vault.enc` originales, la aplicación de escritorio puede intentar abrir esa bóveda con la misma contraseña maestra.

La contraseña maestra no se guarda. Si se pierde, no será posible recuperar el contenido cifrado. Mantén una copia de seguridad segura de `data/salt.bin` y `data/vault.enc`.
