import tkinter as tk
from tkinter import messagebox

MAX = 8
pila = []
tope = 0

def dibujar_pila(lista):
    canvas.delete("all")
    y = 250

    for elemento in reversed(lista):
        canvas.create_rectangle(120, y-40, 220, y, fill="lightblue")
        canvas.create_text(170, y-20, text=str(elemento), font=("Arial", 12))
        y -= 45

def actualizar_pila():
    dibujar_pila(pila)
    label_tope.config(text=f"TOPE = {tope}")

def insertar():
    global tope

    elemento = entrada_insertar.get()

    if elemento == "":
        messagebox.showwarning("Error","Escribe un elemento")
        return

    if tope >= MAX:
        messagebox.showerror("Error","Desbordamiento")
        return

    pila.append(elemento)
    tope += 1

    proceso.set(f"Insertar:\nTOPE = TOPE + 1\nPILA[TOPE] = {elemento}")

    actualizar_pila()
    entrada_insertar.delete(0, tk.END)

def eliminar():
    global tope

    variable = entrada_variable.get()

    if variable == "":
        messagebox.showwarning("Error","Escribe una variable")
        return

    if tope == 0:
        messagebox.showerror("Error","Subdesbordamiento")
        return

    # SI LA VARIABLE ESTA EN LA PILA
    if variable in pila:

        pila.remove(variable)
        tope -= 1

        proceso.set(
            f"Proceso:\n"
            f"La variable {variable} se encontró en la pila\n"
            f"Se elimina directamente"
        )

        actualizar_pila()

    # SI NO ESTA EN LA PILA
    else:

        pila_temp = pila.copy()
        pila_temp.append(variable)

        proceso.set(
            f"Proceso:\n"
            f"{variable} no está en la pila\n"
            f"Se agrega temporalmente"
        )

        dibujar_pila(pila_temp)

        ventana.after(1500, lambda: eliminar_temporal(variable))

def eliminar_temporal(variable):

    proceso.set(
        f"Proceso:\n"
        f"Se elimina el elemento temporal {variable}"
    )

    actualizar_pila()
    entrada_variable.delete(0, tk.END)

ventana = tk.Tk()
ventana.title("Simulador de Pila")
ventana.geometry("420x450")

tk.Label(ventana,text="Elemento a insertar").pack()

entrada_insertar = tk.Entry(ventana)
entrada_insertar.pack()

tk.Button(ventana,text="Insertar",command=insertar).pack(pady=5)

tk.Label(ventana,text="Variable al eliminar").pack()

entrada_variable = tk.Entry(ventana)
entrada_variable.pack()

tk.Button(ventana,text="Eliminar",command=eliminar).pack(pady=5)

canvas = tk.Canvas(ventana,width=350,height=260,bg="white")
canvas.pack(pady=10)

label_tope = tk.Label(ventana,text="TOPE = 0",font=("Arial",12))
label_tope.pack()

proceso = tk.StringVar()
tk.Label(ventana,textvariable=proceso,justify="left").pack(pady=10)

ventana.mainloop()