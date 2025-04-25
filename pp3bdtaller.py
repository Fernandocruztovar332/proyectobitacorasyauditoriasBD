import tkinter as tk  # Importa la biblioteca tkinter para crear interfaces gráficas
from tkinter import messagebox  # Importa el módulo messagebox para mostrar mensajes emergentes
from tkinter import ttk  # Importa ttk para utilizar widgets mejorados en tkinter
import pyodbc  # Importa pyodbc para conectarse a bases de datos SQL Server

# Declarar las variables globales para las entradas
entry_categoryid = None  # Entrada para el ID de la categoría
entry_categoryname = None  # Entrada para el nombre de la categoría
entry_description = None  # Entrada para la descripción de la categoría
cmb = None  # Para el Combobox que contendrá los IDs
cuadro_campo1 = None  # Listbox para mostrar los IDs de las categorías
cuadro_campo2 = None  # Listbox para mostrar los nombres de las categorías
cuadro_campo3 = None  # Listbox para mostrar las descripciones de las categorías

# Configuración de la conexión a SQL Server
connection_string = ('DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=TSQL2012;Trusted_Connection=yes;')
# Función para verificar la conexión a la base de datos
def verificar_conexion():
    try:
        # Intenta conectar a la base de datos utilizando la cadena de conexión
        conn = pyodbc.connect(connection_string)
        conn.close()  # Cierra la conexión si es exitosa
        messagebox.showinfo("Conexión exitosa", "Conexión exitosa a SQL Server.")
        root.deiconify()  # Muestra la ventana principal después de aceptar el mensaje
        configurar_interfaz()  # Configura la interfaz de la aplicación
    except Exception as e:
        # Si hay un error en la conexión, muestra un mensaje de error
        messagebox.showerror("Error de conexión", f"No se pudo conectar a SQL Server.\n{str(e)}")
        root.destroy()  # Cierra la aplicación si hay un error en la conexión

# Función para cargar los IDs en el Combobox
def cargar_categoryids():
    try:
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute("EXEC BUSCARIDs")  # Llama al procedimiento almacenado para obtener los IDs
            # Extrae los IDs, los convierte a cadena y los ordena
            ids = sorted([str(row[0]) for row in cursor.fetchall()])
            cmb['values'] = ids  # Asigna los IDs al Combobox
            if ids:
                cmb.set(ids[0])  # Selecciona el primer ID por defecto
            else:
                cmb.set('')  # Si no hay IDs, limpia el Combobox
    except Exception as e:
        messagebox.showerror("Error al cargar IDs", str(e))  # Muestra un mensaje de error si falla

# Función para cargar los datos en la tabla
def cargar_tabla():
    global cuadro_campo1, cuadro_campo2, cuadro_campo3

    try:
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute("EXEC MOSTRARTODO")  # Ejecuta el procedimiento almacenado para mostrar todos los datos
            filas = cursor.fetchall()  # Obtiene todas las filas resultantes de la consulta

            # Limpia los Listbox antes de insertar nuevos datos
            cuadro_campo1.delete(0, tk.END)
            cuadro_campo2.delete(0, tk.END)
            cuadro_campo3.delete(0, tk.END)

            # Procesa los datos obtenidos de la consulta
            idt = [str(row[0]) for row in filas]  # Lista de IDs de las categorías
            categoria = [str(row[1]) for row in filas]  # Lista de nombres de las categorías
            descripcion = [str(row[2]) for row in filas]  # Lista de descripciones de las categorías

            # Inserta los datos en los Listbox correspondientes
            for i in range(len(idt)):
                cuadro_campo1.insert(0, idt[i])
                cuadro_campo2.insert(0, categoria[i])
                cuadro_campo3.insert(0, descripcion[i])
                
    except Exception as e:
        print(f"Error al cargar la tabla: {str(e)}")  # Imprime un mensaje de error en la consola

