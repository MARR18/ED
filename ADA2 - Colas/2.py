import tkinter as tk
from tkinter import messagebox

# -------- CLASE COLA --------
class Cola:
    def __init__(self):
        self.items = []

    def encolar(self, elemento):
        self.items.append(elemento)

    def desencolar(self):
        if not self.vacia():
            return self.items.pop(0)
        return None

    def vacia(self):
        return len(self.items) == 0

# -------- VARIABLES --------
colas = {}
contadores = {}

# -------- FUNCIONES --------
def agregar_cliente():
    servicio = entry_servicio.get()

    if servicio == "":
        messagebox.showwarning("Error", "Ingrese número de servicio")
        return

    servicio = int(servicio)

    if servicio not in colas:
        colas[servicio] = Cola()
        contadores[servicio] = 0

    contadores[servicio] += 1
    numero = contadores[servicio]

    colas[servicio].encolar(numero)

    actualizar_colas()

    label_info.config(text=f"Cliente agregado\nServicio {servicio} → Turno {numero}")

def atender_cliente():
    servicio = entry_servicio.get()

    if servicio == "":
        messagebox.showwarning("Error", "Ingrese número de servicio")
        return

    servicio = int(servicio)

    if servicio not in colas or colas[servicio].vacia():
        label_info.config(text=f"No hay clientes en servicio {servicio}")
        return

    numero = colas[servicio].desencolar()

    actualizar_colas()

    label_info.config(text=f"Atendiendo turno {numero}\nServicio {servicio}")

def actualizar_colas():
    lista_colas.delete(0, tk.END)

    for servicio in colas:
        clientes = ", ".join(map(str, colas[servicio].items))
        lista_colas.insert(tk.END, f"Servicio {servicio}: [{clientes}]")

# -------- INTERFAZ --------
ventana = tk.Tk()
ventana.title("Sistema de Colas - Seguros")
ventana.geometry("400x400")

titulo = tk.Label(ventana, text="Sistema de Colas", font=("Arial", 16))
titulo.pack(pady=10)

frame = tk.Frame(ventana)
frame.pack()

tk.Label(frame, text="Número de servicio:").grid(row=0, column=0)

entry_servicio = tk.Entry(frame)
entry_servicio.grid(row=0, column=1)

btn_agregar = tk.Button(ventana, text="Llegada Cliente (C)", command=agregar_cliente)
btn_agregar.pack(pady=5)

btn_atender = tk.Button(ventana, text="Atender Cliente (A)", command=atender_cliente)
btn_atender.pack(pady=5)

label_info = tk.Label(ventana, text="", fg="blue", font=("Arial", 11))
label_info.pack(pady=10)

tk.Label(ventana, text="Colas de servicios").pack()

lista_colas = tk.Listbox(ventana, width=40, height=10)
lista_colas.pack(pady=10)

ventana.mainloop()