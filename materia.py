import tkinter as tk
from tkinter import messagebox
import pyodbc
from tkinter import ttk  # Esto permite usar ttk.Combobox

def interfaz_materias(conexion, usuario):
    root = tk.Tk()
    root.title("Gestión de Materias")
    root.geometry("600x400")
    root.configure(bg="#1F618D")

    # ---------- Funciones ----------
    def insertar_materia():
        nombre = entry_nombre.get()
        horasP = entry_horasP.get()
        horasT = entry_horasT.get()
        creditos = entry_creditos.get()

        if not nombre or not horasP or not horasT or not creditos:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            cursor = conexion.cursor()
            cursor.execute("EXEC sp_set_session_context @key=N'usuario_app', @value=?", (usuario,))
            cursor.execute("EXEC sp_InsertarMateria ?, ?, ?, ?",
                           (nombre, horasP, horasT, int(creditos)))
            conexion.commit()
            messagebox.showinfo("Éxito", "Materia insertada correctamente.")
            limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo insertar la materia: {e}")

            
    def actualizar_materia():
        idmateria = entry_idmateria.get().strip()
        nombre = entry_nombre.get().strip()
        horasP = entry_horasP.get().strip()
        horasT = entry_horasT.get().strip()
        creditos = entry_creditos.get().strip()

        if not idmateria:
            messagebox.showerror("Error", "Debes seleccionar una materia válida para actualizar.")
            return

        try:
            cursor = conexion.cursor()
            cursor.execute("EXEC sp_set_session_context @key=N'usuario_app', @value=?", (usuario,))
            cursor.execute(
                "EXEC sp_ActualizarMateria ?, ?, ?, ?, ?",
                (
                    int(idmateria),
                    nombre if nombre else '',
                    horasP if horasP else '',
                    horasT if horasT else '',
                    int(creditos) if creditos else 0
                )
            )
            conexion.commit()
            messagebox.showinfo("Éxito", "Materia actualizada correctamente.")
            limpiar_campos()
            cargar_materias()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la materia: {e}")

    def eliminar_materia():
        idmateria = entry_idmateria.get()

        if not idmateria:
            messagebox.showerror("Error", "Debes ingresar el ID de la materia a eliminar.")
            return

        try:
            cursor = conexion.cursor()
            cursor.execute("EXEC sp_set_session_context @key=N'usuario_app', @value=?", (usuario,))
            cursor.execute("EXEC sp_EliminarMateria ?", (int(idmateria),))
            conexion.commit()
            messagebox.showinfo("Éxito", "Materia eliminada correctamente.")
            limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la materia: {e}")


    def limpiar_campos():
        entry_nombre.delete(0, tk.END)
        entry_horasP.delete(0, tk.END)
        entry_horasT.delete(0, tk.END)
        entry_creditos.delete(0, tk.END)
        entry_idmateria.delete(0, tk.END)

    # ---------- Widgets ----------
    tk.Label(root, text="ID Materia (solo para actualizar/eliminar):", bg="#1F618D", fg="white").pack()
    entry_idmateria = tk.Entry(root)
    entry_idmateria.pack(pady=5)

    tk.Label(root, text="Nombre de la materia:", bg="#1F618D", fg="white").pack()
    entry_nombre = tk.Entry(root)
    entry_nombre.pack(pady=5)

    tk.Label(root, text="Horas prácticas:", bg="#1F618D", fg="white").pack()
    entry_horasP = tk.Entry(root)
    entry_horasP.pack(pady=5)

    tk.Label(root, text="Horas teóricas:", bg="#1F618D", fg="white").pack()
    entry_horasT = tk.Entry(root)
    entry_horasT.pack(pady=5)

    tk.Label(root, text="Créditos:", bg="#1F618D", fg="white").pack()
    entry_creditos = tk.Entry(root)
    entry_creditos.pack(pady=5)

    tk.Button(root, text="Insertar Materia", command=insertar_materia).pack(pady=10)

    # Deja botones vacíos para completar con otras funciones después
    tk.Button(root, text="Actualizar Materia", command=actualizar_materia).pack(pady=5)
    tk.Button(root, text="Eliminar Materia", command=eliminar_materia).pack(pady=5)
    tk.Button(root, text="Limpiar Campos", command=limpiar_campos).pack(pady=10)

    materias_dict = {}

    tk.Label(root, text="Selecciona una materia:", bg="#1F618D", fg="white").pack()
    combo_materias = tk.ttk.Combobox(root, state="readonly")
    combo_materias.pack(pady=5)

    # Función para llenar el Combobox con nombres de materias
    def cargar_materias():
        try:
            cursor = conexion.cursor()
            cursor.execute("EXEC sp_set_session_context @key=N'usuario_app', @value=?", (usuario,))
            cursor.execute("EXEC sp_ListarMateriasDetalles")
            materias = cursor.fetchall()
            
            for idmat, nombre, hp, ht, cred in materias:
                materias_dict[nombre] = (idmat, hp, ht, cred)

            combo_materias['values'] = list(materias_dict.keys())
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las materias:\n{e}")

    def al_seleccionar_materia(event):
        nombre = combo_materias.get()
        if nombre in materias_dict:
            idmat, hp, ht, cred = materias_dict[nombre]
            entry_idmateria.delete(0, tk.END)
            entry_idmateria.insert(0, idmat)
            entry_nombre.delete(0, tk.END)
            entry_nombre.insert(0, nombre)
            entry_horasP.delete(0, tk.END)
            entry_horasP.insert(0, hp)
            entry_horasT.delete(0, tk.END)
            entry_horasT.insert(0, ht)
            entry_creditos.delete(0, tk.END)
            entry_creditos.insert(0, cred)

    combo_materias.bind("<<ComboboxSelected>>", al_seleccionar_materia)

    cargar_materias()

    root.mainloop()