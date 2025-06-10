import tkinter as tk
from tkinter import messagebox
import estudiante_crud as est
import materia_crud as mat
import cursan_crud as cur

def panel_admin(con):
    root = tk.Tk()
    root.title("Panel de Administrador")
    root.geometry("600x400")
    root.configure(bg="#1F618D")

    def abrir_estudiantes():
        root.destroy()
        est.crud_estudiante(con)

    def abrir_materias():
        root.destroy()
        mat.crud_materia(con)

    def abrir_cursan():
        root.destroy()
        cur.crud_cursan(con)

    tk.Label(root, text="Administrador", font=("Arial", 16), bg="#1F618D", fg="white").pack(pady=20)
    tk.Button(root, text="Gestionar Estudiantes", command=abrir_estudiantes, width=30).pack(pady=10)
    tk.Button(root, text="Gestionar Materias", command=abrir_materias, width=30).pack(pady=10)
    tk.Button(root, text="Gestionar Cursan", command=abrir_cursan, width=30).pack(pady=10)
    tk.Button(root, text="Salir", command=root.destroy, width=30, bg="lightgray").pack(pady=30)

    root.mainloop()
