import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

# Conexión a la base de datos
def conectar_bd():
    try:
        conexion = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=SCHOOL;Trusted_Connection=yes;')
        return conexion
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
        return None



def insertar_estudiante():
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        # Insertar en Estudiante
        cursor.execute("""
            INSERT INTO Estudiante (NoControl, nombre, apP, apM, semestre, carrera)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            entry_no_control.get(),
            entry_nombre.get(),
            entry_apP.get(),
            entry_apM.get(),
            entry_semestre.get(),
            entry_carrera.get()
        ))
        
        # Insertar en cursa
        cursor.execute("""
            INSERT INTO cursa (NoControl, calif, oportunidad, idmateria)
            VALUES (?, ?, ?, ?)
        """, (
            entry_no_control.get(),
            entry_calif.get() or 0,  # Valor inicial para calificación
            entry_oportunidad.get() or 'Primera',
            entry_id_materia.get() or None
        ))
        
        conexion.commit()
        messagebox.showinfo("Éxito", "Estudiante creado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo insertar el estudiante: {e}")
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
            INSERT INTO cursa (calif, oportunidad, NoControl, idmateria)
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
            UPDATE cursa
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

# Función para eliminar un estudiante
def eliminar_estudiante():
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Estudiante WHERE NoControl = ?", (entry_no_control.get(),))
        conexion.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Éxito", "Estudiante eliminado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "No se encontró el estudiante para eliminar.")
        limpiar_campos()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el estudiante: {e}")
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

# Configuración de la ventana principal
root = tk.Tk()
root.title("Interfaz SCHOOL")
root.geometry("600x600")

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
btn_crear = tk.Button(root, text="Crear Estudiante", command=insertar_estudiante)
btn_crear.grid(row=9, column=0, padx=10, pady=10)

btn_consultar = tk.Button(root, text="Consultar Estudiante", command=consultar_estudiante)
btn_consultar.grid(row=9, column=1, padx=10, pady=10)

btn_calificacion = tk.Button(root, text="Registrar Calificación", command=registrar_calificacion)
btn_calificacion.grid(row=10, column=0, padx=10, pady=10)

btn_actualizar = tk.Button(root, text="Actualizar Estudiante", command=actualizar_estudiante)
btn_actualizar.grid(row=10, column=1, padx=10, pady=10)

btn_eliminar = tk.Button(root, text="Eliminar Estudiante", command=eliminar_estudiante)
btn_eliminar.grid(row=11, column=0, padx=10, pady=10)

btn_limpiar = tk.Button(root, text="Limpiar Campos", command=limpiar_campos)
btn_limpiar.grid(row=11, column=1, padx=10, pady=10)

# Iniciar la aplicación
root.mainloop()
