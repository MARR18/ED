contador_recursivo = 0

def fibonacci_recursivo(n):
    global contador_recursivo
    contador_recursivo += 1

    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_recursivo(n - 1) + fibonacci_recursivo(n - 2)

# Programa principal
n = int(input("Ingresa el número de Fibonacci a calcular: "))

contador_recursivo = 0
resultado = fibonacci_recursivo(n)

print("\nRESULTADO RECURSIVO")
print("----------------------------")
print(f"Fibonacci({n}) = {resultado}")
print(f"Número de llamadas recursivas: {contador_recursivo}")