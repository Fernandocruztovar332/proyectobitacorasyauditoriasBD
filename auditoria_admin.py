#auditoria_admin.py
import tkinter as tk
from tkinter import ttk
import pyodbc
import menuprincipal as mp

def abrir_ventana_admin(conexion):
    root = tk.Tk()
    root.title("Panel de Auditoría - Admin")
    root.geometry("1200x600")
    root.configure(bg="#1F618D")

    def regresar():
        root.destroy()
        mp.cargarmenu_adm(conexion)

    # Listbox para mostrar auditorías
    cuadro_fecha = tk.Listbox(root)
    cuadro_fecha.place(x=50, y=100, width=200, height=400)

    cuadro_tabla = tk.Listbox(root)
    cuadro_tabla.place(x=250, y=100, width=200, height=400)

    cuadro_accion = tk.Listbox(root)
    cuadro_accion.place(x=450, y=100, width=200, height=400)

    cuadro_usuario = tk.Listbox(root)
    cuadro_usuario.place(x=650, y=100, width=200, height=400)

    cuadro_detalle = tk.Listbox(root)
    cuadro_detalle.place(x=850, y=100, width=300, height=400)

    tk.Label(root, text="Fecha", bg="light blue").place(x=50, y=70, width=200)
    tk.Label(root, text="Tabla", bg="light blue").place(x=250, y=70, width=200)
    tk.Label(root, text="Acción", bg="light blue").place(x=450, y=70, width=200)
    tk.Label(root, text="Usuario", bg="light blue").place(x=650, y=70, width=200)
    tk.Label(root, text="Detalle", bg="light blue").place(x=850, y=70, width=300)

    # Función para cargar auditoría
    def cargar_auditoria():
        try:
            cursor = conexion.cursor()
            cursor.execute("EXEC sp_ConsultarAuditoriaGeneral")
            resultados = cursor.fetchall()

            cuadro_fecha.delete(0, tk.END)
            cuadro_tabla.delete(0, tk.END)
            cuadro_accion.delete(0, tk.END)
            cuadro_usuario.delete(0, tk.END)
            cuadro_detalle.delete(0, tk.END)

            for fila in resultados:
                cuadro_fecha.insert(tk.END, fila[0])
                cuadro_tabla.insert(tk.END, fila[1])
                cuadro_accion.insert(tk.END, fila[2])
                cuadro_usuario.insert(tk.END, fila[3])
                cuadro_detalle.insert(tk.END, fila[4])

        except Exception as e:
            print(f"Error al cargar auditoría: {str(e)}")

    # Botón para cargar auditoría
    tk.Button(root, text="Cargar Auditoría", command=cargar_auditoria, bg="light blue").place(x=500, y=20, width=200, height=40)
    tk.Button(root, text="<--", command=regresar, bg="light blue").place(x=20, y=20, width=200, height=40)

    root.mainloop()