#historial.py
import tkinter as tk
from tkinter import messagebox
import menuprincipal as mp

def historial(con):
    root = tk.Tk()
    root.title("Panel Historial")
    root.geometry("1100x520")
    root.configure(bg="#1F618D")

    def regresar():
        root.destroy()
        mp.cargarmenu_adm(con)

    # Listboxes para mostrar los campos
    campos = {
        "No. Control": tk.Listbox(root),
        "Nombre": tk.Listbox(root),
        "Apellido P": tk.Listbox(root),
        "Apellido M": tk.Listbox(root),
        "Carrera": tk.Listbox(root),
        "Semestre": tk.Listbox(root),
        "Horas P": tk.Listbox(root),
        "Horas T": tk.Listbox(root),
        "Calif": tk.Listbox(root),
        "Oportunidad": tk.Listbox(root)
    }

    # Posiciones iniciales
    x_inicial = 10
    ancho = 100
    alto = 400
    espacio = 5

    # Crear etiquetas y listboxes dinámicamente
    for idx, (nombre, cuadro) in enumerate(campos.items()):
        x_pos = x_inicial + idx * (ancho + espacio)
        tk.Label(root, text=nombre, bg="light blue").place(x=x_pos, y=50, width=ancho)
        cuadro.place(x=x_pos, y=80, width=ancho, height=alto)

    # Función para cargar el historial
    def cargar_historial():
        try:
            cursor = con.cursor()
            cursor.execute("""
                EXEC sp_ConsultarHistorial
            """)
            resultados = cursor.fetchall()

            # Limpiar listboxes
            for cuadro in campos.values():
                cuadro.delete(0, tk.END)

            # Insertar filas en cada columna
            for fila in resultados:
                for i, (campo, cuadro) in enumerate(campos.items()):
                    cuadro.insert(tk.END, fila[i])

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el historial:\n{e}")

    # Botón para cargar datos
    tk.Button(root, text="Cargar Historial", command=cargar_historial, bg="light blue").place(x=850, y=10, width=200, height=40)
    tk.Button(root, text="<--", command=regresar, bg="light blue").place(x=20, y=10, width=200, height=40)
    root.mainloop()
