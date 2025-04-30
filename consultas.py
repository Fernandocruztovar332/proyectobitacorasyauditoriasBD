import tkinter as tk
from tkinter import messagebox
import pyodbc
import menuprincipal as mp
def paneladmn(con):
    admin_ventana = tk.Tk()
    admin_ventana.title("Panel de Administrador")
    admin_ventana.geometry("800x600")
    admin_ventana.configure(bg="#1F618D")

    # Label y Entry para escribir la consulta
    tk.Label(admin_ventana, text="Consulta SQL:", bg="#1F618D", fg="white", font=("Arial", 12)).pack(pady=10)
    entrada_consulta = tk.Entry(admin_ventana, width=100, font=("Arial", 12))
    entrada_consulta.pack(pady=5)

    # Textbox para mostrar resultados
    area_resultados = tk.Text(admin_ventana, height=25, width=120, font=("Courier", 10))
    area_resultados.pack(pady=10)

    def ejecutar_consulta():
        query = entrada_consulta.get()

        if not query.strip():
            messagebox.showwarning("Advertencia", "Por favor ingresa una consulta SQL.")
            return

        try:
            cursor = con.cursor()
            cursor.execute(query)

            try:
                resultados = cursor.fetchall()
                columnas = [desc[0] for desc in cursor.description]

                # Mostrar resultados
                area_resultados.delete("1.0", tk.END)
                area_resultados.insert(tk.END, "\t".join(columnas) + "\n")
                area_resultados.insert(tk.END, "-" * 100 + "\n")
                for fila in resultados:
                    area_resultados.insert(tk.END, "\t".join(str(dato) for dato in fila) + "\n")
            except pyodbc.ProgrammingError:
                con.commit()
                area_resultados.delete("1.0", tk.END)
                area_resultados.insert(tk.END, "✅ Consulta ejecutada correctamente (sin resultados).")

        except Exception as e:
            area_resultados.delete("1.0", tk.END)
            area_resultados.insert(tk.END, f"❌ Error al ejecutar consulta:\n{str(e)}")

    # Botón para ejecutar la consulta
    tk.Button(admin_ventana, text="Ejecutar Consulta", command=ejecutar_consulta, bg="light green").pack(pady=5)
    tk.Button(admin_ventana, text="<--", command=mp.cargarmenu_adm, bg="light blue").place(x=20, y=0, width=200, height=40)