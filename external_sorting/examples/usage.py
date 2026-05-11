"""Example usage of the external sorting library."""

from external_sorting import (
    RecursiveMergeSort,
    DirectMergeSort,
    BalancedMergeSort,
    Benchmark,
    FileManager,
)


def example_sort_list():
    print("=== Recursive Merge Sort on list ===")
    data = [64, 25, 12, 22, 11, 90]
    sorter = RecursiveMergeSort(visual=True)
    sorted_data = sorter.sort(data)
    print(f"Original: {data}")
    print(f"Sorted:   {sorted_data}\n")


def example_sort_file():
    print("=== Balanced K‑Way Merge Sort on file ===")
    # Create a sample file
    sample_data = [str(i) for i in range(100, 0, -1)]
    FileManager.write_records(sample_data, "sample_input.txt")
    sorter = BalancedMergeSort(k=4, chunk_size=20, use_multiprocessing=False)
    sorter.sort_file("sample_input.txt", "sample_sorted.txt")
    # Verify
    sorted_result = FileManager.read_all("sample_sorted.txt")
    print(f"First 10 sorted: {sorted_result[:10]}\n")


def example_custom_key():
    print("=== Sorting by custom key (length of string) descending ===")
    words = ["python", "java", "go", "rust", "cplusplus", "swift"]
    sorter = DirectMergeSort(reverse=True, key=lambda x: len(x))
    sorted_words = sorter.sort(words)
    print(f"Original: {words}")
    print(f"Sorted by length desc: {sorted_words}\n")


def example_benchmark():
    print("=== Benchmark small comparison ===")
    results = Benchmark.run_benchmark([500, 1000], ["recursive", "direct"], repeat=2)
    Benchmark.display_benchmark(results)


if __name__ == "__main__":
    example_sort_list()
    example_sort_file()
    example_custom_key()
    example_benchmark()