#cursan_interfaz.py
# Interfaz para asignar materias a un estudiante
import tkinter as tk
from tkinter import ttk, messagebox

def interfaz_cursan(conexion, no_control, usuario):
    ventana = tk.Toplevel()
    ventana.title("Asignar Materia")
    ventana.geometry("400x400")
    ventana.configure(bg="#1F618D")

    tk.Label(ventana, text=f"No. Control: {no_control}").pack(pady=10)

    tk.Label(ventana, text="Materia:").pack()
    combo_materia = ttk.Combobox(ventana, state="readonly")
    combo_materia.pack()

    tk.Label(ventana, text="ID Materia:").pack()
    entry_idmateria = tk.Entry(ventana)
    entry_idmateria.pack()

    tk.Label(ventana, text="Calificación:").pack()
    entry_calif = tk.Entry(ventana)
    entry_calif.pack()

    tk.Label(ventana, text="Oportunidad:").pack()
    entry_oportunidad = tk.Entry(ventana)
    entry_oportunidad.pack()

    # Cargar nombres de materias en combobox
    try:
        cursor = conexion.cursor()
        cursor.execute("EXEC sp_set_session_context @key=N'usuario_app', @value=?", (usuario,))
        cursor.execute("SELECT idmateria, nombreM FROM materia")
        materias = cursor.fetchall()
        materias_dict = {nombre: idm for idm, nombre in materias}
        combo_materia['values'] = list(materias_dict.keys())
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar materias: {e}")

    # Al seleccionar materia, llenar el campo ID
    def al_seleccionar_materia(event):
        nombre = combo_materia.get()
        entry_idmateria.delete(0, tk.END)
        entry_idmateria.insert(0, materias_dict[nombre])

    combo_materia.bind("<<ComboboxSelected>>", al_seleccionar_materia)

    # Botón para guardar la asignación
    def asignar_materia():
        try:
            idmateria = int(entry_idmateria.get())
            calif = int(entry_calif.get())
            oportunidad = entry_oportunidad.get()

            cursor = conexion.cursor()
            cursor.execute("EXEC sp_set_session_context @key=N'usuario_app', @value=?", (usuario,))
            cursor.execute("EXEC sp_InsertarCursan ?, ?, ?, ?", (no_control, idmateria, calif, oportunidad))
            conexion.commit()
            messagebox.showinfo("Éxito", "Materia asignada correctamente.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo asignar materia: {e}")


    def actualizar_cursan():
        try:
            idmateria = int(entry_idmateria.get())
            calif = int(entry_calif.get())
            oportunidad = entry_oportunidad.get()

            cursor = conexion.cursor()
            cursor.execute("EXEC sp_set_session_context @key=N'usuario_app', @value=?", (usuario,))
            cursor.execute("EXEC sp_ActualizarCursan ?, ?, ?, ?", (no_control, idmateria, calif, oportunidad))
            conexion.commit()
            messagebox.showinfo("Éxito", "Datos actualizados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {e}")

    def eliminar_cursan():
        try:
            idmateria = int(entry_idmateria.get())
            cursor = conexion.cursor()
            cursor.execute("EXEC sp_set_session_context @key=N'usuario_app', @value=?", (usuario,))
            cursor.execute("EXEC sp_EliminarCursan ?, ?", (no_control, idmateria))
            conexion.commit()
            messagebox.showinfo("Éxito", "Asignación eliminada correctamente.")
            entry_calif.delete(0, tk.END)
            entry_oportunidad.delete(0, tk.END)
            entry_idmateria.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")


    tk.Button(ventana, text="Actualizar", command=actualizar_cursan).pack(pady=10)
    tk.Button(ventana, text="Eliminar", command=eliminar_cursan).pack(pady=10)
    tk.Button(ventana, text="Asignar", command=asignar_materia).pack(pady=20)