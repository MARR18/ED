#!/usr/bin/env python3
"""
Script de prueba para la librería external_sorting.
Demuestra:
- Ordenamiento de listas en memoria con los tres algoritmos.
- Ordenamiento de archivos (txt, csv, json).
- Uso de clave personalizada y orden descendente.
- Estadísticas de rendimiento.
"""

import os
import tempfile
import random
import string
from external_sorting import (
    RecursiveMergeSort,
    DirectMergeSort,
    BalancedMergeSort,
    FileManager,
    Benchmark,
)

def generar_lista_enteros(n: int):
    """Genera lista de enteros aleatorios."""
    return [random.randint(1, 100_000) for _ in range(n)]

def generar_lista_cadenas(n: int):
    """Genera lista de cadenas aleatorias."""
    return [
        ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
        for _ in range(n)
    ]

def prueba_ordenamiento_listas():
    print("=" * 60)
    print("1. ORDENAMIENTO DE LISTAS EN MEMORIA")
    print("=" * 60)

    # Datos de prueba
    datos_enteros = generar_lista_enteros(20)
    datos_cadenas = generar_lista_cadenas(20)

    print(f"\nLista original (enteros): {datos_enteros[:10]}...")
    print(f"Lista original (cadenas): {datos_cadenas[:10]}...")

    # Recursive Merge Sort
    sorter_rec = RecursiveMergeSort(reverse=False)
    sorted_rec = sorter_rec.sort(datos_enteros.copy())
    print(f"\n[Recursive Merge] Ordenado (enteros): {sorted_rec[:10]}...")
    print(f"  Estadísticas: tiempo={sorter_rec.stats.elapsed_time():.4f}s, "
          f"comparaciones={sorter_rec.stats.comparisons}, fusiones={sorter_rec.stats.merges}")

    # Direct Merge Sort con orden descendente
    sorter_dir = DirectMergeSort(reverse=True)
    sorted_dir_desc = sorter_dir.sort(datos_enteros.copy())
    print(f"\n[Direct Merge] Orden descendente (enteros): {sorted_dir_desc[:10]}...")
    print(f"  Estadísticas: tiempo={sorter_dir.stats.elapsed_time():.4f}s, "
          f"comparaciones={sorter_dir.stats.comparisons}, fusiones={sorter_dir.stats.merges}")

    # Balanced Merge Sort con clave longitud
    sorter_bal = BalancedMergeSort(chunk_size=5, reverse=False, key=lambda x: len(x))
    sorted_bal = sorter_bal.sort(datos_cadenas.copy())
    print(f"\n[Balanced K-Way] Ordenado por longitud (cadenas): {sorted_bal[:10]}...")
    print(f"  Estadísticas: tiempo={sorter_bal.stats.elapsed_time():.4f}s, "
          f"comparaciones={sorter_bal.stats.comparisons}, fusiones={sorter_bal.stats.merges}")

