"""Benchmarking suite to compare performance of the three algorithms."""

import random
import string
import time
from typing import Dict, List, Any

from rich.table import Table

from . import BalancedMergeSort, DirectMergeSort, RecursiveMergeSort
from .utils import console


class Benchmark:
    """Run performance benchmarks on different algorithms and data sizes."""

    @staticmethod
    def generate_random_list(size: int, data_type: str = "int") -> List[Any]:
        """Generate a list of random integers or strings."""
        if data_type == "int":
            return [random.randint(1, 1_000_000) for _ in range(size)]
        elif data_type == "str":
            return [
                "".join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
                for _ in range(size)
            ]
        else:
            raise ValueError(f"Unsupported data_type: {data_type}")

    @staticmethod
    def run_benchmark(
        sizes: List[int],
        algorithms: List[str],
        data_type: str = "int",
        repeat: int = 3,
    ) -> Dict[int, Dict[str, float]]:
        """
        Run benchmark and return average times.

        :param sizes: List of dataset sizes to test.
        :param algorithms: List of algorithm names: 'recursive', 'direct', 'balanced'.
        :param data_type: 'int' or 'str'.
        :param repeat: Number of repetitions to average over.
        :return: Dict {size: {algo: avg_time_seconds}}
        """
        results = {}
        for size in sizes:
            print(f"Benchmarking size {size}...")
            data = Benchmark.generate_random_list(size, data_type)
            results[size] = {}
            for algo_name in algorithms:
                total_time = 0.0
                for _ in range(repeat):
                    if algo_name == "recursive":
                        sorter = RecursiveMergeSort()
                    elif algo_name == "direct":
                        sorter = DirectMergeSort()
                    elif algo_name == "balanced":
                        # Adaptive chunk size: at most 10% of list or 10,000
                        chunk = max(1000, size // 10)
                        sorter = BalancedMergeSort(chunk_size=chunk)
                    else:
                        continue
                    start = time.perf_counter()
                    sorter.sort(data.copy())
                    elapsed = time.perf_counter() - start
                    total_time += elapsed
                avg = total_time / repeat
                results[size][algo_name] = avg
        return results

    @staticmethod
    def display_benchmark(results: Dict[int, Dict[str, float]]) -> None:
        """Display benchmark results as a rich table."""
        table = Table(title="Benchmark Results (seconds, lower is better)")
        table.add_column("Size", style="cyan")
        table.add_column("Recursive Merge", style="green")
        table.add_column("Direct Merge", style="yellow")
        table.add_column("Balanced K‑Way", style="magenta")

        for size, algos in results.items():
            row = [
                str(size),
                f"{algos.get('recursive', 0):.4f}",
                f"{algos.get('direct', 0):.4f}",
                f"{algos.get('balanced', 0):.4f}",
            ]
            table.add_row(*row)
        console.print(table)