# Función para configurar la interfaz de gestión de categorías
def configurar_interfaz():
    global entry_categoryid, entry_categoryname, entry_description, cmb, cuadro_campo1, cuadro_campo2, cuadro_campo3

    # Etiquetas y campos de entrada
    lbl_categoryid = tk.Label(root, text="ID de Categoría:", bg="light blue")
    lbl_categoryid.place(x=10, y=40, width=170, height=30)
    entry_categoryid = tk.Entry(root)
    entry_categoryid.place(x=10, y=10, width=170, height=30)

    root.title("Gestión de Categorías")  # Establece el título de la ventana
    cmb = ttk.Combobox(root)
    cmb.place(x=10, y=70, width=170, height=30)
    cmb.bind("<<ComboboxSelected>>", on_categoryid_selected)  # Enlaza la selección del Combobox con una función

    cargar_categoryids()  # Carga los IDs en el Combobox al iniciar

    # Configuración de etiquetas y entradas para el nombre y descripción de la categoría
    lbl_categoryname = tk.Label(root, text="Nombre de Categoría:", bg="light blue")
    lbl_categoryname.place(x=10, y=130, width=170, height=30)
    entry_categoryname = tk.Entry(root)
    entry_categoryname.place(x=10, y=100, width=170, height=30)

    lbl_description = tk.Label(root, text="Descripción:", bg="light blue")
    lbl_description.place(x=10, y=190, width=170, height=30)
    entry_description = tk.Entry(root)
    entry_description.place(x=10, y=160, width=170, height=30)

    # Configuración de los botones para distintas acciones
    btn_insertar = tk.Button(root, text="Insertar", command=insertar_categoria, bg="light blue")
    btn_insertar.place(x=10, y=230, width=170, height=50)

    btn_actualizar = tk.Button(root, text="Actualizar", command=actualizar_categoria, bg="light blue")
    btn_actualizar.place(x=10, y=280, width=170, height=50)

    btn_eliminar = tk.Button(root, text="Eliminar", command=eliminar_categoria, bg="light blue")
    btn_eliminar.place(x=10, y=330, width=170, height=50)

    btn_buscar = tk.Button(root, text="Buscar", command=buscar_categoria, bg="light blue")
    btn_buscar.place(x=10, y=380, width=170, height=50)

    btn_salir = tk.Button(root, text="Salir", command=salir, bg="#EC7063")
    btn_salir.place(x=10, y=430, width=170, height=50)

    btn_cargar = tk.Button(root, text="Cargar Tabla", command=cargar_tabla, bg="light blue")
    btn_cargar.place(x=841, y=290, width=170, height=50)

    # Configuración de las etiquetas y Listbox para mostrar la tabla
    label_tablaC1 = tk.Label(root, text="id", bg="light blue")
    label_tablaC1.place(x=200, y=70, width=250)
    cuadro_campo1 = tk.Listbox(root)
    cuadro_campo1.place(x=200, y=90, width=250, height=200)

    label_tablaC2 = tk.Label(root, text="nombres", bg="light blue")
    label_tablaC2.place(x=450, y=70, width=250)
    cuadro_campo2 = tk.Listbox(root)
    cuadro_campo2.place(x=450, y=90, width=250, height=200)

    label_tablaC3 = tk.Label(root, text="descripcion", bg="light blue")
    label_tablaC3.place(x=650, y=70, width=360)
    cuadro_campo3 = tk.Listbox(root)
    cuadro_campo3.place(x=650, y=90, width=360, height=200)

# Función para manejar la selección de un ID en el Combobox
def on_categoryid_selected(event):
    categoryid = cmb.get()  # Obtiene el ID seleccionado
    buscar_categoria_por_id(categoryid)  # Llama a la función para buscar la categoría correspondiente

# Función para buscar una categoría por ID y mostrar sus detalles
def buscar_categoria_por_id(categoryid):
    try:
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()
            # Ejecuta un procedimiento almacenado para buscar la categoría por su ID
            cursor.execute("EXEC BuscarCategoria @categoryid = ?", categoryid)
            row = cursor.fetchone()  # Obtiene el resultado de la consulta

            if row:
                # Si se encuentra la categoría, muestra sus detalles en los campos de entrada correspondientes
                entry_categoryid.delete(0, tk.END)  # Limpia el campo de entrada del ID
                entry_categoryid.insert(0, str(row.categoryid))  # Inserta el ID encontrado

                entry_categoryname.delete(0, tk.END)  # Limpia el campo de entrada del nombre
                entry_categoryname.insert(0, row.categoryname)  # Inserta el nombre encontrado

                entry_description.delete(0, tk.END)  # Limpia el campo de entrada de la descripción
                entry_description.insert(0, row.description)  # Inserta la descripción encontrada
            else:
                # Si no se encuentra la categoría, muestra un mensaje de información
                messagebox.showinfo("Resultados de la búsqueda", "No se encontraron resultados.")
    except Exception as e:
        # Muestra un mensaje de error si ocurre algún problema al buscar
        messagebox.showerror("Error", str(e))

# Función para insertar una nueva categoría en la base de datos
def insertar_categoria():
    categoryname = entry_categoryname.get()  # Obtiene el nombre de la categoría desde el campo de entrada
    description = entry_description.get()  # Obtiene la descripción de la categoría desde el campo de entrada
    
    # Confirma la inserción con el usuario antes de proceder
    if messagebox.askyesno("Confirmar inserción", f"¿Desea insertar la categoría '{categoryname}' con la descripción '{description}'?"):
        try:
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()
                # Ejecuta un procedimiento almacenado para insertar la categoría
                cursor.execute("EXEC InsertarCategoria @categoryname = ?, @description = ?", categoryname, description)
                conn.commit()  # Confirma la transacción en la base de datos
                messagebox.showinfo("Éxito", "Categoría insertada correctamente.")
                cargar_categoryids()  # Actualiza los IDs en el Combobox para reflejar el cambio
        except Exception as e:
            # Muestra un mensaje de error si falla la inserción
            messagebox.showerror("Error", str(e))

