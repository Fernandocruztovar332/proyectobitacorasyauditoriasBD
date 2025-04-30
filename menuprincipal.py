#menuadmn.py
import tkinter as tk
import auditoria_admin as adm
import consultas as cons
import historial as hist
import login_auditoria as log

def cargarmenu_adm(con):
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Panel de Auditoría - Admin")
    root.geometry("1200x600")
    root.configure(bg="#1F618D")

    # Crear un marco para el menú
    menu_frame = tk.Frame(root, bg="#1F618D")
    menu_frame.pack(side=tk.TOP, fill=tk.X)

    # Crear botones para el menú
    btn_auditoria = tk.Button(menu_frame, text="Auditoría", command=lambda: adm.abrir_ventana_admin(con), bg="light blue")
    btn_auditoria.pack(side=tk.LEFT, padx=50, pady=20)

    #btn_configuracion = tk.Button(menu_frame, text="Configuración", command=lambda: abrir_ventana_configuracion(conexion), bg="light blue")
    #btn_configuracion.pack(side=tk.LEFT, padx=10, pady=10)

    btn_consultas = tk.Button(menu_frame, text="Consultas", command=lambda: cons.paneladmn(con), bg="light blue")
    btn_consultas.pack(side=tk.LEFT, padx=50, pady=50)

    btn_historial = tk.Button(menu_frame, text="Historial", command=lambda: hist.historial(con), bg="light blue")
    btn_historial.pack(side=tk.LEFT, padx=50, pady=70)

    btn_salir = tk.Button(menu_frame, text="Salir", command=root.quit, bg="light blue")
    btn_salir.pack(side=tk.LEFT, padx=50, pady=90)
    tk.Button(root, text="<--", command=log.cargarlogin, bg="light blue").place(x=0, y=0, width=200, height=40)

    # Iniciar el bucle principal de la ventana
    root.mainloop()