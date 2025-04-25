#proyectoschoolv3.py
import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

# Conexión a la base de datos
def conectar_bd():
    try:
        conexion = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=ESCOOL;Trusted_Connection=yes;')
        return conexion
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
        return None



def insertar_estudiante():
    no_control = entry_no_control.get()
    nombre = entry_nombre.get()
    ap_paterno = entry_apP.get()
    ap_materno = entry_apM.get()
    semestre = entry_semestre.get()
    carrera = entry_carrera.get()
    calif = entry_calif.get()
    oportunidad = entry_oportunidad.get()
    id_materia = entry_id_materia.get()

    if not no_control or not nombre or not ap_paterno or not semestre or not carrera or not calif or not oportunidad or not id_materia:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    try:
        conexion = conectar_bd()
        if not conexion:
            return
        cursor = conexion.cursor()

        # Llamar al procedimiento almacenado con todos los valores
        cursor.execute(
            "EXEC sp_InsertarEstudiante ?, ?, ?, ?, ?, ?, ?, ?, ?",
            (no_control, nombre, ap_paterno, ap_materno, semestre, carrera, int(calif), oportunidad, int(id_materia))
        )
        conexion.commit()
        messagebox.showinfo("Éxito", "Estudiante y calificación insertados correctamente.")
        limpiar_campos()
    except pyodbc.Error as e:
        messagebox.showerror("Error", f"No se pudo insertar el estudiante: {str(e)}")
    finally:
        if conexion:
            conexion.close()



# Función para consultar estudiantes con la vista
def consultar_estudiante():
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        # Consultar información completa del estudiante desde la vista
        cursor.execute("SELECT * FROM vw_EstudianteCompleto WHERE NoControl = ?", (entry_no_control.get(),))
        estudiante = cursor.fetchone()
        
        if estudiante:
            # Mostrar información básica
            entry_nombre.delete(0, tk.END)
            entry_nombre.insert(0, estudiante[1])
            entry_apP.delete(0, tk.END)
            entry_apP.insert(0, estudiante[2])
            entry_apM.delete(0, tk.END)
            entry_apM.insert(0, estudiante[3])
            entry_semestre.delete(0, tk.END)
            entry_semestre.insert(0, estudiante[4])
            entry_carrera.delete(0, tk.END)
            entry_carrera.insert(0, estudiante[5])
            
            # Mostrar calificaciones y materias
            entry_calif.delete(0, tk.END)
            entry_calif.insert(0, estudiante[6] if estudiante[6] else "")
            entry_oportunidad.delete(0, tk.END)
            entry_oportunidad.insert(0, estudiante[7] if estudiante[7] else "")
            entry_id_materia.delete(0, tk.END)
            entry_id_materia.insert(0, estudiante[8] if estudiante[8] else "")
        else:
            messagebox.showwarning("Advertencia", "No se encontró el estudiante.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo consultar el estudiante: {e}")
    finally:
        if conexion:
            conexion.close()



