class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class MyLinkedList:
    def __init__(self):
        self.cabeza = None

    # ─── Insertar al inicio ───────────────────────────────
    def insertar_inicio(self, dato):
        nuevo = Nodo(dato)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo

    def insertar_final(self, dato):
        nuevo = Nodo(dato)
        if not self.cabeza:
            self.cabeza = nuevo
            return
        
        actual = self.cabeza
        while actual.siguiente:
            actual = actual.siguiente
        
        actual.siguiente = nuevo

    def eliminar(self, dato):
        actual = self.cabeza

        # Si el nodo a eliminar es la cabeza
        if actual and actual.dato == dato:
            self.cabeza = actual.siguiente
            return True

        anterior = None
        while actual and actual.dato != dato:
            anterior = actual
            actual = actual.siguiente

        if actual is None:
            return False

        anterior.siguiente = actual.siguiente
        return True

    def buscar(self, dato):
        actual = self.cabeza
        while actual:
            if actual.dato == dato:
                return True
            actual = actual.siguiente
        return False

    def mostrar(self):
        elementos = []
        actual = self.cabeza
        while actual:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def tamaño(self):
        contador = 0
        actual = self.cabeza
        while actual:
            contador += 1
            actual = actual.siguiente
        return contador

    def esta_vacia(self):
        return self.cabeza is None