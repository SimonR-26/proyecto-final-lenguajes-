"""Aplicacion de escritorio Boveda usando Tkinter."""

import tkinter as tk
from tkinter import ttk, messagebox

from cryptography.fernet import InvalidToken

import archivos
import funciones


class AplicacionBoveda:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Boveda - Gestor de contraseñas")
        self.ventana.geometry("900x620")
        self.ventana.minsize(760, 520)

        self.llave = None
        self.registros = []
        self.registro_seleccionado = None

        self.mostrar_pantalla_acceso()

    def limpiar_ventana(self):
        for elemento in self.ventana.winfo_children():
            elemento.destroy()

    def mostrar_pantalla_acceso(self):
        self.limpiar_ventana()

        marco = ttk.Frame(self.ventana, padding=30)
        marco.pack(expand=True)

        ttk.Label(marco, text="BÓVEDA", font=("Arial", 24, "bold")).pack(pady=10)

        if archivos.existe_boveda():
            mensaje = "Escribe tu contraseña maestra para desbloquear la bóveda."
            texto_boton = "Desbloquear"
        else:
            mensaje = "Crea una contraseña maestra de mínimo 8 caracteres."
            texto_boton = "Crear bóveda"

        ttk.Label(marco, text=mensaje).pack(pady=8)
        self.entrada_maestra = ttk.Entry(marco, width=35, show="*")
        self.entrada_maestra.pack(pady=8)
        ttk.Button(marco, text=texto_boton, command=self.acceder).pack(pady=10)

    def acceder(self):
        contraseña = self.entrada_maestra.get()

        if len(contraseña) < 8:
            messagebox.showwarning("Validación", "La contraseña maestra debe tener mínimo 8 caracteres.")
            return

        if archivos.existe_boveda():
            try:
                self.llave = archivos.obtener_llave(contraseña)
                datos = archivos.cargar_datos(self.llave)
                self.registros = datos["entries"]
            except InvalidToken:
                messagebox.showerror("Error", "La contraseña maestra es incorrecta.")
                return
            except (OSError, ValueError, KeyError) as error:
                messagebox.showerror("Error", "No se pudo abrir la bóveda: " + str(error))
                return
        else:
            try:
                self.llave = archivos.crear_boveda(contraseña)
                self.registros = []
            except OSError as error:
                messagebox.showerror("Error", "No se pudo crear la bóveda: " + str(error))
                return

        self.mostrar_pantalla_principal()

    def mostrar_pantalla_principal(self):
        self.limpiar_ventana()

        encabezado = ttk.Frame(self.ventana, padding=10)
        encabezado.pack(fill="x")
        ttk.Label(encabezado, text="BÓVEDA", font=("Arial", 20, "bold")).pack(side="left")
        ttk.Button(encabezado, text="Bloquear", command=self.bloquear).pack(side="right")

        busqueda = ttk.Frame(self.ventana, padding=10)
        busqueda.pack(fill="x")
        ttk.Label(busqueda, text="Buscar por sitio o usuario:").pack(side="left")
        self.entrada_busqueda = ttk.Entry(busqueda, width=35)
        self.entrada_busqueda.pack(side="left", padx=8)
        ttk.Button(busqueda, text="Buscar", command=self.buscar).pack(side="left")
        ttk.Button(busqueda, text="Mostrar todos", command=self.actualizar_tabla).pack(side="left", padx=5)

        columnas = ("sitio", "usuario")
        self.tabla = ttk.Treeview(self.ventana, columns=columnas, show="headings", height=15)
        self.tabla.heading("sitio", text="Sitio")
        self.tabla.heading("usuario", text="Usuario")
        self.tabla.column("sitio", width=350)
        self.tabla.column("usuario", width=350)
        self.tabla.pack(fill="both", expand=True, padx=12, pady=8)

        botones = ttk.Frame(self.ventana, padding=10)
        botones.pack(fill="x")
        ttk.Button(botones, text="Agregar", command=self.agregar).pack(side="left", padx=4)
        ttk.Button(botones, text="Consultar", command=self.consultar).pack(side="left", padx=4)
        ttk.Button(botones, text="Actualizar", command=self.actualizar).pack(side="left", padx=4)
        ttk.Button(botones, text="Eliminar", command=self.eliminar).pack(side="left", padx=4)
        ttk.Button(botones, text="Generar contraseña", command=self.abrir_generador).pack(side="left", padx=4)
        ttk.Button(botones, text="Estadísticas", command=self.mostrar_estadisticas).pack(side="right", padx=4)

        self.actualizar_tabla()

    def guardar_cambios(self):
        try:
            archivos.guardar_datos({"entries": self.registros}, self.llave)
            return True
        except OSError as error:
            messagebox.showerror("Error", "No se pudieron guardar los cambios: " + str(error))
            return False

    def actualizar_tabla(self, lista_registros=None):
        for elemento in self.tabla.get_children():
            self.tabla.delete(elemento)

        if lista_registros is None:
            lista_registros = self.registros

        for registro in lista_registros:
            self.tabla.insert("", "end", iid=registro["id"], values=(registro["site"], registro["username"]))

    def buscar(self):
        texto = self.entrada_busqueda.get()
        encontrados = funciones.buscar_registros(self.registros, texto)
        self.actualizar_tabla(encontrados)

        if len(encontrados) == 0:
            messagebox.showinfo("Búsqueda", "No se encontraron registros.")

    def obtener_seleccion(self):
        seleccion = self.tabla.selection()
        if len(seleccion) == 0:
            messagebox.showwarning("Selección", "Primero selecciona un registro.")
            return None
        return seleccion[0]

    def ventana_registro(self, titulo, registro=None):
        ventana = tk.Toplevel(self.ventana)
        ventana.title(titulo)
        ventana.geometry("420x360")
        ventana.transient(self.ventana)
        ventana.grab_set()

        marco = ttk.Frame(ventana, padding=15)
        marco.pack(fill="both", expand=True)

        etiquetas = ["Sitio:", "Usuario:", "Contraseña:", "Notas:"]
        entradas = []
        valores = ["", "", "", ""]

        if registro is not None:
            valores = [registro["site"], registro["username"], registro["password"], registro["notes"]]

        contador = 0
        while contador < len(etiquetas):
            ttk.Label(marco, text=etiquetas[contador]).pack(anchor="w", pady=(5, 0))
            entrada = ttk.Entry(marco, width=45)
            entrada.pack(fill="x", pady=3)
            entrada.insert(0, valores[contador])
            entradas.append(entrada)
            contador = contador + 1

        def guardar():
            sitio = entradas[0].get()
            usuario = entradas[1].get()
            contraseña = entradas[2].get()
            notas = entradas[3].get()

            valido, mensaje = funciones.validar_registro(sitio, usuario, contraseña)
            if valido == False:
                messagebox.showwarning("Validación", mensaje, parent=ventana)
                return

            if registro is None:
                nuevo = funciones.crear_registro(sitio, usuario, contraseña, notas)
                funciones.agregar_registro(self.registros, nuevo)
            else:
                funciones.actualizar_registro(self.registros, registro["id"], sitio, usuario, contraseña, notas)

            guardado = self.guardar_cambios()
            if guardado == True:
                self.actualizar_tabla()
                ventana.destroy()

        ttk.Button(marco, text="Guardar", command=guardar).pack(pady=15)

    def agregar(self):
        self.ventana_registro("Agregar contraseña")

    def consultar(self):
        identificador = self.obtener_seleccion()
        if identificador is None:
            return

        registro = funciones.buscar_por_id(self.registros, identificador)
        if registro is not None:
            mensaje = "Sitio: " + registro["site"]
            mensaje = mensaje + "\nUsuario: " + registro["username"]
            mensaje = mensaje + "\nContraseña: " + registro["password"]
            mensaje = mensaje + "\nNotas: " + registro["notes"]
            messagebox.showinfo("Datos del registro", mensaje)

    def actualizar(self):
        identificador = self.obtener_seleccion()
        if identificador is None:
            return

        registro = funciones.buscar_por_id(self.registros, identificador)
        if registro is not None:
            self.ventana_registro("Actualizar contraseña", registro)

    def eliminar(self):
        identificador = self.obtener_seleccion()
        if identificador is None:
            return

        respuesta = messagebox.askyesno("Confirmar", "¿Deseas eliminar este registro?")
        if respuesta == True:
            eliminado = funciones.eliminar_registro(self.registros, identificador)
            if eliminado == True:
                if self.guardar_cambios() == True:
                    self.actualizar_tabla()
                    messagebox.showinfo("Bóveda", "Registro eliminado.")

    def abrir_generador(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Generador de contraseñas")
        ventana.geometry("350x230")
        ventana.transient(self.ventana)
        ventana.grab_set()

        marco = ttk.Frame(ventana, padding=15)
        marco.pack(fill="both", expand=True)

        ttk.Label(marco, text="Longitud (8 a 64):").pack(anchor="w")
        entrada_longitud = ttk.Entry(marco)
        entrada_longitud.insert(0, "16")
        entrada_longitud.pack(fill="x", pady=5)

        usar_simbolos = tk.BooleanVar(value=True)
        ttk.Checkbutton(marco, text="Incluir símbolos", variable=usar_simbolos).pack(anchor="w", pady=5)

        entrada_resultado = ttk.Entry(marco, width=40)
        entrada_resultado.pack(fill="x", pady=8)

        def generar():
            try:
                longitud = int(entrada_longitud.get())
                if longitud < 8 or longitud > 64:
                    messagebox.showwarning("Validación", "La longitud debe estar entre 8 y 64.", parent=ventana)
                    return
                contraseña = funciones.generar_contraseña(longitud, usar_simbolos.get())
                entrada_resultado.delete(0, "end")
                entrada_resultado.insert(0, contraseña)
            except ValueError:
                messagebox.showerror("Error", "La longitud debe ser un número entero.", parent=ventana)

        ttk.Button(marco, text="Generar", command=generar).pack(pady=5)

    def mostrar_estadisticas(self):
        datos = funciones.calcular_estadisticas(self.registros)
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Estadísticas de la bóveda")
        ventana.geometry("500x430")

        marco = ttk.Frame(ventana, padding=15)
        marco.pack(fill="both", expand=True)

        ttk.Label(marco, text="Resumen de la bóveda", font=("Arial", 16, "bold")).pack(pady=8)
        ttk.Label(marco, text="Total de registros: " + str(datos["total_registros"])).pack(anchor="w", pady=3)
        ttk.Label(marco, text="Sitios diferentes: " + str(datos["total_sitios"])).pack(anchor="w", pady=3)
        ttk.Label(marco, text="Registros con usuario: " + str(datos["con_usuario"])).pack(anchor="w", pady=3)
        ttk.Label(marco, text="Registros con notas: " + str(datos["con_notas"])).pack(anchor="w", pady=3)

        sitios, cantidades = funciones.contar_registros_por_sitio(self.registros)
        lienzo = tk.Canvas(marco, width=440, height=210, background="white")
        lienzo.pack(pady=10)

        if len(sitios) == 0:
            lienzo.create_text(220, 100, text="Todavía no hay registros para graficar.")
        else:
            mayor = cantidades[0]
            contador_mayor = 1
            while contador_mayor < len(cantidades):
                if cantidades[contador_mayor] > mayor:
                    mayor = cantidades[contador_mayor]
                contador_mayor = contador_mayor + 1

            posicion_y = 20
            contador = 0
            while contador < len(sitios):
                ancho = int((cantidades[contador] / mayor) * 250)
                lienzo.create_text(75, posicion_y + 10, text=sitios[contador], anchor="e")
                lienzo.create_rectangle(85, posicion_y, 85 + ancho, posicion_y + 20, fill="#3976a8")
                lienzo.create_text(95 + ancho, posicion_y + 10, text=str(cantidades[contador]), anchor="w")
                posicion_y = posicion_y + 35
                contador = contador + 1
                if posicion_y > 190:
                    break

    def bloquear(self):
        self.llave = None
        self.registros = []
        self.mostrar_pantalla_acceso()


def iniciar_aplicacion():
    ventana = tk.Tk()
    aplicacion = AplicacionBoveda(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    iniciar_aplicacion()
