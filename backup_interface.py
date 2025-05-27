import tkinter as tk
from tkinter import filedialog, messagebox

def backup_interface(con):
    root = tk.Tk()
    root.title("Respaldo de Base de Datos")
    root.geometry("400x250")
    root.configure(bg="#1F618D")

    def hacer_respaldo(tipo):
        ruta = filedialog.asksaveasfilename(
            defaultextension=".bak",
            filetypes=[("Backup Files", "*.bak")],
            title="Guardar archivo de respaldo"
        )
        if ruta:
            try:
                cursor = con.cursor()
                if tipo == "full":
                    comando = f"BACKUP DATABASE ESCOOL TO DISK = '{ruta}' WITH INIT"
                elif tipo == "partial":
                    comando = f"BACKUP DATABASE ESCOOL FILEGROUP = 'PRIMARY' TO DISK = '{ruta}' WITH INIT"
                else:
                    raise ValueError("Tipo de respaldo no válido.")

                cursor.execute(comando)
                messagebox.showinfo("Éxito", f"Respaldo {tipo} realizado correctamente en:\n{ruta}")
            except Exception as e:
                messagebox.showerror("Error en respaldo", str(e))

    tk.Label(root, text="Opciones de Respaldo", font=("Arial", 14), bg="#1F618D", fg="white").pack(pady=10)
    tk.Button(root, text="Respaldo Completo", command=lambda: hacer_respaldo("full"), width=25).pack(pady=10)
    tk.Button(root, text="Respaldo Parcial", command=lambda: hacer_respaldo("partial"), width=25).pack(pady=10)
    tk.Button(root, text="Salir", command=root.destroy, width=25, bg="lightgray").pack(pady=20)

    root.mainloop()