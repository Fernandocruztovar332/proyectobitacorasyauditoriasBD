import auditorias as sc
#import auditoria_admin as adm
import menuprincipal as mp

import tkinter as tk
from tkinter import messagebox
import pyodbc
def cargarlogin():
    # Función para conectarse a SQL Server
    def conectar_sql(usuario, contrasena, base_datos):
        try:
            servidor = 'localhost\\SQLEXPRESS'  # Cambia si tu servidor tiene otro nombre
            conexion = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={servidor};"
                f"DATABASE={base_datos};"
                f"UID={usuario};"
                f"PWD={contrasena}",
                autocommit=True
            )
            return conexion
        except pyodbc.Error:
            return None

    # Función para manejar login
    def login():
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()
        base_datos = "ESCOOL"  # Todos trabajan en la misma base en este caso

        conexion = conectar_sql(usuario, contrasena, base_datos)

        if usuario == "usuario_admin":
            if conexion:
                messagebox.showinfo("Inicio de sesión", f"Bienvenido, {usuario}")
                ventana.destroy()
                mp.cargarmenu_adm(conexion)
            else:
                messagebox.showerror("Error", "Credenciales incorrectas o conexión fallida.")
        elif usuario == "usuario_normal":
            if conexion:
                messagebox.showinfo("Inicio de sesión", f"Bienvenido, {usuario}")
                ventana.destroy()
                sc.iniciar_school(conexion)
            else:
                messagebox.showerror("Error", "Credenciales incorrectas o conexión fallida.")
        else:
            messagebox.showerror("Error", "Usuario no autorizado.")

    # Crear ventana de login
    ventana = tk.Tk()
    ventana.title("Login Proyecto Auditorías")
    ventana.geometry("300x200")

    tk.Label(ventana, text="Usuario:").pack(pady=5)
    entry_usuario = tk.Entry(ventana)
    entry_usuario.pack(pady=5)

    tk.Label(ventana, text="Contraseña:").pack(pady=5)
    entry_contrasena = tk.Entry(ventana, show="*")
    entry_contrasena.pack(pady=5)

    tk.Button(ventana, text="Iniciar sesión", command=login).pack(pady=20)

    ventana.mainloop()

if __name__ == "__main__":
    cargarlogin()