"""Command‑line interface using Typer."""

from pathlib import Path
from typing import List, Optional

import typer

from . import BalancedMergeSort, Benchmark, DirectMergeSort, RecursiveMergeSort

app = typer.Typer(help="Professional external sorting library CLI")


@app.command()
def sort(
    input_file: Path = typer.Argument(..., help="Path to input file"),
    output_file: Path = typer.Argument(..., help="Path for sorted output"),
    algorithm: str = typer.Option(
        "balanced", "--algo", "-a", help="Algorithm: recursive, direct, balanced"
    ),
    reverse: bool = typer.Option(False, "--reverse", "-r", help="Descending order"),
    key: Optional[str] = typer.Option(
        None, "--key", help="Key function as lambda, e.g. 'x: x[1]'"
    ),
    k: int = typer.Option(8, "--k", help="Number of ways for balanced merge"),
    chunk_size: int = typer.Option(
        100000, "--chunk-size", help="Records per chunk (balanced merge)"
    ),
    visual: bool = typer.Option(False, "--visual", help="Show recursion tree (recursive)"),
    show_blocks: bool = typer.Option(False, "--show-blocks", help="Show block sizes (direct)"),
):
    """Sort a file using the chosen external sorting algorithm."""
    key_func = None
    if key:
        try:
            # Security note: eval is used for convenience; in production restrict to safe functions.
            key_func = eval(f"lambda {key}")
        except Exception as e:
            typer.echo(f"Invalid key function: {e}", err=True)
            raise typer.Exit(1)

    if algorithm == "recursive":
        sorter = RecursiveMergeSort(reverse=reverse, key=key_func, visual=visual)
        sorter.sort_file(str(input_file), str(output_file))
    elif algorithm == "direct":
        sorter = DirectMergeSort(
            reverse=reverse, key=key_func, show_block_sizes=show_blocks
        )
        sorter.sort_file(str(input_file), str(output_file))
    elif algorithm == "balanced":
        sorter = BalancedMergeSort(
            k=k, chunk_size=chunk_size, reverse=reverse, key=key_func
        )
        sorter.sort_file(str(input_file), str(output_file))
    else:
        typer.echo(f"Unknown algorithm: {algorithm}", err=True)
        raise typer.Exit(1)

    typer.echo(f"✅ Sorting completed. Output saved to {output_file}")


@app.command()
def benchmark(
    sizes: List[int] = typer.Option(
        [1000, 10000, 100000], "--size", "-s", help="List of sizes to test"
    ),
    algorithms: List[str] = typer.Option(
        ["recursive", "direct", "balanced"], "--algo", "-a", help="Algorithms to benchmark"
    ),
    data_type: str = typer.Option("int", "--data-type", help="int or str"),
    repeat: int = typer.Option(3, "--repeat", help="Number of repetitions"),
):
    """Run performance benchmark and display results."""
    results = Benchmark.run_benchmark(sizes, algorithms, data_type, repeat)
    Benchmark.display_benchmark(results)


if __name__ == "__main__":
    app()