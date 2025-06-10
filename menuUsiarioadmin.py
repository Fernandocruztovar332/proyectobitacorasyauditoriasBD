import tkinter as tk
from tkinter import messagebox
import estudiante as est
import materia as mat
import consultas as cons


def panel_admin(con, usuario):
    root = tk.Tk()
    root.title("Panel de Administrador")
    root.geometry("600x400")
    root.configure(bg="#1F618D")

    def abrir_estudiantes():
        root.destroy()
        est.iniciar_school(con, usuario)

    def abrir_materias():
        root.destroy()
        mat.interfaz_materias(con, usuario)



   

    tk.Label(root, text="Administrador", font=("Arial", 16), bg="#1F618D", fg="white").pack(pady=20)
    tk.Button(root, text="Gestionar Estudiantes", command=abrir_estudiantes, width=30).pack(pady=10)
    tk.Button(root, text="Gestionar Materias", command=abrir_materias, width=30).pack(pady=10)
    tk.Button(root, text="Salir", command=root.destroy, width=30, bg="lightgray").pack(pady=10)
    


    root.mainloop()
