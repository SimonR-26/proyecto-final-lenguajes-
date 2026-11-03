"""Operaciones de la boveda. Aqui no se construyen ventanas."""

import secrets
import string


def validar_registro(sitio, usuario, contraseña):
    """Comprueba los campos obligatorios de un registro."""
    if sitio.strip() == "":
        return False, "El sitio es obligatorio."
    if contraseña == "":
        return False, "La contraseña es obligatoria."
    return True, ""


def crear_registro(sitio, usuario, contraseña, notas):
    """Crea y devuelve un registro como diccionario."""
    registro = {
        "id": secrets.token_hex(8),
        "site": sitio.strip(),
        "username": usuario.strip(),
        "password": contraseña,
        "notes": notas.strip()
    }
    return registro


def agregar_registro(registros, registro):
    registros.append(registro)


def buscar_registros(registros, texto):
    """Devuelve los registros cuyo sitio o usuario coincide con la busqueda."""
    encontrados = []
    texto = texto.lower().strip()

    for registro in registros:
        sitio = registro["site"].lower()
        usuario = registro["username"].lower()

        if texto in sitio or texto in usuario:
            encontrados.append(registro)

    return encontrados


def buscar_por_id(registros, identificador):
    for registro in registros:
        if registro["id"] == identificador:
            return registro
    return None


def actualizar_registro(registros, identificador, sitio, usuario, contraseña, notas):
    registro = buscar_por_id(registros, identificador)

    if registro is None:
        return False

    registro["site"] = sitio.strip()
    registro["username"] = usuario.strip()
    registro["password"] = contraseña
    registro["notes"] = notas.strip()
    return True


def eliminar_registro(registros, identificador):
    registro = buscar_por_id(registros, identificador)

    if registro is None:
        return False

    registros.remove(registro)
    return True


def generar_contraseña(longitud, usar_simbolos):
    """Genera una contraseña aleatoria usando el modulo secrets."""
    letras_numeros = string.ascii_letters + string.digits
    simbolos = "!@#$%^&*()-_=+"

    caracteres = letras_numeros
    if usar_simbolos:
        caracteres = caracteres + simbolos

    contraseña = ""
    contador = 0

    while contador < longitud:
        contraseña = contraseña + secrets.choice(caracteres)
        contador = contador + 1

    return contraseña


def calcular_estadisticas(registros):
    """Calcula indicadores sin mostrar las contraseñas guardadas."""
    total_registros = len(registros)
    sitios = []
    registros_con_usuario = 0
    registros_con_notas = 0

    for registro in registros:
        sitio = registro["site"]
        if sitio not in sitios:
            sitios.append(sitio)

        if registro["username"] != "":
            registros_con_usuario = registros_con_usuario + 1

        if registro["notes"] != "":
            registros_con_notas = registros_con_notas + 1

    total_sitios = len(sitios)
    return {
        "total_registros": total_registros,
        "total_sitios": total_sitios,
        "con_usuario": registros_con_usuario,
        "con_notas": registros_con_notas
    }


def contar_registros_por_sitio(registros):
    """Cuenta cuantos registros hay para cada sitio."""
    sitios = []
    cantidades = []

    for registro in registros:
        sitio = registro["site"]
        posicion = -1
        contador = 0

        while contador < len(sitios):
            if sitios[contador] == sitio:
                posicion = contador
            contador = contador + 1

        if posicion == -1:
            sitios.append(sitio)
            cantidades.append(1)
        else:
            cantidades[posicion] = cantidades[posicion] + 1

    return sitios, cantidades
