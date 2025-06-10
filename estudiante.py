
#estudiante.py
import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from tkinter import ttk
import cursan_interfaz  as cursan

import login_auditoria as log

def conectar_bd():
    try:
        conexion = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=ESCOOL;Trusted_Connection=yes;')
        return conexion
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
        return None


def iniciar_school(conexion, usuario):
    # Configuración de la ventana principal
    root = tk.Tk()
    root.title("Interfaz SCHOOL")
    root.geometry("1300x1000")
    root.configure(bg="light blue")
    # Conexión a la base de datos

    def abrir_ventana_cursan(no_control):
        if not no_control:
            messagebox.showerror("Error", "Debe ingresar un número de control válido.")
            return
        root.destroy()
        cursan.interfaz_cursan(conexion, no_control, usuario)

    def regresar():
        root.destroy()
        log.cargarlogin()


    def cargar_numeros_control():
        try:
            cursor = conexion.cursor()
            cursor.execute("EXEC sp_set_session_context @key=N'usuario_app', @value=?", (usuario,))
            cursor.execute("EXEC sp_ListarNoControl")
            numeros_control = [row[0] for row in cursor.fetchall()]
            combo_no_control['values'] = numeros_control
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los números de control:\n{e}")

    def seleccionar_no_control():
        seleccionado = combo_no_control.get()
        entry_no_control.delete(0, tk.END)
        entry_no_control.insert(0, seleccionado)


    def insertar_estudiante():
        no_control = entry_no_control.get().strip()
        nombre = entry_nombre.get().strip()
        ap_paterno = entry_apP.get().strip()
        ap_materno = entry_apM.get().strip()
        semestre = entry_semestre.get().strip()
        carrera = entry_carrera.get().strip()

        if not no_control or not nombre or not ap_paterno or not ap_materno or not semestre or not carrera:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            if not conexion:
                return
            cursor = conexion.cursor()
            cursor.execute("EXEC sp_set_session_context @key=N'usuario_app', @value=?", (usuario,))

            cursor.execute(
                "EXEC sp_InsertarEstudianteSolo ?, ?, ?, ?, ?, ?",
                (no_control, nombre, ap_paterno, ap_materno, semestre, carrera)
            )
            conexion.commit()
            messagebox.showinfo("Éxito", "Estudiante insertado correctamente.")
            limpiar_campos()
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"No se pudo insertar el estudiante: {str(e)}")

    # Función para consultar estudiantes con la vista
    def consultar_estudiante():
        no_control = entry_no_control.get().strip()

        if not no_control:
            messagebox.showerror("Error", "Debes ingresar el número de control.")
            return

        try:
            cursor = conexion.cursor()
            cursor.execute("EXEC sp_set_session_context @key=N'usuario_app', @value=?", (usuario,))

            # Consulta directa (puedes reemplazar esto por tu vista si es necesario)
            cursor.execute("EXEC sp_ConsultarEstudianteSolo ?", (no_control,))
            estudiante = cursor.fetchone()

            if estudiante:
                entry_nombre.delete(0, tk.END)
                entry_nombre.insert(0, estudiante[0])

                entry_apP.delete(0, tk.END)
                entry_apP.insert(0, estudiante[1])

                entry_apM.delete(0, tk.END)
                entry_apM.insert(0, estudiante[2])

                entry_semestre.delete(0, tk.END)
                entry_semestre.insert(0, estudiante[3])

                entry_carrera.delete(0, tk.END)
                entry_carrera.insert(0, estudiante[4])
            else:
                messagebox.showwarning("Advertencia", "No se encontró el estudiante.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo consultar el estudiante: {e}")


    def actualizar_estudiante():
        try:
            cursor = conexion.cursor()
            cursor.execute("EXEC sp_set_session_context @key=N'usuario_app', @value=?", (usuario,))
            
            # Llamar al procedimiento almacenado SOLO para actualizar Estudiante
            cursor.execute("""
                EXEC sp_ActualizarEstudianteSolo ?, ?, ?, ?, ?, ?
            """, (
                entry_no_control.get(),
                entry_nombre.get(),
                entry_apP.get(),
                entry_apM.get(),
                entry_semestre.get(),
                entry_carrera.get()
            ))
            
            conexion.commit()
            messagebox.showinfo("Éxito", "Estudiante actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el estudiante: {e}")

    def eliminar_estudiante():
        try:
            cursor = conexion.cursor()
            cursor.execute("EXEC sp_set_session_context @key=N'usuario_app', @value=?", (usuario,))
            
            no_control = entry_no_control.get()
            if not no_control:
                messagebox.showerror("Error", "Debes ingresar el número de control para eliminar.")
                return

            # Llamar al procedimiento almacenado solo para eliminar al estudiante
            cursor.execute("EXEC sp_EliminarEstudianteSolo ?", (no_control,))
            
            conexion.commit()
            messagebox.showinfo("Éxito", "Estudiante eliminado correctamente.")
            limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el estudiante: {e}")




    def listar_materias_estudiante():
        no_control = entry_no_control.get()

        if not no_control:
            messagebox.showerror("Error", "Debes ingresar el No. Control del estudiante.")
            return

        try:
            #conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute("EXEC sp_set_session_context @key=N'usuario_app', @value=?", (usuario,))

            # Llamar al procedimiento almacenado
            cursor.execute("EXEC sp_ListarMateriasEstudiantes ?", (no_control,))
            resultados = cursor.fetchall()

            # Limpiar los datos existentes en los Listbox
            cuadro_campo1.delete(0, tk.END)
            cuadro_campo2.delete(0, tk.END)
            cuadro_campo3.delete(0, tk.END)
            cuadro_campo4.delete(0, tk.END)

            # Insertar los datos obtenidos en los Listbox
            for fila in resultados:
                cuadro_campo1.insert(tk.END, fila[0])  # idmateria
                cuadro_campo2.insert(tk.END, fila[1])  # Materia
                cuadro_campo3.insert(tk.END, fila[2])  # Oportunidad
                cuadro_campo4.insert(tk.END, fila[3])  # Calificación
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron listar las materias: {e}")
        #finally:
            #if conexion:
                #conexion.close()


    # Función para limpiar los campos
    def limpiar_campos():
        entry_no_control.delete(0, tk.END)
        entry_nombre.delete(0, tk.END)
        entry_apP.delete(0, tk.END)
        entry_apM.delete(0, tk.END)
        entry_semestre.delete(0, tk.END)
        entry_carrera.delete(0, tk.END)



    def salir_aplicacion():
        respuesta = messagebox.askyesno("Salir", "¿Estás seguro de que deseas salir?")
        if respuesta:
            if conexion:
                conexion.close()
            root.destroy()  # Cierra la ventana principal


    # Widgets de la interfaz
    label_no_control = tk.Label(root, text="No. Control:")
    label_no_control.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_no_control = tk.Entry(root)
    entry_no_control.grid(row=0, column=1, padx=10, pady=5)

    label_nombre = tk.Label(root, text="Nombre:")
    label_nombre.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_nombre = tk.Entry(root)
    entry_nombre.grid(row=1, column=1, padx=10, pady=5)

    label_apP = tk.Label(root, text="Apellido Paterno:")
    label_apP.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_apP = tk.Entry(root)
    entry_apP.grid(row=2, column=1, padx=10, pady=5)

    label_apM = tk.Label(root, text="Apellido Materno:")
    label_apM.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entry_apM = tk.Entry(root)
    entry_apM.grid(row=3, column=1, padx=10, pady=5)

    label_semestre = tk.Label(root, text="Semestre:")
    label_semestre.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    entry_semestre = tk.Entry(root)
    entry_semestre.grid(row=4, column=1, padx=10, pady=5)

    label_carrera = tk.Label(root, text="Carrera:")
    label_carrera.grid(row=5, column=0, padx=10, pady=5, sticky="w")
    entry_carrera = tk.Entry(root)
    entry_carrera.grid(row=5, column=1, padx=10, pady=5)

  

    # Combobox para números de control
    label_combo_nc = tk.Label(root, text="Selecciona No. Control:")
    label_combo_nc.grid(row=10, column=0, padx=10, pady=5, sticky="w")

    combo_no_control = ttk.Combobox(root, state="readonly")
    combo_no_control.grid(row=10, column=1, padx=10, pady=5)

    combo_no_control.bind("<<ComboboxSelected>>", lambda event: seleccionar_no_control())

    # Botón para cargar los NoControl en el Combobox
    btn_cargar_nc = tk.Button(root, text="Cargar NoControl", command=cargar_numeros_control)
    btn_cargar_nc.place(x=350, y=240, width=250)

    # Botones
    btn_crear = tk.Button(root, text="insertar", command=insertar_estudiante)
    btn_crear.place(x=350, y=30, width=250)

    btn_consultar = tk.Button(root, text="Consultar Estudiante", command=consultar_estudiante)
    btn_consultar.place(x=350, y=60, width=250)


    btn_actualizar = tk.Button(root, text="Actualizar Estudiante", command=actualizar_estudiante)
    btn_actualizar.place(x=350, y=90, width=250)


    btn_eliminar = tk.Button(root, text="Eliminar Estudiante", command=eliminar_estudiante)
    btn_eliminar.place(x=350, y=120, width=250)

    btn_limpiar = tk.Button(root, text="Limpiar Campos", command=limpiar_campos)
    btn_limpiar.place(x=350, y=150, width=250)

    # Configuración de las etiquetas y Listbox para mostrar la tabla
    label_tablaC1 = tk.Label(root, text="idM", bg="light blue")
    label_tablaC1.place(x=100, y=350, width=250)
    cuadro_campo1 = tk.Listbox(root)
    cuadro_campo1.place(x=100, y=370, width=250, height=200)

    label_tablaC2 = tk.Label(root, text="Materia", bg="light blue")
    label_tablaC2.place(x=350, y=350, width=250)
    cuadro_campo2 = tk.Listbox(root)
    cuadro_campo2.place(x=350, y=370, width=250, height=200)

    label_tablaC3 = tk.Label(root, text="Oportunidad", bg="light blue")
    label_tablaC3.place(x=550, y=350, width=360)
    cuadro_campo3 = tk.Listbox(root)
    cuadro_campo3.place(x=550, y=370, width=360, height=200)

    label_tablaC4 = tk.Label(root, text="calificacion", bg="light blue")
    label_tablaC4.place(x=850, y=350, width=360)
    cuadro_campo4 = tk.Listbox(root)
    cuadro_campo4.place(x=850, y=370, width=360, height=200)

    btn_listar_materias = tk.Button(root, text="Listar Materias", command=listar_materias_estudiante)
    btn_listar_materias.place(x=350, y=210, width=250)

    btn_salir = tk.Button(root, text="Salir", command=salir_aplicacion)
    btn_salir.place(x=350, y=180, width=250)
    
    btn_asignar_materia = tk.Button(
        root, 
        text="Asignar Materia", 
        command=lambda: abrir_ventana_cursan(entry_no_control.get().strip())
    )
    btn_asignar_materia.place(x=700, y=250, width=200)

    tk.Button(root, text="<--", command=regresar, bg="light blue").place(x=1100, y=0, width=200, height=40)

    # Iniciar la aplicación
    root.mainloop()


