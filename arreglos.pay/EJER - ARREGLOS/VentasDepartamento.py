ventas = [
    [120, 95, 80],   
    [110, 90, 75],   
    [130, 100, 85],  
    [140, 110, 90],  
    [150, 120, 100], 
    [160, 130, 110], 
    [170, 140, 120], 
    [165, 135, 115], 
    [155, 125, 105], 
    [180, 150, 130],  
    [190, 160, 140], 
    [200, 170, 160]  
]

meses = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

departamentos = ["Ropa", "Deportes", "Juguetería"]


def insertar_venta(matriz):
    fila = int(input("Mes (1-12): ")) - 1
    columna = int(input("Departamento (1=Ropa, 2=Deportes, 3=Juguetería): ")) - 1
    valor = float(input("Nueva venta: "))
    matriz[fila][columna] = valor
    print("Venta insertada correctamente.")

def buscar_venta(matriz):
    valor = float(input("Ingrese la venta a buscar: "))
    encontrado = False
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == valor:
                print(f"Venta encontrada en {meses[i]} - {departamentos[j]}")
                encontrado = True
    if not encontrado:
        print("La venta no fue encontrada.")

def eliminar_venta(matriz):
    fila = int(input("Mes (1-12): ")) - 1
    columna = int(input("Departamento (1=Ropa, 2=Deportes, 3=Juguetería): ")) - 1
    matriz[fila][columna] = 0
    print("Venta eliminada correctamente.")

def mostrar_tabla(matriz):
    print(f"\n{'Mes':<12}{'Ropa':>12}{'Deportes':>12}{'Juguetería':>14}")
    print("-" * 50)
    for i in range(len(matriz)):
        print(f"{meses[i]:<12}", end="")
        for valor in matriz[i]:
            print(f"{valor:>12}", end="")
        print()


while True:
    print("\n--- MENÚ DE OPCIONES ---")
    print("1. Insertar venta")
    print("2. Buscar venta")
    print("3. Eliminar venta")
    print("4. Mostrar tabla")
    print("5. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        insertar_venta(ventas)
    elif opcion == "2":
        buscar_venta(ventas)
    elif opcion == "3":
        eliminar_venta(ventas)
    elif opcion == "4":
        mostrar_tabla(ventas)
    elif opcion == "5":
        print("Saliendo del programa...")
        break
    else:
        print("Opción no válida, intente de nuevo.")
