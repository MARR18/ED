import customtkinter as ctk
import time
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ================= ALGORITMOS =================

def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivote = arr[len(arr) // 2]
    menores = [x for x in arr if x < pivote]
    iguales = [x for x in arr if x == pivote]
    mayores = [x for x in arr if x > pivote]
    return quick_sort(menores) + iguales + quick_sort(mayores)


def heapify(arr, n, i):
    mayor = i
    izq = 2 * i + 1
    der = 2 * i + 2

    if izq < n and arr[izq] > arr[mayor]:
        mayor = izq
    if der < n and arr[der] > arr[mayor]:
        mayor = der

    if mayor != i:
        arr[i], arr[mayor] = arr[mayor], arr[i]
        heapify(arr, n, mayor)


def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr


def counting_sort(arr, exp):
    n = len(arr)
    salida = [0] * n
    conteo = [0] * 10

    for i in arr:
        index = i // exp
        conteo[index % 10] += 1

    for i in range(1, 10):
        conteo[i] += conteo[i - 1]

    for i in reversed(arr):
        index = i // exp
        salida[conteo[index % 10] - 1] = i
        conteo[index % 10] -= 1

    return salida


def radix_sort(arr):
    maximo = max(arr)
    exp = 1
    while maximo // exp > 0:
        arr = counting_sort(arr, exp)
        exp *= 10
    return arr


# ================= FUNCIONES GUI =================

def ejecutar():
    try:
        cantidad = int(entry_cantidad.get())
        numeros = list(map(int, entry_numeros.get().split(",")))

        if len(numeros) != cantidad:
            messagebox.showerror("Error", "La cantidad no coincide con los números ingresados.")
            return

        metodo = opcion.get()

        inicio = time.time()

        if metodo == "ShellSort":
            resultado = shell_sort(numeros.copy())
        elif metodo == "QuickSort":
            resultado = quick_sort(numeros.copy())
        elif metodo == "HeapSort":
            resultado = heap_sort(numeros.copy())
        elif metodo == "Radix Sort":
            if any(n < 0 for n in numeros):
                messagebox.showerror("Error", "Radix Sort solo admite números positivos.")
                return
            resultado = radix_sort(numeros.copy())
        else:
            messagebox.showerror("Error", "Selecciona un método válido.")
            return

        fin = time.time()

        output.configure(state="normal")
        output.delete("1.0", "end")
        output.insert("end", f"Resultado: {resultado}\n")
        output.insert("end", f"Tiempo: {fin - inicio:.6f} segundos")
        output.configure(state="disabled")

    except ValueError:
        messagebox.showerror("Error de entrada", "Ingresa solo números válidos separados por comas.")


# ================= INTERFAZ =================

app = ctk.CTk()
app.title("Ordenamientos - Interfaz Moderna")
app.geometry("600x500")

titulo = ctk.CTkLabel(app, text="Algoritmos de Ordenamiento", font=("Arial", 20))
titulo.pack(pady=10)

entry_cantidad = ctk.CTkEntry(app, placeholder_text="Cantidad de números")
entry_cantidad.pack(pady=10)

entry_numeros = ctk.CTkEntry(app, placeholder_text="Ej: 5,3,8,1,2")
entry_numeros.pack(pady=10)

opcion = ctk.StringVar(value="ShellSort")

menu = ctk.CTkOptionMenu(app, variable=opcion,
                         values=["ShellSort", "QuickSort", "HeapSort", "Radix Sort"])
menu.pack(pady=10)

btn = ctk.CTkButton(app, text="Ejecutar Ordenamiento", command=ejecutar)
btn.pack(pady=15)

output = ctk.CTkTextbox(app, height=150)
output.pack(pady=10, padx=20, fill="both")
output.configure(state="disabled")

app.mainloop()