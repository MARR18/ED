import tkinter as tk
from tkinter import messagebox

MAX = 8
pila = []

def actualizar_pila():
    canvas.delete("all")
    y = 350

    for elemento in reversed(pila):
        canvas.create_rectangle(150, y-40, 350, y, fill="#4ECDC4", outline="black")
        canvas.create_text(250, y-20, text=str(elemento), font=("Arial", 14, "bold"))
        y -= 45

    estado()

def push():
    valor = entrada.get()

    if valor == "":
        messagebox.showwarning("Aviso", "Ingresa un valor")
        return

    if len(pila) == MAX:
        messagebox.showerror("Error", "La pila está llena")
    else:
        pila.append(valor)
        entrada.delete(0, tk.END)
        actualizar_pila()

def pop():
    if len(pila) == 0:
        messagebox.showerror("Error", "La pila está vacía")
    else:
        eliminado = pila.pop()
        messagebox.showinfo("Pop", f"Se eliminó el elemento del tope: {eliminado}")
        actualizar_pila()

def peek():
    if len(pila) == 0:
        messagebox.showinfo("Peek", "La pila está vacía")
    else:
        messagebox.showinfo("Peek", f"El elemento en el tope es: {pila[-1]}")

def limpiar():
    pila.clear()
    actualizar_pila()

def estado():
    if len(pila) == 0:
        label_estado.config(text="Estado: Pila Vacía")
    elif len(pila) == MAX:
        label_estado.config(text="Estado: Pila Llena")
    else:
        label_estado.config(text=f"Elementos en pila: {len(pila)} / {MAX}")

# Ventana
ventana = tk.Tk()
ventana.title("Simulador de Pila")
ventana.geometry("600x550")

titulo = tk.Label(ventana, text="Simulación de Pila (STACK)", font=("Arial",18,"bold"))
titulo.pack(pady=10)

entrada = tk.Entry(ventana, font=("Arial",12))
entrada.pack(pady=5)

frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=10)

btn_push = tk.Button(frame_botones, text="Push", width=10, command=push)
btn_push.grid(row=0, column=0, padx=5)

btn_pop = tk.Button(frame_botones, text="Pop", width=10, command=pop)
btn_pop.grid(row=0, column=1, padx=5)

btn_peek = tk.Button(frame_botones, text="Peek", width=10, command=peek)
btn_peek.grid(row=0, column=2, padx=5)

btn_clear = tk.Button(frame_botones, text="Vaciar", width=10, command=limpiar)
btn_clear.grid(row=0, column=3, padx=5)

canvas = tk.Canvas(ventana, width=500, height=350, bg="white")
canvas.pack()

label_estado = tk.Label(ventana, text="Estado: Pila Vacía", font=("Arial",12))
label_estado.pack(pady=5)

# Panel de explicación
explicacion = tk.Label(
    ventana,
    text=(
        "Operaciones de una pila:\n\n"
        "Push → Inserta un elemento en el tope de la pila.\n"
        "Pop → Elimina el elemento que está en el tope de la pila.\n"
        "Peek → Muestra el elemento del tope sin eliminarlo.\n"
        "Vaciar → Elimina todos los elementos de la pila.\n\n"
        "Las pilas funcionan con el principio LIFO:\n"
        "Last In, First Out (El último en entrar es el primero en salir)."
    ),
    font=("Arial",11),
    justify="left"
)

explicacion.pack(pady=10)

ventana.mainloop()