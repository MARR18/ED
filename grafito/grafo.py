import tkinter as tk
from tkinter import messagebox
import math
from collections import deque

# ================== GRAFO ==================
class Grafo:
    def __init__(self):
        self.vertices = {}
        self.aristas = []

    def agregar_vertice(self, v):
        if v not in self.vertices:
            self.vertices[v] = []

    def agregar_arista(self, v, w):
        if v in self.vertices and w in self.vertices:
            if (v, w) not in self.aristas:
                self.vertices[v].append(w)
                self.aristas.append((v, w))

    def tiene_ciclo(self):
        visitado = set()
        stack = set()

        def dfs(v):
            visitado.add(v)
            stack.add(v)

            for vecino in self.vertices[v]:
                if vecino not in visitado:
                    if dfs(vecino):
                        return True
                elif vecino in stack:
                    return True

            stack.remove(v)
            return False

        for v in self.vertices:
            if v not in visitado:
                if dfs(v):
                    return True
        return False

    def bfs(self, inicio):
        visitado = set()
        cola = deque([inicio])
        orden = []

        while cola:
            v = cola.popleft()
            if v not in visitado:
                visitado.add(v)
                orden.append(v)
                for vecino in self.vertices[v]:
                    cola.append(vecino)
        return orden


# ================== APP ==================
class App:
    def __init__(self, root):
        self.grafo = Grafo()
        self.root = root
        self.root.title("💀 GRAFO MODO DIOS FINAL")
        self.root.geometry("1200x700")
        self.root.config(bg="#0f172a")

        self.pos = {}
        self.dragging = None

        panel = tk.Frame(root, bg="#0f172a")
        panel.pack(side="left", fill="y", padx=10, pady=10)

        self.entry = tk.Entry(panel)
        self.entry.pack()
        tk.Button(panel, text="Agregar Nodo", command=self.add_vertice).pack()

        self.v1 = tk.Entry(panel)
        self.v1.pack()
        self.v2 = tk.Entry(panel)
        self.v2.pack()
        tk.Button(panel, text="Agregar Arista", command=self.add_arista).pack()

        tk.Button(panel, text="Detectar Ciclo", command=self.detectar_ciclo).pack(pady=5)
        tk.Button(panel, text="Animar BFS", command=self.animar_bfs).pack(pady=5)

        self.canvas = tk.Canvas(root, bg="#020617")
        self.canvas.pack(side="right", expand=True, fill="both")

        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<B1-Motion>", self.drag)

    # ================= FUNCIONES =================
    def add_vertice(self):
        v = self.entry.get()
        if v:
            self.grafo.agregar_vertice(v)
            self.pos[v] = (100 + len(self.pos)*80, 200)
            self.dibujar()

    def add_arista(self):
        v1 = self.v1.get()
        v2 = self.v2.get()
        self.grafo.agregar_arista(v1, v2)
        self.dibujar()

    def detectar_ciclo(self):
        if self.grafo.tiene_ciclo():
            messagebox.showinfo("Resultado", "🔥 Tiene ciclo")
        else:
            messagebox.showinfo("Resultado", "✅ No tiene ciclo")

    def animar_bfs(self):
        inicio = self.entry.get()
        orden = self.grafo.bfs(inicio)
        self.animar_lista(orden, 0)

    def animar_lista(self, lista, i):
        if i >= len(lista):
            return
        v = lista[i]
        x, y = self.pos[v]
        self.canvas.create_oval(x-30, y-30, x+30, y+30, fill="#facc15")
        self.root.after(600, lambda: self.animar_lista(lista, i+1))

    # ================= DRAG =================
    def click(self, event):
        for v, (x, y) in self.pos.items():
            if (x-25 < event.x < x+25) and (y-25 < event.y < y+25):
                self.dragging = v

    def drag(self, event):
        if self.dragging:
            self.pos[self.dragging] = (event.x, event.y)
            self.dibujar()

    # ================= DIBUJO =================
    def dibujar(self):
        self.canvas.delete("all")

        for (v1, v2) in self.grafo.aristas:
            x1, y1 = self.pos.get(v1, (0,0))
            x2, y2 = self.pos.get(v2, (0,0))

            if v1 == v2:
                self.canvas.create_arc(x1-30, y1-50, x1+30, y1-10,
                                       start=0, extent=300,
                                       style=tk.ARC, outline="red", width=3)
            else:
                self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="white", width=2)

        for v, (x, y) in self.pos.items():
            self.canvas.create_oval(x-25, y-25, x+25, y+25, fill="#38bdf8")
            self.canvas.create_text(x, y, text=v, fill="white")


# ================= MAIN =================
root = tk.Tk()
app = App(root)
root.mainloop()