def prueba_archivos():
    print("\n" + "=" * 60)
    print("2. ORDENAMIENTO DE ARCHIVOS (EXTERNO)")
    print("=" * 60)

    # Crear archivo temporal de texto con enteros desordenados
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        input_txt = f.name
        for _ in range(500):
            f.write(str(random.randint(1, 10_000)) + "\n")
    output_txt = input_txt.replace('.txt', '_sorted.txt')
    print(f"\nArchivo de texto generado: {input_txt} (500 números)")

    # Balanced Merge Sort (externo)
    sorter_ext = BalancedMergeSort(k=4, chunk_size=100, use_multiprocessing=False)
    sorter_ext.sort_file(input_txt, output_txt)
    print(f"  Ordenado guardado en: {output_txt}")
    # Verificar primeras líneas
    with open(output_txt, 'r') as f:
        lines = [int(line.strip()) for line in f.readlines()]
    print(f"  Primeros 10 ordenados: {lines[:10]}")

    # Limpiar
    os.unlink(input_txt)
    os.unlink(output_txt)

    # Crear archivo CSV con registros (nombre, edad)
    input_csv = "temp_datos.csv"
    with open(input_csv, 'w', encoding='utf-8') as f:
        f.write("nombre,edad\n")
        nombres = ["Ana", "Luis", "Carlos", "Marta", "Javier", "Lucía", "Pedro", "Sofia"]
        for i in range(200):
            nombre = random.choice(nombres) + str(random.randint(1,100))
            edad = random.randint(18, 80)
            f.write(f"{nombre},{edad}\n")
    output_csv = "temp_datos_ordenados.csv"
    print(f"\nArchivo CSV generado: {input_csv} (200 registros)")

    # Ordenar por edad (clave custom) con Direct Merge (pero usamos Balanced porque puede ser grande)
    # Para demostrar clave custom en archivo, usamos BalancedMergeSort
    def key_edad(record):
        # record es una lista de strings: ['nombre', 'edad']
        return int(record[1])
    sorter_csv = BalancedMergeSort(chunk_size=50, reverse=False, key=key_edad)
    sorter_csv.sort_file(input_csv, output_csv)
    print(f"  Ordenado por edad (ascendente) guardado en: {output_csv}")
    # Mostrar primeros 10 registros ordenados
    sorted_data = FileManager.read_all(output_csv)
    print("  Primeros 5 ordenados por edad:")
    for rec in sorted_data[:5]:
        print(f"    {rec}")

    # Limpiar
    os.unlink(input_csv)
    os.unlink(output_csv)

    # Archivo JSON
    input_json = "temp_datos.json"
    datos_json = [{"id": i, "valor": random.random()} for i in range(100)]
    # Mezclar
    random.shuffle(datos_json)
    FileManager.write_records(datos_json, input_json)
    output_json = "temp_datos_ordenados.json"
    print(f"\nArchivo JSON generado: {input_json} (100 objetos)")

    sorter_json = BalancedMergeSort(chunk_size=20, key=lambda x: x["valor"])
    sorter_json.sort_file(input_json, output_json)
    print(f"  Ordenado por 'valor' guardado en: {output_json}")
    # Mostrar primeros 5
    res = FileManager.read_all(output_json)
    print("  Primeros 5 por valor:", [f"{r['valor']:.4f}" for r in res[:5]])

    os.unlink(input_json)
    os.unlink(output_json)

def prueba_benchmark_rapido():
    print("\n" + "=" * 60)
    print("3. BENCHMARK RÁPIDO (tamaños pequeños)")
    print("=" * 60)
    # Benchmark con listas pequeñas para no demorar
    resultados = Benchmark.run_benchmark(
        sizes=[200, 500],
        algorithms=["recursive", "direct", "balanced"],
        data_type="int",
        repeat=2
    )
    Benchmark.display_benchmark(resultados)

def prueba_visual_recursivo():
    print("\n" + "=" * 60)
    print("4. VISUALIZACIÓN DEL ÁRBOL DE MERGE SORT")
    print("=" * 60)
    datos = [3, 7, 1, 9, 4, 6, 2, 8]
    print(f"Lista original: {datos}")
    sorter = RecursiveMergeSort(visual=False)  # visual False para no mostrar estadísticas ahora
    # Llamar al método de visualización de árbol
    sorter.visualize_recursion(datos)
    # También ordenar para ver estadísticas
    sorted_data = sorter.sort(datos)
    print(f"Lista ordenada: {sorted_data}")
    sorter.stats.display()

if __name__ == "__main__":
    # Ejecutar todas las pruebas
    prueba_ordenamiento_listas()
    prueba_archivos()
    prueba_benchmark_rapido()
    prueba_visual_recursivo()
    print("\n" + "=" * 60)
    print("✅ PRUEBAS COMPLETADAS EXITOSAMENTE")
    print("=" * 60)