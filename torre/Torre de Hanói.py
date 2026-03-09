import tkinter as tk
import time

movimientos = 0
torres = {"A": [], "B": [], "C": []}
discos = 0
inicio = 0

# Dibujar torres y discos
def dibujar():
    canvas.delete("all")

    posiciones = {"A": 150, "B": 350, "C": 550}

    # dibujar torres
    for torre in posiciones:
        x = posiciones[torre]
        canvas.create_rectangle(x-5, 150, x+5, 350, fill="black")

    # dibujar discos
    for torre in torres:
        x = posiciones[torre]
        y = 330

        for disco in torres[torre]:
            ancho = disco * 20
            canvas.create_rectangle(
                x-ancho, y-20, x+ancho, y,
                fill="skyblue"
            )
            canvas.create_text(x, y-10, text=str(disco))
            y -= 22

    ventana.update()

# Movimiento visual
def mover(origen, destino):
    global movimientos

    disco = torres[origen].pop()
    torres[destino].append(disco)

    movimientos += 1
    label_mov.config(text=f"Movimientos: {movimientos}")

    dibujar()
    time.sleep(0.5)

# Algoritmo recursivo
def hanoi(n, origen, auxiliar, destino):
    if n == 1:
        mover(origen, destino)
        return

    hanoi(n-1, origen, destino, auxiliar)
    mover(origen, destino)
    hanoi(n-1, auxiliar, origen, destino)

# Iniciar simulación
def iniciar():
    global discos, movimientos, inicio

    movimientos = 0
    discos = int(entry.get())

    torres["A"] = list(range(discos, 0, -1))
    torres["B"] = []
    torres["C"] = []

    dibujar()

    inicio = time.time()

    hanoi(discos, "A", "B", "C")

    fin = time.time()
    tiempo = round(fin - inicio, 4)

    label_tiempo.config(text=f"Tiempo: {tiempo} s")

# Ventana
ventana = tk.Tk()
ventana.title("Torre de Hanoi")
ventana.geometry("700x450")

titulo = tk.Label(ventana, text="Simulación Torre de Hanoi", font=("Arial",16))
titulo.pack(pady=10)

frame = tk.Frame(ventana)
frame.pack()

tk.Label(frame, text="Número de discos:").grid(row=0, column=0)

entry = tk.Entry(frame, width=5)
entry.grid(row=0, column=1)

btn = tk.Button(frame, text="Iniciar", command=iniciar)
btn.grid(row=0, column=2, padx=10)

canvas = tk.Canvas(ventana, width=700, height=350, bg="white")
canvas.pack()

label_mov = tk.Label(ventana, text="Movimientos: 0", font=("Arial",12))
label_mov.pack()

label_tiempo = tk.Label(ventana, text="Tiempo: 0 s", font=("Arial",12))
label_tiempo.pack()

ventana.mainloop()