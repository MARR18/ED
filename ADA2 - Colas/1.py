class Cola:
    def __init__(self):
        self.items = []

    def esta_vacia(self):
        return len(self.items) == 0

    def encolar(self, elemento):
        self.items.append(elemento)

    def desencolar(self):
        if not self.esta_vacia():
            return self.items.pop(0)

    def tamano(self):
        return len(self.items)

    def mostrar(self):
        return self.items


def sumar_colas(colaA, colaB):
    cola_resultado = Cola()

    while not colaA.esta_vacia() and not colaB.esta_vacia():
        a = colaA.desencolar()
        b = colaB.desencolar()
        cola_resultado.encolar(a + b)

    return cola_resultado


# Ejemplo de uso
colaA = Cola()
colaB = Cola()

# Datos de ejemplo
datosA = [3, 4, 2, 8, 12]
datosB = [6, 2, 9, 11, 3]

for i in datosA:
    colaA.encolar(i)

for i in datosB:
    colaB.encolar(i)

resultado = sumar_colas(colaA, colaB)

print("Cola Resultado:", resultado.mostrar())