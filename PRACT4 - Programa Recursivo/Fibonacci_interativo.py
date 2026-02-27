contador_iterativo = 0

def fibonacci_iterativo(n):
    global contador_iterativo
    a, b = 0, 1

    for i in range(n):
        contador_iterativo += 1
        a, b = b, a + b

    return a

# Programa principal
n = int(input("Ingresa el número de Fibonacci a calcular: "))

contador_iterativo = 0
resultado = fibonacci_iterativo(n)

print("\nRESULTADO ITERATIVO")
print("----------------------------")
print(f"Fibonacci({n}) = {resultado}")
print(f"Número de iteraciones: {contador_iterativo}")