# Función para registrar calificaciones
def registrar_calificacion():
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO cursan (calif, oportunidad, NoControl, idmateria)
            VALUES (?, ?, ?, ?)
        """, (entry_calif.get(), entry_oportunidad.get(), entry_no_control.get(), entry_id_materia.get()))
        conexion.commit()
        messagebox.showinfo("Éxito", "Calificación registrada correctamente.")
        limpiar_campos()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo registrar la calificación: {e}")
    finally:
        if conexion:
            conexion.close()

def actualizar_estudiante():
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        # Actualizar en Estudiante
        cursor.execute("""
            UPDATE Estudiante
            SET nombre = ?, apP = ?, apM = ?, semestre = ?, carrera = ?
            WHERE NoControl = ?
        """, (
            entry_nombre.get(),
            entry_apP.get(),
            entry_apM.get(),
            entry_semestre.get(),
            entry_carrera.get(),
            entry_no_control.get()
        ))
        
        # Actualizar en cursa
        cursor.execute("""
            UPDATE cursan
            SET calif = ?, oportunidad = ?, idmateria = ?
            WHERE NoControl = ?
        """, (
            entry_calif.get(),
            entry_oportunidad.get(),
            entry_id_materia.get(),
            entry_no_control.get()
        ))
        
        conexion.commit()
        messagebox.showinfo("Éxito", "Estudiante actualizado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar el estudiante: {e}")
    finally:
        if conexion:
            conexion.close()

def eliminar_estudiante():
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        no_control = entry_no_control.get()
        if not no_control:
            messagebox.showerror("Error", "Debes ingresar el número de control para eliminar.")
            return
        
        # Eliminar registros relacionados en la tabla 'cursan'
        cursor.execute("DELETE FROM cursan WHERE NoControl = ?", (no_control,))
        
        # Eliminar el estudiante de la tabla 'Estudiante'
        cursor.execute("DELETE FROM Estudiante WHERE NoControl = ?", (no_control,))
        
        conexion.commit()
        messagebox.showinfo("Éxito", "Estudiante eliminado correctamente.")
        limpiar_campos()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el estudiante: {e}")
    finally:
        if conexion:
            conexion.close()

def listar_materias_estudiante():
    no_control = entry_no_control.get()

    if not no_control:
        messagebox.showerror("Error", "Debes ingresar el No. Control del estudiante.")
        return

    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()

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
    finally:
        if conexion:
            conexion.close()


# Función para limpiar los campos
def limpiar_campos():
    entry_no_control.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_apP.delete(0, tk.END)
    entry_apM.delete(0, tk.END)
    entry_semestre.delete(0, tk.END)
    entry_carrera.delete(0, tk.END)
    entry_calif.delete(0, tk.END)
    entry_oportunidad.delete(0, tk.END)
    entry_id_materia.delete(0, tk.END)


def salir_aplicacion():
    respuesta = messagebox.askyesno("Salir", "¿Estás seguro de que deseas salir?")
    if respuesta:
        root.destroy()  # Cierra la ventana principal


# Configuración de la ventana principal
root = tk.Tk()
root.title("Interfaz SCHOOL")
root.geometry("1300x1000")

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

label_calif = tk.Label(root, text="Calificación:")
label_calif.grid(row=6, column=0, padx=10, pady=5, sticky="w")
entry_calif = tk.Entry(root)
entry_calif.grid(row=6, column=1, padx=10, pady=5)

label_oportunidad = tk.Label(root, text="Oportunidad:")
label_oportunidad.grid(row=7, column=0, padx=10, pady=5, sticky="w")
entry_oportunidad = tk.Entry(root)
entry_oportunidad.grid(row=7, column=1, padx=10, pady=5)

label_id_materia = tk.Label(root, text="ID Materia:")
label_id_materia.grid(row=8, column=0, padx=10, pady=5, sticky="w")
entry_id_materia = tk.Entry(root)
entry_id_materia.grid(row=8, column=1, padx=10, pady=5)

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
label_tablaC1.place(x=100, y=300, width=250)
cuadro_campo1 = tk.Listbox(root)
cuadro_campo1.place(x=100, y=320, width=250, height=200)

label_tablaC2 = tk.Label(root, text="Materia", bg="light blue")
label_tablaC2.place(x=350, y=300, width=250)
cuadro_campo2 = tk.Listbox(root)
cuadro_campo2.place(x=350, y=320, width=250, height=200)

label_tablaC3 = tk.Label(root, text="Oportunidad", bg="light blue")
label_tablaC3.place(x=550, y=300, width=360)
cuadro_campo3 = tk.Listbox(root)
cuadro_campo3.place(x=550, y=320, width=360, height=200)

label_tablaC4 = tk.Label(root, text="calificacion", bg="light blue")
label_tablaC4.place(x=850, y=300, width=360)
cuadro_campo4 = tk.Listbox(root)
cuadro_campo4.place(x=850, y=320, width=360, height=200)

btn_listar_materias = tk.Button(root, text="Listar Materias", command=listar_materias_estudiante)
btn_listar_materias.place(x=350, y=210, width=250)

btn_salir = tk.Button(root, text="Salir", command=salir_aplicacion)
btn_salir.place(x=350, y=180, width=250)

# Iniciar la aplicación
root.mainloop()