# Función para actualizar una categoría existente en la base de datos
def actualizar_categoria():
    categoryid = entry_categoryid.get()  # Obtiene el ID de la categoría desde el campo de entrada
    categoryname = entry_categoryname.get()  # Obtiene el nombre de la categoría desde el campo de entrada
    description = entry_description.get()  # Obtiene la descripción de la categoría desde el campo de entrada
    
    # Confirma la actualización con el usuario antes de proceder
    if messagebox.askyesno("Confirmar actualización", f"¿Desea actualizar la categoría ID '{categoryid}' a '{categoryname}' con la descripción '{description}'?"):
        try:
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()
                # Ejecuta un procedimiento almacenado para actualizar la categoría
                cursor.execute("EXEC ActualizarCategoria @categoryid = ?, @categoryname = ?, @description = ?", categoryid, categoryname, description)
                conn.commit()  # Confirma la transacción en la base de datos
                messagebox.showinfo("Éxito", "Categoría actualizada correctamente.")
                cargar_categoryids()  # Actualiza los IDs en el Combobox para reflejar el cambio
        except Exception as e:
            # Muestra un mensaje de error si falla la actualización
            messagebox.showerror("Error", str(e))

# Función para eliminar una categoría de la base de datos
def eliminar_categoria():
    categoryid = entry_categoryid.get()  # Obtiene el ID de la categoría desde el campo de entrada
    
    # Confirma la eliminación con el usuario antes de proceder
    if messagebox.askyesno("Confirmar eliminación", f"¿Desea eliminar la categoría ID '{categoryid}'?"):
        try:
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()
                # Ejecuta un procedimiento almacenado para eliminar la categoría
                cursor.execute("EXEC EliminarCategoria @categoryid = ?", categoryid)
                conn.commit()  # Confirma la transacción en la base de datos
                messagebox.showinfo("Éxito", "Categoría eliminada correctamente.")
                cargar_categoryids()  # Actualiza los IDs en el Combobox para reflejar el cambio
        except Exception as e:
            # Muestra un mensaje de error si falla la eliminación
            messagebox.showerror("Error", str(e))

# Función para buscar una categoría por ID a través del botón de búsqueda
def buscar_categoria():
    categoryid = entry_categoryid.get()  # Obtiene el ID de la categoría desde el campo de entrada
    
    # Validación para asegurarse de que el ID sea un número y no esté vacío
    if not categoryid.isdigit() or not categoryid:
        messagebox.showerror("Error", "Por favor, ingrese un ID válido.")
        return
    
    # Confirma la búsqueda con el usuario antes de proceder
    if messagebox.askyesno("Confirmar búsqueda", f"¿Desea buscar la categoría con ID '{categoryid}'?"):
        try:
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()
                # Ejecuta un procedimiento almacenado para buscar la categoría por su ID
                cursor.execute("EXEC BuscarCategoria @categoryid = ?", int(categoryid))
                rows = cursor.fetchall()  # Obtiene todos los resultados de la consulta

                # Muestra los resultados de la búsqueda en un mensaje emergente
                resultado = ""
                for row in rows:
                    resultado += f"ID: {row.categoryid}, Nombre: {row.categoryname}, Descripción: {row.description}\n"

                if resultado:
                    messagebox.showinfo("Resultados de la búsqueda", resultado)
                else:
                    messagebox.showinfo("Resultados de la búsqueda", "No se encontraron resultados.")
        except Exception as e:
            # Muestra un mensaje de error si falla la búsqueda
            messagebox.showerror("Error", str(e))

# Función para salir de la aplicación
def salir():
    # Confirma la salida con el usuario antes de cerrar la aplicación
    if messagebox.askyesno("Confirmar salida", "¿Está seguro de que desea salir del programa?"):
        root.destroy()  # Cierra la ventana principal y finaliza el programa

# Crear la ventana principal de la aplicación
root = tk.Tk()  # Instancia de la ventana principal de tkinter
root.title("Gestión de Categorías")  # Establece el título de la ventana
root.geometry("1080x520")  # Configura el tamaño de la ventana
root.configure(bg="#1F618D")  # Establece el color de fondo de la ventana

# Oculta la ventana principal inicialmente para verificar la conexión primero
root.withdraw()

# Verifica la conexión a la base de datos al iniciar la aplicación
verificar_conexion()

# Inicia el bucle principal de la aplicación para gestionar los eventos de la interfaz gráfica
root.mainloop()