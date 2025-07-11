#menuadmn.py
import tkinter as tk
import auditoria_admin as adm
import consultas as cons
import historial as hist
import login_auditoria as log
from tkinter import  messagebox
def cargarmenu_adm(con):
    root = tk.Tk()
    root.title("Panel de Auditoría - Admin")
    root.geometry("600x400")
    root.configure(bg="#1F618D")

    def regresar():
        root.destroy()
        log.cargarlogin()

    def ir_a_auditoria():
        root.destroy()
        adm.abrir_ventana_admin(con)


    def ir_a_historial():
        root.destroy()
        hist.historial(con)

    def salir_aplicacion():
        respuesta = messagebox.askyesno("Salir", "¿Estás seguro de que deseas salir?")
        if respuesta:
            if con:
                con.close()
            root.destroy()

    # Marco lateral para botones
    menu_frame = tk.Frame(root, bg="#1F618D")
    menu_frame.place(x=0, y=0, width=500, height=600)  # <-- Asegura visibilidad

    # Botones dentro del marco
    btn_auditoria = tk.Button(menu_frame, text="Bitacora", command=ir_a_auditoria, bg="light blue")
    btn_auditoria.place(x=50, y=20, width=400, height=40)



    btn_historial = tk.Button(menu_frame, text="Historial", command=ir_a_historial, bg="light blue")
    btn_historial.place(x=50, y=140, width=400, height=40)

    btn_salir = tk.Button(menu_frame, text="Salir", command=salir_aplicacion, bg="light blue")
    btn_salir.place(x=50, y=200, width=400, height=40)

    tk.Button(menu_frame, text="<--", command=regresar, bg="light blue").place(x=50, y=260, width=400, height=40)

    root.mainloop()
