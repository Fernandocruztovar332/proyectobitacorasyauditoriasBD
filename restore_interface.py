#restoration_interface.py
import tkinter as tk
from tkinter import filedialog, messagebox
import menuprincipal as mp

def restore_interface(con):
    root = tk.Tk()
    root.title("Restaurar Base de Datos")
    root.geometry("400x250")
    root.configure(bg="#1F618D")
    
    def hacer_restore(tipo):
        ruta = filedialog.askopenfilename(filetypes=[("Backup Files", "*.bak")])
        if ruta:
            try:
                con.autocommit = True
                cursor = con.cursor()
                cursor.execute("USE master")
                cursor.execute("ALTER DATABASE ESCOOL SET SINGLE_USER WITH ROLLBACK IMMEDIATE")
                if tipo == "full":
                    cursor.execute(f"RESTORE DATABASE ESCOOL FROM DISK = '{ruta}' WITH REPLACE, RECOVERY")
                elif tipo == "partial":
                    cursor.execute(f"RESTORE DATABASE ESCOOL FILEGROUP = 'PRIMARY' FROM DISK = '{ruta}' WITH REPLACE, RECOVERY")
                cursor.execute("ALTER DATABASE ESCOOL SET MULTI_USER")
                messagebox.showinfo("Éxito", "Restauración completada.")
            except Exception as e:
                messagebox.showerror("Error", f"Error en restauración:\n{e}")

    def regresar():
        root.destroy()
        mp.cargarmenu_adm(con)

    tk.Button(root, text="Restaurar Completo", command=lambda: hacer_restore("full")).pack(pady=10)
    tk.Button(root, text="Restaurar Parcial", command=lambda: hacer_restore("partial")).pack(pady=10)
    tk.Button(root, text="Salir", command=root.destroy).pack(pady=20)
    tk.Button(root, text="<--", command=regresar, bg="light blue").pack(pady=10)
    root.mainloop()