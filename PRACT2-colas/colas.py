import tkinter as tk
from tkinter import messagebox

# =========================
# Clase Order
# =========================
class Order:

    def __init__(self, qtty, customer):
        self.customer = customer
        self.qtty = qtty

    def print(self):
        return f"Customer: {self.customer} | Quantity: {self.qtty}"

    def getQtty(self):
        return self.qtty

    def getCustomer(self):
        return self.customer


# =========================
# Clase Node
# =========================
class Node:

    def __init__(self, info):
        self.info = info
        self.next = None

    def getNext(self):
        return self.next

    def setNext(self, node):
        self.next = node

    def getInfo(self):
        return self.info


# =========================
# Clase Queue
# =========================
class Queue:

    def __init__(self):
        self.top = None
        self.tail = None
        self.count = 0

    def size(self):
        return self.count

    def isEmpty(self):
        return self.count == 0

    def front(self):
        if self.isEmpty():
            return None
        return self.top.getInfo()

    def enqueue(self, info):
        newNode = Node(info)

        if self.isEmpty():
            self.top = newNode
            self.tail = newNode
        else:
            self.tail.setNext(newNode)
            self.tail = newNode

        self.count += 1

    def dequeue(self):

        if self.isEmpty():
            return None

        removed = self.top.getInfo()
        self.top = self.top.getNext()
        self.count -= 1

        if self.top is None:
            self.tail = None

        return removed

    def getNth(self, pos):

        if pos <= 0 or pos > self.size():
            return None

        node = self.top
        count = 1

        while node != None:

            if count == pos:
                return node.getInfo()

            node = node.getNext()
            count += 1

        return None

    def getAll(self):

        node = self.top
        orders = []

        while node != None:
            orders.append(node.getInfo())
            node = node.getNext()

        return orders


# =========================
# INTERFAZ GRÁFICA
# =========================

queue = Queue()

def actualizar_lista():

    listbox.delete(0, tk.END)

    for i, order in enumerate(queue.getAll(), start=1):
        listbox.insert(tk.END, f"{i}. {order.print()}")

    size_label.config(text=f"Pedidos en cola: {queue.size()}")


def agregar():

    cliente = entry_cliente.get()
    cantidad = entry_cantidad.get()

    if cliente == "" or cantidad == "":
        messagebox.showerror("Error", "Completa todos los campos")
        return

    try:
        cantidad = int(cantidad)
    except:
        messagebox.showerror("Error", "Cantidad debe ser número")
        return

    pedido = Order(cantidad, cliente)
    queue.enqueue(pedido)

    entry_cliente.delete(0, tk.END)
    entry_cantidad.delete(0, tk.END)

    actualizar_lista()


def eliminar():

    pedido = queue.dequeue()

    if pedido:
        messagebox.showinfo("Pedido atendido", pedido.print())
    else:
        messagebox.showwarning("Cola vacía", "No hay pedidos")

    actualizar_lista()


def ver_primero():

    pedido = queue.front()

    if pedido:
        messagebox.showinfo("Primer pedido", pedido.print())
    else:
        messagebox.showwarning("Cola vacía", "No hay pedidos")


def obtener_n():

    try:
        pos = int(entry_pos.get())
    except:
        messagebox.showerror("Error", "Ingresa un número válido")
        return

    pedido = queue.getNth(pos)

    if pedido:
        messagebox.showinfo("Pedido encontrado", pedido.print())
    else:
        messagebox.showwarning("Error", "Posición inválida")


# =========================
# VENTANA
# =========================

ventana = tk.Tk()
ventana.title("Sistema de Pedidos - Queue")
ventana.geometry("650x500")
ventana.configure(bg="#2c3e50")

titulo = tk.Label(
    ventana,
    text="Sistema de Gestión de Pedidos",
    font=("Arial", 18, "bold"),
    bg="#2c3e50",
    fg="white"
)
titulo.pack(pady=10)

frame_inputs = tk.Frame(ventana, bg="#34495e")
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Cliente", bg="#34495e", fg="white").grid(row=0, column=0)
entry_cliente = tk.Entry(frame_inputs)
entry_cliente.grid(row=0, column=1, padx=10)

tk.Label(frame_inputs, text="Cantidad", bg="#34495e", fg="white").grid(row=1, column=0)
entry_cantidad = tk.Entry(frame_inputs)
entry_cantidad.grid(row=1, column=1, padx=10)

btn_agregar = tk.Button(
    frame_inputs,
    text="Agregar Pedido",
    bg="#27ae60",
    fg="white",
    command=agregar
)
btn_agregar.grid(row=2, columnspan=2, pady=10)

frame_lista = tk.Frame(ventana)
frame_lista.pack()

listbox = tk.Listbox(frame_lista, width=70, height=12)
listbox.pack()

size_label = tk.Label(
    ventana,
    text="Pedidos en cola: 0",
    font=("Arial", 12),
    bg="#2c3e50",
    fg="white"
)
size_label.pack(pady=5)

frame_botones = tk.Frame(ventana, bg="#2c3e50")
frame_botones.pack(pady=10)

btn_front = tk.Button(frame_botones, text="Ver Primero", command=ver_primero, width=15)
btn_front.grid(row=0, column=0, padx=5)

btn_dequeue = tk.Button(frame_botones, text="Atender Pedido", command=eliminar, width=15)
btn_dequeue.grid(row=0, column=1, padx=5)

entry_pos = tk.Entry(frame_botones, width=5)
entry_pos.grid(row=0, column=2)

btn_get = tk.Button(frame_botones, text="Buscar N", command=obtener_n)
btn_get.grid(row=0, column=3, padx=5)

ventana.mainloop()