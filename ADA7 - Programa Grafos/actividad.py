import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations

# Crear grafo
G = nx.Graph()

# Estados (nodos)
estados = [
    "Yucatán", "Campeche", "Quintana Roo",
    "Tabasco", "Chiapas", "Veracruz", "Oaxaca"
]

G.add_nodes_from(estados)

# Conexiones con costos (puedes modificarlos)
conexiones = [
    ("Yucatán", "Campeche", 100),
    ("Yucatán", "Quintana Roo", 120),
    ("Campeche", "Tabasco", 150),
    ("Tabasco", "Chiapas", 200),
    ("Chiapas", "Oaxaca", 180),
    ("Oaxaca", "Veracruz", 220),
    ("Veracruz", "Tabasco", 160),
    ("Quintana Roo", "Campeche", 140)
]

# Agregar aristas
for origen, destino, costo in conexiones:
    G.add_edge(origen, destino, weight=costo)

print("Estados y sus relaciones:")
for u, v, data in G.edges(data=True):
    print(f"{u} <--> {v} | Costo: {data['weight']}")

# -------------------------------
# FUNCION PARA CALCULAR COSTO
# -------------------------------
def calcular_costo(camino):
    costo_total = 0
    for i in range(len(camino) - 1):
        if G.has_edge(camino[i], camino[i+1]):
            costo_total += G[camino[i]][camino[i+1]]['weight']
        else:
            return float('inf')  # camino inválido
    return costo_total

# -------------------------------
# INCISO A: SIN REPETIR
# -------------------------------
print("\nRecorrido sin repetir estados:")
mejor_camino = None
menor_costo = float('inf')

for ruta in permutations(estados):
    costo = calcular_costo(ruta)
    if costo < menor_costo:
        menor_costo = costo
        mejor_camino = ruta

print("Mejor ruta:", mejor_camino)
print("Costo total:", menor_costo)

print("\nRecorrido repitiendo al menos un estado:")

ruta_repetida = list(estados) + [estados[0]]
costo_repetido = calcular_costo(ruta_repetida)

print("Ruta:", ruta_repetida)
print("Costo total:", costo_repetido)

pos = nx.spring_layout(G)

nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

plt.title("Grafo de Estados y Costos")
plt.show()