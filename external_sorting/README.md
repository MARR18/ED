# External Sorting Library

A professional Python library for sorting large datasets using external memory algorithms.  
Implements three classical algorithms:

- **Recursive Merge Sort** (Intercalación) – O(n log n), recursive, stable.
- **Direct Merge Sort** (Bottom‑Up) – iterative, no recursion, stable.
- **Balanced K‑Way Merge Sort** – external sorting for files larger than RAM, uses disk runs and heap merging.

## Features

- ✅ Sort numbers, strings, or custom objects with `key` functions.
- ✅ Ascending / descending order.
- ✅ Work with in‑memory lists OR large files (TXT, CSV, JSON, Excel).
- ✅ Configurable chunk size and number of ways (`k`) for balanced merge.
- ✅ Optional multiprocessing for parallel run creation.
- ✅ Detailed statistics: time, memory, comparisons, merges.
- ✅ Progress bars with `rich`.
- ✅ CLI tool `extsort` with Typer.
- ✅ Benchmark suite to compare algorithms.
- ✅ Fully typed, documented, and tested.

## Installation

```bash
git clone https://github.com/yourusername/external_sorting.git
cd external_sorting
pip install -e .